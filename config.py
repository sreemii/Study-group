from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "your_secret_key_here"  # 🔑 Replace with a strong secret key
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60  # ⏳ Token expiry time (adjust as needed)
    ALGORITHM: str = "HS256"  # 🔐 JWT Signing Algorithm

    class Config:
        env_file = ".env"  # (Optional) Load settings from a .env file

#Create an instance of Settings to use in your app
settings = Settings()
