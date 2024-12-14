import os
from dotenv import load_dotenv
from src.utils.utility import Utility

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
                Utility.print_yellow("DB_CONFIG variable not defined")
                return None
            if var_name == "ENV_APP":
                Utility.print_yellow("ENV_APP variable not defined")
                return None
            if var_name == "SEED_DB":
                Utility.print_yellow("SEED_DB variable not defined. Seeding is set to False")
                return False
            raise RuntimeError(f"\033[91mThe environment variable '{var_name}' is not set")
        return value
