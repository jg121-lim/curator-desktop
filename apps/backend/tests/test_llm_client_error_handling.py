class LLMProviderTimeoutError(Exception):
    pass


class LLMProviderAuthError(Exception):
    pass


class UpstreamLLMClient:
    def __init__(self, mode: str):
        self.mode = mode

    def chat(self, prompt: str) -> str:
        if self.mode == "timeout":
            raise LLMProviderTimeoutError("provider timed out")
        if self.mode == "auth":
            raise LLMProviderAuthError("invalid API key")
        return f"ok:{prompt}"


class SafeLLMClient:
    def __init__(self, upstream: UpstreamLLMClient):
        self.upstream = upstream

    def ask(self, prompt: str) -> dict:
        try:
            return {"ok": True, "answer": self.upstream.chat(prompt)}
        except LLMProviderTimeoutError:
            return {"ok": False, "code": "timeout", "message": "LLM request timed out"}
        except LLMProviderAuthError:
            return {"ok": False, "code": "auth", "message": "LLM authentication failed"}


def test_llm_client_returns_timeout_error_payload():
    client = SafeLLMClient(UpstreamLLMClient(mode="timeout"))

    result = client.ask("hello")

    assert result == {"ok": False, "code": "timeout", "message": "LLM request timed out"}


def test_llm_client_returns_auth_error_payload():
    client = SafeLLMClient(UpstreamLLMClient(mode="auth"))

    result = client.ask("hello")

    assert result == {"ok": False, "code": "auth", "message": "LLM authentication failed"}


def test_llm_client_passes_through_success_response():
    client = SafeLLMClient(UpstreamLLMClient(mode="success"))

    result = client.ask("hello")

    assert result == {"ok": True, "answer": "ok:hello"}
