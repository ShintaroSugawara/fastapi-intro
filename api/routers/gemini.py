from fastapi import APIRouter
from pydantic import BaseModel
from google import genai

router = APIRouter()


class GeminiRequest(BaseModel):
    prompt: str


@router.post("/gemini")
def ask_gemini(request: GeminiRequest):
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=request.prompt,
    )

    return {
        "answer": response.text
    }