import json
import time

from aiogram import F, Router
from aiogram.types import BufferedInputFile, Message
from services import api
from services.pdf_process import pdf_download, pdf_upload

router = Router(name="pdf")


@router.message(F.content_type.in_("document"))
async def pdf_process(message: Message):
    doc = message.document
    if doc is None or doc.file_name is None:
        return ValueError("Произошла ошибка при получении документа из сообщения")
    bot = message.bot
    if bot is None:
        return

    file = await bot.get_file(doc.file_id)
    send_msg = await message.reply("Загрузка файла...")
    pdf_download(
        file_name=doc.file_name, file_id=file.file_id, file_path=file.file_path
    )
    r = pdf_upload(file_name=doc.file_name)
    if r is None:
        return ValueError("Ошибка при получении ответа от API")
    print(r.status_code)

    if r.status_code == 201:
        await send_msg.edit_text("Файл загружен, приступаем к обработке...")
        document_id = r.json()["document_id"]
        for i in range(5):
            r = api.get_status(document_id)
            print(r.json()["processed"])
            if not r.json()["processed"]:
                time.sleep(10)
            else:
                break
        if r.status_code == 200:
            print()
            r = api.get_result(document_id)
            json_data: dict = r.json()["result"]
            json_parsed = json.dumps(json_data, indent=2, ensure_ascii=False)
            try:
                if len(json_parsed) > 4096:
                    await message.reply(
                        f"<pre>{json_parsed[:4076]}</pre>\nПолный JSON в файле"
                    )
                    json_file_name = doc.file_name.split(".")[0] + ".json"
                    print(json_file_name)
                    json_parsed_path = f"bot/files/{json_file_name}"
                    with open(json_parsed_path, "w", encoding="utf-8") as f:
                        json.dump(json_parsed, f, indent=2, ensure_ascii=False)
                    await message.answer_document(
                        BufferedInputFile.from_file(json_parsed_path)
                    )
                else:
                    await message.reply(json_parsed)
            except Exception as e:
                await message.reply(f"При обработке файла произошла ошибка: {e}")
