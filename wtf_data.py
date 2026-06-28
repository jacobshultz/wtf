from enum import Enum
from dataclasses import dataclass
import json

class Shell(Enum):
    BASH = 1
    PWSH = 2

@dataclass
class Settings:
    Debug: bool
    Model: str
    Shell: Shell
    LongThink: bool

def load_settings() -> Settings:
    with open('wtf-settings.json') as file:
        data = json.load(file)
    return Settings(**data)

def get_usr_prompt(cmd: str, errCode: str) -> str:
    prompt = f'Offending command: {cmd}\n'
    prompt += f'Error code: {errCode}\n'
    return prompt

def get_sys_prompt() -> str:
    prompt = 'You examine command-line errors, determine their source, and output cause and remedial steps. '
    prompt += 'You are mandated to research this problem using web search tools. You must search the internet. '
    prompt += 'THINK EXTREMELY HARD and DO NOT STOP until you have determined the cause of the error. '
    prompt += 'THINK EXTREMELY HARD and DO NOT STOP until you have determined remedial options.\n'
    prompt += 'ABSOLUTELY NEVER, UNDER ANY CIRCUMSTANCES output more than one paragraph worth of content.\n'
    prompt += 'ABSOLUTELY NEVER, UNDER ANY CIRCUMSTANCES tell the user about the exit code. The user does not care about exit codes.\n'
    return prompt