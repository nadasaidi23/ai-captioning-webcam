# model_loader.py

from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import io
import base64
from transformers import MarianMTModel, MarianTokenizer

# Load model and processor once at startup
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def caption_image(base64_image: str) -> str:
    # Decode base64 → bytes → PIL image
    image_data = base64.b64decode(base64_image)
    image = Image.open(io.BytesIO(image_data)).convert("RGB")

    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=30)
    
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

# Load English-to-French translator
trans_model_name = "Helsinki-NLP/opus-mt-en-fr"
trans_tokenizer = MarianTokenizer.from_pretrained(trans_model_name)
trans_model = MarianMTModel.from_pretrained(trans_model_name)

def translate_caption(text: str, target_lang: str = "fr") -> str:
    if not text.strip():
        return ""
    inputs = trans_tokenizer([text], return_tensors="pt", padding=True)
    translated = trans_model.generate(**inputs)
    return trans_tokenizer.decode(translated[0], skip_special_tokens=True)