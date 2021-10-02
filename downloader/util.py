import os


def get_secret_value(env_var: str, file_path: str) -> str:
    if env_val := os.getenv(env_var):
        return env_val.strip()

    with open(file_path) as fp:
        return fp.read().strip()
