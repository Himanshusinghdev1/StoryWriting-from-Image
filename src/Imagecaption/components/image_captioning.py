from pathlib import Path
import logging
import base64
import os
import streamlit as st
from together import Together

logger = logging.getLogger(__name__)

class ImageCaptioning:
    def __init__(self, config):
        self.config = config
        self.config.captions_dir.mkdir(parents=True, exist_ok=True)
        
        # Robust API key retrieval (Streamlit secrets + local env fallback)
        try:
            api_key = st.secrets["TOGETHER_API_KEY"]
        except Exception:
            api_key = os.getenv("TOGETHER_API_KEY", "")
            
        self.client = Together(api_key=api_key)

    def caption_image(self, image_path: Path) -> str:
        logger.info("Attempting to generate caption using Together.ai vision model...")
        
        try:
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                
            prompt = "Describe this image in 2-3 vivid sentences. Focus on the setting, mood, characters or objects present, and any emotions the scene conveys. Make it suitable for inspiring a short creative story."
            
            response = self.client.chat.completions.create(
                model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
            )
            caption = response.choices[0].message.content.strip()
            logger.info("Together.ai vision model captioning succeeded!")
            
        except Exception as api_err:
            logger.warning(f"Together.ai vision model failed or not available ({api_err}). Falling back to local Florence-2 model...")
            
            # Local Florence-2 fallback loading and inference
            import torch
            from transformers import AutoProcessor, AutoModelForCausalLM
            from PIL import Image
            
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            logger.info(f"Loading local Florence-2 model on {device}...")
            
            processor = AutoProcessor.from_pretrained("microsoft/Florence-2-base-ft", trust_remote_code=True, revision="main")
            torch_dtype = torch.float16 if device.type != "cpu" else torch.float32
            model = AutoModelForCausalLM.from_pretrained(
                "microsoft/Florence-2-base-ft", 
                trust_remote_code=True, 
                torch_dtype=torch_dtype, 
                revision="main"
            ).to(device).eval()
            
            image = Image.open(image_path)
            inputs = processor(text="<MORE_DETAILED_CAPTION>", images=image, return_tensors="pt")
            inputs = {k: v.to(device) if hasattr(v, 'to') else v for k, v in inputs.items()}
            
            with torch.no_grad():
                generated_ids = model.generate(
                    input_ids=inputs["input_ids"],
                    pixel_values=inputs["pixel_values"],
                    max_new_tokens=64,
                    num_beams=3,
                    early_stopping=True,
                    do_sample=False
                )
            generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
            parsed_answer = processor.post_process_generation(
                generated_text,
                task="<MORE_DETAILED_CAPTION>",
                image_size=(image.width, image.height)
            )
            caption = parsed_answer.get("<MORE_DETAILED_CAPTION>", "").strip()
            logger.info("Local Florence-2 fallback captioning succeeded!")

        # Save caption to captions_dir
        caption_file = self.config.captions_dir / f"{image_path.stem}_caption.txt"
        with open(caption_file, "w", encoding="utf-8") as f:
            f.write(caption)
            
        logger.info(f"Caption saved at: {caption_file}")
        return caption
