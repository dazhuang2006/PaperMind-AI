#给前端返回josn结构
# 接口返回的数据结构（Pydantic 模型）
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PaperOut(BaseModel):
    """论文信息，上传成功后返回给前端"""
    id: int
    title: str
    authors: str
    file_name: str
    page_count: int
    created_at: datetime

    # 允许直接从 SQLAlchemy 模型对象转换
    model_config = ConfigDict(from_attributes=True)