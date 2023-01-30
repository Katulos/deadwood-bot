from threading import local

from app.config import Settings


class Shared(local):
    settings = Settings()


shared = Shared()
