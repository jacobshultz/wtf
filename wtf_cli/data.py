from enum import Enum
from os import path
from pathlib import Path
from dataclasses import dataclass
import random
import json
import itertools
import threading
import time
import getpass
from yaspin import yaspin

CONFIG_PATH = path.join(Path.home(), ".config", "wtf")
ENV_PATH = path.join(CONFIG_PATH, ".env")
SETTINGS_PATH = path.join(CONFIG_PATH, "wtf-settings.json")
PROMPT_PATH = path.join(CONFIG_PATH, "PROMPT.txt")

@dataclass
class Settings:
    Version: str
    Debug: bool
    Model: str
    UseTools: bool
    Think: bool

def load_settings() -> Settings:
    with open(SETTINGS_PATH) as file:
        data = json.load(file)
    return Settings(**data)

def key_status() -> bool:
    is_fine = True  # fine, do not need to set up
    if not path.exists(ENV_PATH):
        print("UseTools is set to true, but you do not have an Ollama API key for the model to use. This will cause errors!")
        print(f"To suppress this message set UseTools to false in {SETTINGS_PATH}")
        answer = input("(Recommended) Would you like to set the api key now? y/n: ").strip().lower()
        is_fine = answer not in ('y', 'yes')    # false means need to set up the key
    
    return is_fine

def set_key():
    if path.exists(ENV_PATH):
        ans = input("It appears you've already set the API key for this utility. Would you like to continue? y/n: ").strip().lower()
        if ans not in ('y', "yes"): 
            print(f"To view or modify the api key entry visit {ENV_PATH}")
            return

    print("Enter your ollama API key to allow the model to search the internet.")
    print("Follow the steps at https://docs.ollama.com/capabilities/web-search (see Authentication) then return here.")
    api_key = getpass.getpass("Paste your Ollama API key: ")
    with open(ENV_PATH, "a") as e:
        e.write(f"OLLAMA_API_KEY={api_key}\n")

    print(f"Done. To view or modify this entry visit {ENV_PATH}")
    return

def get_usr_prompt(hist: str, errCode: str) -> str:
    prompt = f'HISTORY: {hist}\n'
    prompt += f'EXIT CODE: {errCode}\n'
    return prompt

def get_sys_prompt() -> str:
    with open(PROMPT_PATH, encoding="utf-8") as file:
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