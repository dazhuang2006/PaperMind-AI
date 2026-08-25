# 初始化数据库：执行后自动创建所有表
import backend.app.model  # 必须导入，让模型先注册到 Base 上

from backend.app.database import Base, engine

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)  # 表不存在就创建，已存在不动
    print("数据库初始化完成")