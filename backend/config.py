"""Central configuration for V-AgentWar.

All secrets are read from environment variables. Safe defaults keep the
backend runnable without external AI/security services.
"""
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "V-AgentWar"
    app_env: str = "development"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    frontend_origin: str = "http://localhost:3000"

    database_url: str = "sqlite:///./data/agentwar.db"

    vcore_max_rounds: int = 10
    vcore_event_history: int = 200
    vcore_safe_mode: bool = True

    llm_enabled: bool = False
    llm_provider: str = "groq"
    llm_model: str = ""
    llm_api_key: str = ""

    rag_enabled: bool = True
    rag_knowledge_dir: str = "../knowledge"
    rag_top_k: int = 4

    mcp_enabled: bool = True
    mcp_server_name: str = "v-agentwar-mcp"
    mcp_audit_enabled: bool = True

    cyber_range_enabled: bool = False
    cyber_range_network: str = "v_agentwar_range"
    cyber_range_target_url: str = "http://target:3000"
    allow_external_targets: bool = False

    suricata_enabled: bool = False
    suricata_eve_path: str = ""
    zeek_enabled: bool = False
    zeek_log_dir: str = ""
    wazuh_enabled: bool = False
    wazuh_api_url: str = ""
    wazuh_api_user: str = ""
    wazuh_api_password: str = ""

    @property
    def data_dir(self) -> Path:
        path = Path(__file__).resolve().parent / "data"
        path.mkdir(parents=True, exist_ok=True)
        return path


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
