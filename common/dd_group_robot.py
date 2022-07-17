import base64
import hashlib
import hmac
import json
import time
import urllib.parse

from requests import post


class DDGroupRobot:

    @staticmethod
    def sign(secret: str) -> dict:
        """
        generate signature
        :param secret:
        :return:
        """
        timestamp = str(round(time.time() * 1000))
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(code))
        return {"sign": sign, "timestamp": timestamp}

    @staticmethod
    def gen_at(at_mobiles: list = None) -> dict:
        """
        judge whether atAll
        :param at_mobiles:
        :return:
        """
        at = dict()
        if at_mobiles is None:
            at['isAtAll'] = False
        else:
            if not isinstance(at_mobiles, list):
                at_mobiles = []
            at['isAtAll'] = len(at_mobiles) == 0
            if len(at_mobiles) != 0:
                at['atMobiles'] = at_mobiles
        return at

    @staticmethod
    def gen_msg(msg_type: str, data: dict, at_mobiles: list = None) -> dict:
        """
        integrate DingTalk news
        :param msg_type:
        :param data:
        :param at_mobiles:
        :see https://developers.dingtalk.com/document/app/custom-robot-access/title-72m-8ag-pqw
        :return:
        """

        body = {
            'msgtype': msg_type,
            'at': DDGroupRobot.gen_at(at_mobiles),
        }
        body.update({msg_type: data})
        return body

    def check_sign(self):
        """
        check signature time and current time
        :return:
        """
        if self.secret is not None:
            current_time = round(time.time() * 1000)
            # The difference between the signature timestamp and the request call time cannot exceed 1 hour
            # To be safe, update the signature when the difference is greater than 50 min
            if (current_time - int(self.tokenDir.get('timestamp'))) > 3000000:
                self.tokenDir.update(DDGroupRobot.sign(self.secret))

    def send_msg(self, body: dict) -> dict:
        """
        send a message and return the request result
        :param body:
        :return:
        """
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json"
        }
        self.check_sign()
        resp = post(url=self.url, json=body, headers=headers, params=self.tokenDir)
        return json.loads(resp.text)

    def __init__(self, url: str, access_token: str, secret: str = None):
        """
        initialize DingTalk Robot
        :param url: str request url
        :param access_token: token
        :param secret: signature
        """
        self.url = url
        self.secret = secret
        self.tokenDir = {
            'access_token': access_token
        }
        if secret is not None:
            self.tokenDir.update(DDGroupRobot.sign(secret))
        else:
            print('No signature, please confirm whether to set the IP address or custom keywords')
