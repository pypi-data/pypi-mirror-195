from app.utils.env import get_env_variable, set_env_variable

KEY_VARIABLE = "OPENAI_API_KEY"

def save_key(key):
    set_env_variable(KEY_VARIABLE, key)

def load_key():
    return get_env_variable(KEY_VARIABLE)