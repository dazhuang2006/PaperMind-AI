# 论文上传与列表接口
import uuid
from io import BytesIO
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pypdf import PdfReader
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.database import get_db
from backend.app.model import Paper
from backend.app.schemas import PaperOut

router = APIRouter(prefix="/papers", tags=["papers"])


@router.post("/upload", response_model=PaperOut)
def upload_paper(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. 只允许 PDF
    if not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="只支持 PDF 文件")

    # 2. 确保存储目录存在
    settings.ensure_storage_dirs()

    # 3. 生成唯一文件名，避免覆盖
    suffix = Path(file.filename).suffix.lower()          # 取扩展名，例如 .pdf
    unique_name = f"{uuid.uuid4().hex}{suffix}"          # 例如 3f2a...9c.pdf
    file_path = settings.storage_dir / unique_name        # 完整保存路径

    # 4. 读取上传内容并写入磁盘
    content = file.file.read()
    file_path.write_bytes(content)

    # 5. 用 pypdf 读取 PDF 页数（解析失败也不影响上传）
    page_count = 0
    try:
        reader = PdfReader(BytesIO(content))
        page_count = len(reader.pages)
    except Exception:
        page_count = 0

    # 6. 写入数据库
    paper = Paper(
        title=Path(file.filename).stem,   # 默认用文件名当标题，以后 PDF 解析再优化
        file_name=file.filename,          # 原始文件名
        file_path=str(file_path),         # 磁盘路径
        page_count=page_count,            # 页数
    )
    db.add(paper)
    db.commit()
    db.refresh(paper)   # 刷新出数据库自动生成的 id 和时间
    return paper


@router.get("", response_model=list[PaperOut])
def list_papers(db: Session = Depends(get_db)):
    # 按 id 倒序，最新上传的排前面
    return db.query(Paper).order_by(Paper.id.desc()).all()