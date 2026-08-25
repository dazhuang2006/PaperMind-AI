# 路由汇总：所有接口模块在这里统一挂载
from fastapi import APIRouter

from app.api.health import router as health_router

api_router = APIRouter()              # 创建总路由
api_router.include_router(health_router)  
