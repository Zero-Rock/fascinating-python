import json
import time
import hmac
import hashlib
import base64
import urllib.parse
from requests import post


class DDGroupRobot:

    @staticmethod
    def sign(secret: str) -> dict:
        """
        生成签名
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
        判断是否atAll
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
        整合钉钉消息
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
        检查签名时间和当前时间
        :return:
        """
        if self.secret is not None:
            current_time = round(time.time() * 1000)
            # 签名时间戳与请求调用时间误差不能超过1小时，为保险起见，相差大于50min时，更新签名
            if (current_time - int(self.tokenDir.get('timestamp'))) > 3000000:
                self.tokenDir.update(DDGroupRobot.sign(self.secret))

    def send_msg(self, body: dict) -> dict:
        """
        发送消息，返回请求结果
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
        初始化钉钉机器人
        :param url: str 请求地址
        :param access_token: token
        :param secret: 签名
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
