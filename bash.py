import sys
from dotenv import load_dotenv
load_dotenv()
import ollama
from ollama_client import OllamaClient
from wtf_data import load_settings

# `wtf` must translate to `python bash.py "$?" "$(fc -ln -1)"`

try:
    LAST_CMD = sys.argv[2].strip() if len(sys.argv) > 1 else ""      # must be "$(fc -ln -1)"
    ERROR_CODE = sys.argv[1] if len(sys.argv) > 2 else ""    # must be "$?"

    settings = load_settings()
    if settings.Debug:
        print(f"settings={settings}")
        print(f"lastCmd={LAST_CMD}")
        print(f"errorCode={ERROR_CODE}")

    # send to server
    msg = OllamaClient.query(LAST_CMD, ERROR_CODE, settings)
    print(msg if msg is not None else "wtf: Model did not answer.")
except Exception as ex:
    print(f"wtf: {ex}")