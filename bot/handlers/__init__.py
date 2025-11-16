from aiogram import Router

from . import pdf, start


def get_handlers_router() -> Router:
    router = Router()
    router.include_router(start.router)
    router.include_router(pdf.router)

    return router