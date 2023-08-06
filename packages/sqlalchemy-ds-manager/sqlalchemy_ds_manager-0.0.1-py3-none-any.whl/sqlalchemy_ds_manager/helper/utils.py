import os
import base64

def hash(sql: str) -> str:
    token = base64.b64encode(sql.encode("ascii"))
    return token.decode("ascii")