from fastapi import APIRouter

from app.api.agent import router as agent_router

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


router.include_router(agent_router)
