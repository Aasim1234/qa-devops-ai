"""Answer generation through Ollama (local) or an OpenAI-compatible API (cloud).

Every failure is raised as LLMUnavailable with a readable message; nothing in
here can take the FastAPI process down.
"""
import logging
import threading
import time

import requests

from .config import Settings

log = logging.getLogger("qa_devops_ai.llm")


class LLMUnavailable(Exception):
    """The configured LLM backend could not produce an answer."""


def build_prompt(question: str, contexts: list[str]) -> str:
    context_text = "\n\n---\n\n".join(contexts)

    return f"""
You are a real-time DevOps and QA interview assistant.

Answer the interviewer's question directly.

IMPORTANT RULES:
- Be concise and natural.
- Do not think aloud.
- Do not explain your reasoning process.
- Do not repeat the question.
- For simple definitions: 1-3 sentences.
- For technical questions: give the key answer first, then important details.
- For troubleshooting scenarios: give a clear step-by-step approach.
- Mention commands when they are genuinely useful.
- Do not invent personal experience, metrics, companies, projects, or results.
- Use the supplied knowledge when relevant.
- If the supplied knowledge is insufficient, use reliable general DevOps knowledge.
- Do not dump the entire knowledge base into the answer.
- Sound like a candidate answering an interviewer, not like a textbook.

Knowledge context:
{context_text}

Interview question:
{question}

Answer:
"""


class LLMClient:
    PROBE_TTL_SECONDS = 15
    PROBE_TIMEOUT_SECONDS = 1.5

    def __init__(self, settings: Settings):
        self._s = settings
        self._probe_lock = threading.Lock()
        self._probe_value: bool | None = None
        self._probe_at = 0.0

    @property
    def provider(self) -> str:
        return self._s.llm_provider

    @property
    def model(self) -> str:
        if self.provider == "ollama":
            return self._s.ollama_model
        if self.provider == "openai":
            return self._s.llm_model
        return ""

    # ------------------------------------------------------------------
    # Status (cheap; used by /health and /status)
    # ------------------------------------------------------------------
    def available(self) -> bool:
        """Best-effort availability check that never raises and never blocks long."""
        if self.provider == "openai":
            return bool(self._s.llm_api_key and self._s.llm_model)
        if self.provider != "ollama":
            return False

        now = time.monotonic()
        if self._probe_value is not None and now - self._probe_at < self.PROBE_TTL_SECONDS:
            return self._probe_value

        # Don't stack up probes; whoever loses the race uses the last value.
        if not self._probe_lock.acquire(blocking=False):
            return bool(self._probe_value)
        try:
            try:
                r = requests.get(
                    f"{self._s.ollama_base_url}/api/tags",
                    timeout=self.PROBE_TIMEOUT_SECONDS,
                )
                self._probe_value = r.ok
            except requests.RequestException:
                self._probe_value = False
            self._probe_at = time.monotonic()
            return self._probe_value
        finally:
            self._probe_lock.release()

    def status(self) -> dict:
        info = {
            "provider": self.provider,
            "model": self.model or None,
            "available": self.available(),
        }
        if self.provider == "ollama":
            info["url"] = self._s.ollama_base_url
        elif self.provider == "openai":
            info["url"] = self._s.llm_base_url
            info["api_key_set"] = bool(self._s.llm_api_key)
        return info

    # ------------------------------------------------------------------
    # Generation
    # ------------------------------------------------------------------
    def generate(self, question: str, contexts: list[str]) -> str:
        prompt = build_prompt(question, contexts)

        if self.provider == "ollama":
            answer = self._ollama(prompt)
        elif self.provider == "openai":
            answer = self._openai(prompt)
        elif self.provider == "none":
            raise LLMUnavailable("LLM generation is disabled (LLM_PROVIDER=none)")
        else:
            raise LLMUnavailable(
                f"Unknown LLM_PROVIDER '{self.provider}'. Use ollama, openai or none."
            )

        if not answer:
            raise LLMUnavailable(f"{self.provider} returned an empty answer")
        return answer

    def _post(self, name: str, url: str, **kwargs) -> dict:
        try:
            r = requests.post(url, timeout=self._s.llm_timeout, **kwargs)
        except requests.ConnectionError:
            raise LLMUnavailable(f"{name} is not reachable at {url}") from None
        except requests.Timeout:
            raise LLMUnavailable(
                f"{name} did not answer within {self._s.llm_timeout}s"
            ) from None
        except requests.RequestException as e:
            raise LLMUnavailable(f"{name} request failed: {e}") from None

        if not r.ok:
            raise LLMUnavailable(f"{name} returned HTTP {r.status_code}: {r.text[:300]}")

        try:
            return r.json()
        except ValueError:
            raise LLMUnavailable(f"{name} returned a non-JSON response") from None

    def _ollama(self, prompt: str) -> str:
        data = self._post(
            "Ollama",
            f"{self._s.ollama_base_url}/api/generate",
            json={
                "model": self._s.ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self._s.llm_temperature,
                    "num_predict": self._s.llm_max_tokens,
                },
            },
        )
        return str(data.get("response", "")).strip()

    def _openai(self, prompt: str) -> str:
        if not self._s.llm_api_key:
            raise LLMUnavailable("LLM_API_KEY is not set")
        if not self._s.llm_model:
            raise LLMUnavailable("LLM_MODEL is not set")

        data = self._post(
            "LLM API",
            f"{self._s.llm_base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self._s.llm_api_key}"},
            json={
                "model": self._s.llm_model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": self._s.llm_temperature,
                "max_tokens": self._s.llm_max_tokens,
            },
        )
        try:
            return str(data["choices"][0]["message"]["content"] or "").strip()
        except (KeyError, IndexError, TypeError):
            raise LLMUnavailable("LLM API returned an unexpected response shape") from None
