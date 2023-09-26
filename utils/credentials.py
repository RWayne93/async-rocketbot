import os

def load_env(filename='.env'):
    with open(filename) as f:
        for line in f:
            if line.strip():
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
    return os.environ