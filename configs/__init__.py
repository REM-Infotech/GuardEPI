import os
from dotenv import load_dotenv
load_dotenv()
import json

def debugmode() -> bool:

    debug = os.getenv("DEBUG", "False").lower() in (
        "true", "1", "t", "y", "yes")
    return debug


def csp() -> dict[str]:

    csp_vars = json.load(os.path.join(os.getcwd(), "configs", "csp.json"))
    return csp_vars
