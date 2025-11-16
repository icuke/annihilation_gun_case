import httpx

API_URL = "http://localhost:8000/api/pdf"


def get_status(document_id):
    response = httpx.get(f"{API_URL}/status/{document_id}/")
    return response


def get_result(document_id):
    response = httpx.get(f"{API_URL}/result/{document_id}/")
    return response
