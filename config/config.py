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
            if var_name == "DB_CONFIG":
                print("\033[91mDB_CONFIG variable not defined\033[0m")
                return None
            if var_name == "ENV_APP":
                print("\033[91mENV_APP variable not defined\033[0m")
                return None
            raise RuntimeError(f"\033[91mThe environment variable '{var_name}' is not set\033[0m")
        return value
