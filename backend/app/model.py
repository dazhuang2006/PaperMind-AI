# 数据库表结构（ORM 模型）
from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base


class Paper(Base):
    """论文表：每篇上传的 PDF 对应一行"""
    __tablename__ = "papers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), default="")      # 标题
    authors: Mapped[str] = mapped_column(Text, default="")           # 作者，多个用逗号分隔
    abstract: Mapped[str] = mapped_column(Text, default="")          # 摘要
    file_name: Mapped[str] = mapped_column(String(500))              # 原始文件名
    file_path: Mapped[str] = mapped_column(String(1000))             # 存储路径
    page_count: Mapped[int] = mapped_column(Integer, default=0)      # 页数
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # 一对多：一篇论文有多个切片
    chunks: Mapped[list["Chunk"]] = relationship(back_populates="paper", cascade="all, delete-orphan")


class Chunk(Base):
    """切片表：论文被切成的小段，RAG 检索的最小单位"""
    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    paper_id: Mapped[int] = mapped_column(ForeignKey("papers.id", ondelete="CASCADE"), index=True)
    text: Mapped[str] = mapped_column(Text)                            # 切片内容
    page: Mapped[int] = mapped_column(Integer, default=0)              # 来自第几页
    section: Mapped[str] = mapped_column(String(200), default="")      # 来自哪个章节
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    paper: Mapped["Paper"] = relationship(back_populates="chunks")


class Conversation(Base):
    """对话表：一次科研问答会话"""
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), default="新对话")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    messages: Mapped[list["Message"]] = relationship(back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    """消息表：对话里的每一条问答"""
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id", ondelete="CASCADE"), index=True)
    role: Mapped[str] = mapped_column(String(20))      # user / assistant
    content: Mapped[str] = mapped_column(Text)         # 消息内容
    sources: Mapped[list] = mapped_column(JSON, default=list)  # 引用来源，以后存 [{paper_id, page, text}]
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    conversation: Mapped["Conversation"] = relationship(back_populates="messages")