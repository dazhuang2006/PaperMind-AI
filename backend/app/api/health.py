# 健康检查接口：访问它就能知道服务是否正常
from fastapi import APIRouter  # APIRouter 用来管理一组接口

from backend.app.core.config import settings

# 创建一个路由对象
router = APIRouter(tags=["health"])



@router.get("/health")
def health() -> dict:
    #看这个接口是否正常,以判断后端是否正常
    return {
        "status": "ok",
        "app": settings.app_name,
    }
