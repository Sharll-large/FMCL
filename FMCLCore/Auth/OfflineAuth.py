import uuid
import base64

def Auth(playername: str):
    return {
        "username": playername,
        "uuid": uuid.uuid4().hex,
        "access_token": base64.b64encode(("{\"name\": \"" + playername + "\"}").encode()).decode()
    }
