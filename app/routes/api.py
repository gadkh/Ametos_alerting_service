from fastapi import APIRouter
from .alerts import router as alerts_router

router = APIRouter(prefix="/v1")

router.include_router(alerts_router)
