import os
import io
import fitz  # PyMuPDF
from PIL import Image
from langchain_core.documents import Document
from backend.core.llm import llm
import time

def extract_visual_summary(image_bytes: bytes, element_type: str = "Image") -> str:
    """
    Passes raw extracted images or table blocks to the Vision LLM 
    to compile a comprehensive, text-searchable descriptive summary.
    """
    print(f"   👁️ [VISION ENGINE] Analyzing extracted {element_type} architecture...")
    
    # Format a prompt specifically instructing the model to output data vectors
    prompt = f"""
    You are an expert multi-modal research analyzer. Look at this extracted document {element_type}. 
    Provide a highly detailed, comprehensive, and grounded textual summary describing exactly what data, 
    trends, formulas, architectures, charts, or values are being communicated. 
    Ensure any numbers, axis labels, legends, or technical components are precisely recorded.
    """
    
    try:
        # Construct the multi-modal payload structure for LangChain / GitHub Models
        # (This structure supports transmitting inline visual image byte payloads)
        message = {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_bytes}"}
                }
            ]
        }
        
        response = llm.invoke([message])
        return f"[{element_type} Summary] {response.content}"
    except Exception as e:
        print(f"   ⚠️ Vision analysis bypassed or failed: {e}")
        return f"Unprocessed document {element_type} element."

def process_multimodal_pdf(pdf_path: str) -> list[Document]:
    """
    Upgraded Multi-Modal Parser with rate-limit protection guardrails.
    """
    print(f"🧬 [MULTIMODAL PARSER] Beginning layout-aware extraction for: {os.path.basename(pdf_path)}")
    doc_elements = []
    pdf_document = fitz.open(pdf_path)
    
    # 💡 Safety Constraints for Free API Tiers
    MAX_IMAGES_PER_DOC = 3   # Don't let a single file burn your whole daily quota
    MIN_IMAGE_SIZE_BYTES = 10 * 1024  # Ignore elements smaller than 10KB (logos, lines, icons)
    processed_images_count = 0
    
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        
        # 1. Standard Text Block Extraction
        text_content = page.get_text("text")
        if text_content.strip():
            doc_elements.append(Document(
                page_content=text_content,
                metadata={"source": os.path.basename(pdf_path), "page": page_num + 1, "type": "text"}
            ))
            
        # 2. Guarded Image / Diagram Extraction Loop
        image_list = page.get_images(full=True)
        for img_idx, img_meta in enumerate(image_list):
            if processed_images_count >= MAX_IMAGES_PER_DOC:
                break  # Stop processing images if we hit our safe session limit
                
            xref = img_meta[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            
            # 💡 Filter out tiny decorative icons or lines
            if len(image_bytes) < MIN_IMAGE_SIZE_BYTES:
                continue
                
            import base64
            b64_image = base64.b64encode(image_bytes).decode("utf-8")
            
            # Call the vision engine
            img_summary = extract_visual_summary(b64_image, element_type="Diagram/Chart")
            processed_images_count += 1
            
            doc_elements.append(Document(
                page_content=img_summary,
                metadata={"source": os.path.basename(pdf_path), "page": page_num + 1, "type": "visual_element"}
            ))
            
            # 💡 Pace out requests to avoid the per-minute rate limit flag
            time.sleep(3)
            
    print(f"   ✅ Extraction Concluded. Successfully generated {len(doc_elements)} chunks. (Analyzed {processed_images_count} key diagrams)")
    return doc_elements