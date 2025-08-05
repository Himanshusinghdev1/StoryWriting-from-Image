from pathlib import Path
import logging
from PIL import Image
import torch
from transformers import AutoProcessor, AutoModelForCausalLM

logger = logging.getLogger(__name__)

class ImageCaptioning:
    def __init__(self, config):
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = AutoProcessor.from_pretrained(config.florence2_model_name, trust_remote_code=True )
        self.model = AutoModelForCausalLM.from_pretrained(config.florence2_model_name, trust_remote_code=True ).to(self.device)
        self.config.captions_dir.mkdir(parents=True, exist_ok=True)

    def caption_image(self, image_path: Path) -> str:
        image = Image.open(image_path)
        inputs = self.processor(
            text=self.config.task_prompt,
            images=image,
            return_tensors="pt"
        )
        inputs = {k: v.to(self.device) if hasattr(v, 'to') else v for k, v in inputs.items()}
        generated_ids = self.model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=self.config.max_new_tokens,
            num_beams=self.config.num_beams,
            early_stopping=True,
            do_sample=False
        )
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
        # Post-process/correct generated text
        parsed_answer = self.processor.post_process_generation(
            generated_text,
            task=self.config.task_prompt,
            image_size=(image.width, image.height)
        )
        caption = parsed_answer.get(self.config.task_prompt, "").strip()
        # Save caption
        caption_file = self.config.captions_dir / f"{image_path.stem}_caption.txt"
        with open(caption_file, "w") as f:
            f.write(caption)
        logger.info(f"Caption saved at: {caption_file}")
        return caption
