# annihilation_gun_case
Общий репозиторий проекта. Отдельные репозитории для backend и бота доступны по ссылкам:

https://github.com/icuke/annihilation_gun_backend - Backend;
https://github.com/uzer2232/annihilation_gun_bot - бот.

# annihilation_gun_backend
Бэкэнд и API на Django REST Framework для OCR парсера инвойсов.

# Set-up:

Склонируйте репозиторий:

        git clone https://github.com/icuke/annihilation_gun_backend

Для установки на baremetal:
1. Установите зависимости:


        pip install -r requirements.txt

2. Выполните миграции:
   
           python ./manage.py  makemigrations pds_processor
           python ./manage.py migrate
   
4. Запустите сервер локально:


       python ./manage.py runserver

Порт по умолчанию 8000.

Для установки в контейнер Docker:
1. Используйте docker-compose для разворачивания контейнера:

        docker compose up --build

# Usage:

Для загрузки файлов используйте POST запрос на URL <hostname>/api/pdf/upload/ формата form-data в теле запроса с ключем original_file:
Пример запроса на Python:

    import requests

    API_URL = "http://localhost:8000/api/pdf/upload/"  
    PDF_PATH = "path\\to\\file.pdf"

    def test_pdf_upload():
    with open(PDF_PATH, "rb") as f:
        files = {
            "original_file": ("test.pdf", f, "application/pdf")
        }

        try:
            response = requests.post(API_URL, files=files)
            print("Status code:", response.status_code)
            print("Response:")
            print(response.json())

        except Exception as e:
            print("Error:", e)


        if __name__ == "__main__":
            test_pdf_upload()

В ответе на запрос в поле document_id будет представлен UUID вашего запроса. Используя GET запросы на URL /api/pdf/result/<document_id> и /api/pdf/status/<document_id> вы можете получить спаршенный JSON и статус реквеста соответственно.

Админская панель доступна по URL /admin/. Дефолтные креды: admin/admin. Для создания суперюзера используйте:

    python ./manage.py createsuperuser
