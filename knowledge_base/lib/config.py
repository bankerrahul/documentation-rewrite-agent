import os
from dataclasses import dataclass, field
from typing import Optional

from dotenv import load_dotenv


@dataclass
class AgentConfig:
    """Centralized configuration for the documentation agent."""

    provider: str = "auto"
    api_key: str = ""
    model: Optional[str] = None
    knowledge_base_dir: str = ""
    output_base_dir: str = ""

    # WordPress (browser-based auth — no app password needed)
    wp_url: str = ""
    wp_username: str = ""
    wp_password: str = ""
    wp_headless: bool = True  # Set False to see the browser (needed for 2FA)

    # Batch processing
    batch_delay_seconds: float = 2.0
    max_retries: int = 3

    @classmethod
    def from_env(cls, dotenv_path: Optional[str] = None) -> "AgentConfig":
        """Load configuration from environment variables (.env file)."""
        if dotenv_path:
            load_dotenv(dotenv_path)
        else:
            load_dotenv()

        # Auto-detect provider
        provider = os.getenv("LLM_PROVIDER", "auto")
        api_key = ""
        if provider == "auto":
            if os.getenv("ANTHROPIC_API_KEY"):
                provider = "anthropic"
                api_key = os.getenv("ANTHROPIC_API_KEY", "")
            elif os.getenv("OPENAI_API_KEY"):
                provider = "openai"
                api_key = os.getenv("OPENAI_API_KEY", "")
            else:
                provider = "ollama"
        elif provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY", "")
        elif provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY", "")

        # Knowledge base directory defaults to the parent of lib/
        default_kb = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        return cls(
            provider=provider,
            api_key=api_key,
            model=os.getenv("LLM_MODEL"),
            knowledge_base_dir=os.getenv("KNOWLEDGE_BASE_DIR", default_kb),
            output_base_dir=os.getenv("OUTPUT_BASE_DIR", os.path.join(default_kb, "output")),
            wp_url=os.getenv("WP_URL", ""),
            wp_username=os.getenv("WP_USERNAME", ""),
            wp_password=os.getenv("WP_PASSWORD", ""),
            wp_headless=os.getenv("WP_HEADLESS", "true").lower() != "false",
            batch_delay_seconds=float(os.getenv("BATCH_DELAY_SECONDS", "2.0")),
            max_retries=int(os.getenv("MAX_RETRIES", "3")),
        )
