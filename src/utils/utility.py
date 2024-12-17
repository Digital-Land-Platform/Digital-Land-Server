import random
import string


class Utility:

    async def generate_transaction_number(length=12) -> str:
        """Generate a transaction number with random letters and digits."""
        characters = string.ascii_letters + string.digits
        transaction_number = ''.join(random.choice(characters) for _ in range(length))
        return transaction_number

    @staticmethod
    def print_yellow(text: str):
        print(f"\033[93m{text}\033[0m")

    @staticmethod
    def print_green(text: str):
        print(f"\033[92m{text}\033[0m")

    @staticmethod
    def print_red(text: str):
        print(f"\033[91m{text}\033[0m")
