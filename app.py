from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from model_loader import caption_image, translate_caption
import uvicorn

app = FastAPI()

# Allow frontend (running on file:// or localhost) to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev only
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/caption")
async def get_caption(request: Request):
    data = await request.json()
    base64_img = data.get("image")

    if not base64_img:
        return {"error": "No image provided."}

    caption = caption_image(base64_img)
    translation = translate_caption(caption, target_lang="fr")

    return {
        "caption": caption,
        "translation": translation
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
