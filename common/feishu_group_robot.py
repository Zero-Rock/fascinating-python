"""
@Author : Zero
@Time   : 2021/7/23 21:57:31
"""
import json
import time
import hmac
import hashlib
import base64
import urllib.parse


class FeishuGroupRobot:
    @staticmethod
    def sign(secret: str) -> dict:
        """
        generate signature
        :param secret:
        :return:
        """

        timestamp = str(round(time.time() * 1000))
        print(timestamp)
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(code))
        return {"sign": sign, "timestamp": timestamp}

    def __init__(self):
        pass


if __name__ == '__main__':
    print(FeishuGroupRobot.sign('hKDCAlK0dzofp8SRo4BaGe'))
