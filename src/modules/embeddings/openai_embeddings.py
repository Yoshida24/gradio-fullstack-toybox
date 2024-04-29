from openai import OpenAI
import tiktoken
import dotenv


dotenv.load_dotenv()

client = OpenAI()

DEFAULT_MODEL = "text-embedding-3-small"
MAX_TOKEN = 8192


def check_token(text: str, model=DEFAULT_MODEL) -> int:
    encoding_model = tiktoken.encoding_name_for_model(model)
    enc = tiktoken.get_encoding(encoding_model)
    tokens = len(enc.encode(text))

    return tokens


def embeddings(text: str, model=DEFAULT_MODEL) -> list[float] | None:
    if check_token(text, model) > MAX_TOKEN:
        return None

    embedding = client.embeddings.create(input=text, model=model).data[0].embedding
    return embedding
