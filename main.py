import qrcode
import base64

from io import BytesIO

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/send_data")
async def send_data(data: dict):
    text_input = data.get("textInput", "")
    if text_input == "":
        return JSONResponse({"error": "text input is required"}, status_code=400)
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text_input)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    # Save the QR code image to a BytesIO buffer
    img_buffer = BytesIO()
    img.save(img_buffer, format="PNG")

    # Get the byte data from the buffer
    img_bytes = img_buffer.getvalue()

    # Encode the image in base64
    base64_encoded_image = base64.b64encode(img_bytes).decode("utf-8")

    return JSONResponse(
        {
            "response": base64_encoded_image,
            "file_name": human_readable_name(text_input),
        }
    )


def human_readable_name(text: str) -> str:
    if text.endswith("/"):
        text = text[:-1]
    return text.replace("https://", "").replace("https://", "").replace("/", ".")
