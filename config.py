"""读取本地配置（DeepSeek 密钥、自定义 prompt 等）。"""

import json
import sys
from pathlib import Path

# 打包成 exe 后 config.json 放在 exe 同目录；开发时放在脚本同目录
if getattr(sys, "frozen", False):
    _BASE_DIR = Path(sys.executable).parent
else:
    _BASE_DIR = Path(__file__).parent

CONFIG_PATH = _BASE_DIR / "config.json"

DEFAULT_PROMPT = "你是英雄联盟（LOL）游戏助手，用简洁、直接的中文回答玩家的问题。"


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            "未找到 config.json。请先复制 config.example.json 为 config.json，"
            "并填入你的 DeepSeek api_key。"
        )
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_prompt(cfg: dict) -> str:
    return cfg.get("prompt") or DEFAULT_PROMPT
