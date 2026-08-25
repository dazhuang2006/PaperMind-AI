from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_ROOT = BACKEND_DIR.parent


# 1. 去项目根目录找 .env
# 2. 文件用 utf-8 编码
# 3. .env 里多余的变量忽略，不报错
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    #服务器相关
    app_name: str = "PaperMind AI Backend"
    debug: bool = False
    api_prefix: str = "/api"

    #大模型配置
    deepseek_api_key: str = ""
    llm_model: str = "deepseek-chat"
    llm_base_url: str = "https://api.deepseek.com/v1"
    #项链数据库
    database_url: str = "sqlite:///./papermind.db"
    milvus_uri: str = ""
    upload_dir: str = "storage/papers"

    @property
    #把相对路径变成绝对路径
    def storage_dir(self) -> Path:
        path = Path(self.upload_dir)
        return path if path.is_absolute() else BACKEND_DIR / path

    def ensure_storage_dirs(self) -> None:
        for name in ("papers", "images", "temp"):
            # 服务启动时自动创建存储目录
            (self.storage_dir.parent / name).mkdir(parents=True, exist_ok=True)
            #                                没有就创建，有也不报错

#实例化
settings = Settings()