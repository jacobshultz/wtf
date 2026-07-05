from ollama import chat, web_fetch, web_search, ChatResponse
from wtf_cli.wtf_data import Settings, get_usr_prompt, get_sys_prompt

available_tools = {'web_search': web_search, 'web_fetch': web_fetch}

class OllamaClient:
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
                think=settings.LongThink,
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

        msg = response.message
        return msg.content