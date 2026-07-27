from .data import with_rolling_spinner, CONFIG_PATH
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path=os.path.join(CONFIG_PATH, ".env"))
from .ollama_client import OllamaClient
from .data import load_settings
from .arguments import bind_and_get_args
import traceback


def main():
    settings = load_settings()

    try:
        args = bind_and_get_args(settings)
        if args.version: 
            print(f"WTF v{settings.Version}\nCreated by Jacob Shultz")
            return

        HISTORY = os.environ.get("WTF_HISTORY", "")
        EXIT_CODE = os.environ.get("WTF_EXIT", "0")

        if HISTORY == "": raise RuntimeError("Failed to grab command history. You may be running in a non-interactive environment.")

        if settings.Debug:
            print(f"settings={settings}")
            print(f"history={HISTORY}")
            print(f"errorCode={EXIT_CODE}")

        msg = with_rolling_spinner(lambda: OllamaClient.query(HISTORY, EXIT_CODE, settings))
        print();
        print(msg if msg is not None else "wtf: Model did not answer.")
        
    except Exception as ex:
        if settings.Debug:
            print(f"wtf: {traceback.format_exc()}")
        else:
            print(f"wtf: {ex}")

if __name__ == "__main__":
    main()