'''
Copyright [2023] [许灿标]
license: Apache License, Version 2.0
email: lcctoor@outlook.com
'''

import re
import openai


class Chat():
    '''
    文档: https://pypi.org/project/openai2
    
    获取api_key:
        链接1: https://platform.openai.com/account/api-keys
        链接2: https://www.baidu.com/s?wd=%E8%8E%B7%E5%8F%96%20openai%20api_key
    '''
    
    def __init__(self, api_key:str, model:str="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.messages = []
    
    def request(self, text:str):
        self.messages.append({"role": "user", "content": text})
        completion = openai.ChatCompletion.create(
            api_key = self.api_key,
            model = self.model,
            messages = self.messages
        )
        answer:str = completion.choices[0].message['content']
        self.messages.append({"role": "assistant", "content": answer})
        return re.sub('\s+', '', answer)