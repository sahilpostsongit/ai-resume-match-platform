from pathlib import Path
from pydantic import BaseModel


class Settings(BaseModel):
    model_config = {"protected_namespaces": ()}
    database_url: str = f"sqlite:///{Path(__file__).resolve().parent.parent / 'resume.db'}"
    model_cache_path: Path = Path(__file__).resolve().parent.parent / "model_cache.joblib"


settings = Settings()





