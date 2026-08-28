import os
from dotenv import load_dotenv

# 读取配置并记载为环境变量
load_dotenv()

MODEL_API_KEY = os.getenv("MODEL_API_KEY")
MODEL_BASE_URL = os.getenv("MODEL_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

def validate_config() -> None:
    """
    验证配置是否正确, 如果配置不正确则抛出异常
    """
    missing = []

    if not MODEL_API_KEY:
        missing.append("MODEL_API_KEY")

    if not MODEL_BASE_URL:
        missing.append("MODEL_BASE_URL")

    if not MODEL_NAME:
        missing.append("MODEL_NAME")

    if missing:
        raise RuntimeError(
            "Missing required environment variables: "
            + ", ".join(missing)
        )
