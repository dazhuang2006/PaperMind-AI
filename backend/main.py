# FastAPI 应用入口：把配置、路由、中间件组装成完整服务
from contextlib import asynccontextmanager  # 用来写"启动时/关闭时"逻辑

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 允许前端跨域访问

from backend.app.api.router import api_router  # 汇总后的所有接口
from backend.app.core.config import settings   # 全局配置


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 服务启动时自动执行：创建 storage 目录
    settings.ensure_storage_dirs()
    yield



app = FastAPI(
    title=settings.app_name,  # Swagger 文档标题
    lifespan=lifespan,        # 注册启动逻辑,应用启动的时候执行一段初始化代码；
                              # 应用关闭的时候执行清理回收代码。
)

# 配置跨域：开发阶段允许所有来源访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # 允许的域名，* 表示全部
    allow_credentials=True,     # 允许携带 Cookie
    allow_methods=["*"],        # 允许所有 HTTP 方法（GET/POST/...）
    allow_headers=["*"],        # 允许所有请求头
)

# 把路由挂到应用上，并统一加 /api 前缀
app.include_router(api_router, prefix=settings.api_prefix)
