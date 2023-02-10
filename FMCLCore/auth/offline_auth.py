# coding:utf-8
"""
    离线登陆
"""
import uuid
import base64


# Auth(Offline)
def auth(player_name: str) -> dict:
    """
        通过离线玩家名生成玩家信息
        :param player_name: 玩家名
        :return: 玩家信息
    """
    return {
        "username": player_name,
        "uuid": uuid.uuid4().hex,
        "access_token": base64.b64encode(("{\"name\": \"" + player_name + "\"}").encode()).decode()
    }
