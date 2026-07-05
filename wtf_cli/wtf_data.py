from enum import Enum
from os import path
from pathlib import Path
from dataclasses import dataclass
import json

@dataclass
class Settings:
    Debug: bool
    Model: str
    UseTools: bool
    LongThink: bool

def load_settings() -> Settings:
    dir = path.join(Path.home(), ".config", "wtf", "wtf-settings.json")
    with open(dir) as file:
        data = json.load(file)
    return Settings(**data)

def get_usr_prompt(hist: str, errCode: str) -> str:
    prompt = f'HISTORY: {hist}\n'
    prompt += f'EXIT CODE: {errCode}\n'
    return prompt

def get_sys_prompt() -> str:
    dir = path.join(Path.home(), ".config", "wtf", "PROMPT.txt")
    with open(dir, encoding="utf-8") as file:
        return file.read()