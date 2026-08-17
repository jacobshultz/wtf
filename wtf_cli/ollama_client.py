import sys
from ollama import chat, pull, web_fetch, web_search, ChatResponse, ResponseError
from ollama import list as list_models
from .data import Settings, get_usr_prompt, get_sys_prompt

available_tools = {'web_search': web_search, 'web_fetch': web_fetch}

class OllamaClient:
    @staticmethod
    def model_exists(model: str) -> bool:
        wanted = model if ':' in model else f'{model}:latest'
        try:
            return any(m.model == wanted for m in list_models().models)
        except ResponseError:
            return False

    @staticmethod
    def ensure_model(settings: Settings) -> bool:
        if OllamaClient.model_exists(settings.Model):
            return True

        print(f"Model '{settings.Model}' is not installed locally.", file=sys.stderr)

        if not sys.stdin.isatty():
            print(f"Run: ollama pull {settings.Model}", file=sys.stderr)
            return False

        try:
            answer = input("Would you like to pull this model? y/n: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print(file=sys.stderr)
            return False

        if answer not in ('y', 'yes'):
            return False

        try:
            for progress in pull(settings.Model, stream=True):
                status = progress.status or ''
                total, done = progress.total, progress.completed
                if total and done:
                    print(f"\r{status}: {done / total * 100:5.1f}%", end='', flush=True)
                else:
                    print(f"\r{status} ", end='', flush=True)
            print()
        except ResponseError as e:
            print(f"\nFailed to pull '{settings.Model}': {e}", file=sys.stderr)
            return False

        return True

    @staticmethod
    def query(hist: str, errCode: str, settings: Settings) -> str | None:
        s_prompt = get_sys_prompt()
        u_prompt = get_usr_prompt(hist, errCode)

        messages = [
                {"role": "system", "content": f"{s_prompt} Research this problem using web_search and web_fetch tools."},
                {"role": "user", "content": f"{u_prompt}"},
            ]

        response: ChatResponse
        while True:
            response = chat(
                model=settings.Model,
                messages=messages,
                tools=[web_fetch, web_search] if settings.UseTools else None,
                think=settings.Think,
            )

            if response.message.tool_calls:
                if settings.Debug: print(f"called tools={response.message.tool_calls}")
                for call in response.message.tool_calls:
                    fn = available_tools.get(call.function.name)
                    if fn is not None:
                        result = fn(**call.function.arguments)
                        messages.append({
                            'role': 'tool',
                            'content': str(result)[:2000 * 4],  # truncate for context
                            'tool_name': call.function.name,
                        })
                    else:
                        messages.append({'role': 'tool',
                            'content': f'Tool {call.function.name} not found',
                            'tool_name': call.function.name,
                        })
            else:
                break

        msg = response.message.content
        if not settings.Think:
            msg = msg.rsplit("\n", 1)[-1]   # no think returns the model's thinking in the response. grab the last line only (the actual answer).
        return msg