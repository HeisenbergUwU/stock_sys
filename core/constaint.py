from dotenv import load_dotenv
import os

load_dotenv()
CONTEXT_LEN = 512
MODEL_PATH = os.getenv("MODEL_PATH")
TOKENIZER_PATH = os.getenv("TOKENIZE_PATH")
DEVICE = os.getenv("DEVICE")
USE_SQL = False  # for debug
