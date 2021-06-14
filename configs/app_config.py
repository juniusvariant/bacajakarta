from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_MODE: str = "Development" ##value -> Development / Production
    INET_MODE: str = "Online" ##value -> Online / Offline
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    METADATA: list = [
        {
            "name": "Auth End-Point",
            "description": "The **login** logic is here.",
        },
        {
            "name": "Utils End-Point",
            "description": "Operations with all about **Application Utility**.",
        },
        {
            "name": "Accounts End-Point",
            "description": "Operations with all about **Accounts**.",
        },
        {
            "name": "Parents End-Point",
            "description": "Operations with all about **Parents**.",
        },
        {
            "name": "Childs End-Point",
            "description": "Operations with all about **Childs**.",
        }
    
    ]