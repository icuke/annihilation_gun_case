import httpx
from config import settings

API_URL = "http://localhost:8000/api/pdf/upload/"
PDF_SAVE_DIR = "bot/files"


def pdf_download(file_id, file_path, file_name):
    download_url = f"https://api.telegram.org/file/bot{settings.BOT_TOKEN}/{file_path}"
    download_save_path = f"{PDF_SAVE_DIR}/{file_name}"
    r = httpx.get(download_url)
    if r.status_code == 200:
        with open(download_save_path, "wb") as f:
            f.write(r.content)
        print("File downloaded")
    else:
        print("Failed to download the file")


def pdf_upload(file_name):
    pdf_path = f"{PDF_SAVE_DIR}/{file_name}"
    with open(pdf_path, "rb") as f:
        files = {"original_file": (f"{file_name}", f, "application/pdf")}

        try:
            r = httpx.post(API_URL, files=files)
            print("Status code:", r.status_code)
            print("Response:")
            print(r.json())
            return r

        except Exception as e:
            print("Error:", e)