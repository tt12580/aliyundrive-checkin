import os
import re
import argparse
from aliyundrive import Aliyundrive
from message_send import MessageSend
import configparser


def main():
    # 创建一个 ConfigParser 对象
    config = configparser.ConfigParser()
    # 读取配置文件
    config.read('config.ini')

    token_string = config.get("Token", "REFRESH_TOKEN_LIST")
    pushplus_token = config.get("Token", "PUSHPLUS_TOKEN")
    serverChan_sendkey = config.get("Token", "SCKEY")
    weCom_tokens = config.get("Token", "WECOM_TOKENS")
    weCom_webhook = config.get("Token", "WECOM_WEBHOOK")
    bark_deviceKey = config.get("Token", "BARK_DEVICEKEY")
    feishu_deviceKey = config.get("Token", "FEISHU_DEVICEKEY")
    bark_private_url = config.get("Token", "BARK_PRIVATE_URL")

    message_tokens = {
        'pushplus_token': pushplus_token,
        'serverChan_token': serverChan_sendkey,
        'weCom_tokens': weCom_tokens,
        'weCom_webhook': weCom_webhook,
        'bark_deviceKey': bark_deviceKey,
        'feishu_deviceKey': feishu_deviceKey,
        'bark_private_url': bark_private_url
    }

    token_string = token_string.split(',')
    ali = Aliyundrive()
    message_all = []

    for idx, token in enumerate(token_string):
        result = ali.aliyundrive_check_in(token)
        message_all.append(str(result))

        if idx < len(token_string) - 1:
            message_all.append('--')

    title = '阿里云盘签到结果'
    message_all = '\n'.join(message_all)
    message_all = re.sub('\n+', '\n', message_all).rstrip('\n')

    message_send = MessageSend()
    message_send.send_all(message_tokens, title, message_all)

    print('finish')


if __name__ == '__main__':
    main()
