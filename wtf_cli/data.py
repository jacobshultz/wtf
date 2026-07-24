from enum import Enum
from os import path
from pathlib import Path
from dataclasses import dataclass
import random
import json
import itertools
import threading
import time
from yaspin import yaspin

CONFIG_PATH = path.join(Path.home(), ".config", "wtf")

@dataclass
class Settings:
    Version: str
    Debug: bool
    Model: str
    UseTools: bool
    Think: bool

def load_settings() -> Settings:
    with open(path.join(CONFIG_PATH, "wtf-settings.json")) as file:
        data = json.load(file)
    return Settings(**data)

def get_usr_prompt(hist: str, errCode: str) -> str:
    prompt = f'HISTORY: {hist}\n'
    prompt += f'EXIT CODE: {errCode}\n'
    return prompt

def get_sys_prompt() -> str:
    with open(path.join(CONFIG_PATH, "PROMPT.txt"), encoding="utf-8") as file:
        return file.read()
    
def _roll_thinking_synonym() -> str:
    syns = [
        "Thinking", "Pondering", "Analyzing", "Pondering", "Contemplating", "Deliberating",
        "Reasoning", "Musing", "Ruminating", "Evaluating", "Assessing", "Examining", "Studying",
        "Reviewing", "Processing", "Figuring", "Puzzling", "Reckoning", "Supposing",
        "Surmising", "Deducing", "Inferring", "Concluding", "Judging", "Gauging", "Estimating",
        "Speculating", "Theorizing", "Hypothesizing",  "Envisioning", "Conceiving", "Conceptualizing",
        "Brainstorming", "Meditating", "Cogitating", "Ideating", "Wondering", "Intellectualizing",
        "Questioning", "Probing"
    ]

    return random.choice(syns)


def _animate(spinner, stop_event,
             dot_interval=0.4, min_reroll=5, max_reroll=12):
    dots = itertools.cycle([".", "..", "..."])
    word = _roll_thinking_synonym()
    next_reroll = time.monotonic() + random.uniform(min_reroll, max_reroll)

    while not stop_event.is_set():
        now = time.monotonic()
        if now >= next_reroll:
            word = _roll_thinking_synonym()
            next_reroll = now + random.uniform(min_reroll, max_reroll)

        spinner.text = word + next(dots)
        stop_event.wait(dot_interval)


def with_rolling_spinner(work):
    stop_event = threading.Event()
    with yaspin() as spinner:   # i am super lazy lol
        animator = threading.Thread(
            target=_animate,
            args=(spinner, stop_event),
            daemon=True,
        )
        animator.start()
        try:
            return work()
        finally:
            stop_event.set()
            animator.join()