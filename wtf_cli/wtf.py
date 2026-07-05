from dotenv import load_dotenv
from os import path
from pathlib import Path
dir = path.join(Path.home(), ".config", "wtf", ".env")
load_dotenv(dotenv_path=dir)
import os
from wtf_cli.ollama_client import OllamaClient
from wtf_cli.wtf_data import load_settings

def main():
    try:
        HISTORY = os.environ.get("WTF_HISTORY", "")
        EXIT_CODE = os.environ.get("WTF_EXIT", "0")

        if HISTORY == "": raise RuntimeError("Failed to grab command history. Try running a few commands first.")

        settings = load_settings()
        if settings.Debug:
            print(f"settings={settings}")
            print(f"lastCmd={HISTORY}")
            print(f"errorCode={EXIT_CODE}")

        # send to server
        print("Thinking...")
        msg = OllamaClient.query(HISTORY, EXIT_CODE, settings)
        print(msg if msg is not None else "wtf: Model did not answer.")
    except Exception as ex:
        print(f"wtf: {ex}")