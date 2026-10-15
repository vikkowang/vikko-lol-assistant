"""读取/写入本地配置（千问 API 密钥、prompt、联网搜索开关等）。"""

import json
import os
import sys
from pathlib import Path

APP_DIR = "LOL助手"

DEFAULT_PROMPT = "你是英雄联盟（LOL）游戏助手，用简洁、直接的中文回答玩家的问题（50字以内）。注意：1）玩家提问来自语音识别，可能有同音字/错别字，尤其是英雄名、技能名、装备名，请结合英雄联盟知识自动纠正后再理解；2）涉及版本、胜率、出装等时效性问题时，优先依据联网搜索结果回答。"

DEFAULT_CONFIG = {
    "api_key": "",
    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "model": "qwen-plus",
    "prompt": DEFAULT_PROMPT,
    "web_search": True,
}


def _config_path() -> Path:
    if getattr(sys, "frozen", False):
        # 打包后配置统一存到用户目录，exe 移动、重装都不影响
        appdata = os.environ.get("APPDATA") or str(Path.home())
        return Path(appdata) / APP_DIR / "config.json"
    # 开发时用脚本同目录，方便调试
    return Path(__file__).parent / "config.json"


CONFIG_PATH = _config_path()


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        # 首次运行：写入默认配置，用户再通过设置界面填 key
        save_config(dict(DEFAULT_CONFIG))
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(cfg: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def get_prompt(cfg: dict) -> str:
    return cfg.get("prompt") or DEFAULT_PROMPT
