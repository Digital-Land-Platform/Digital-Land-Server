import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Class to hold and validate the configuration."""

    @staticmethod
    def get_env_variable(var_name: str) -> str:
        """Get an environment variable or raise an error if not defined."""
        value = os.getenv(var_name)
        if value is None:
            raise RuntimeError(f"The environment variable '{var_name}' is not set")
        return value
