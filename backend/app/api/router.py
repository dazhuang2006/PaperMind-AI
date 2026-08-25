# 路由汇总：所有接口模块在这里统一挂载
from fastapi import APIRouter

from backend.app.api.health import router as health_router
from backend.app.api.papers import router as papers_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(papers_router)