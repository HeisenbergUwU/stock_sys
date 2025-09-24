from model import Kronos, KronosTokenizer, KronosPredictor
from core.constaint import *

tokenizer = KronosTokenizer.from_pretrained(TOKENIZER_PATH)
model = Kronos.from_pretrained(MODEL_PATH)

predictor = KronosPredictor(model, tokenizer, device=DEVICE, max_context=CONTEXT_LEN)


