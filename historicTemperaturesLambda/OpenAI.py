import os
import requests
import json
from logger_config import logger

class OpenAI():
    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(
                os.environ.get('OPENAI_API_KEY')
            )
        }
        self.base_url = 'https://api.openai.com/v1/'
    
    def get_request(self, url):
        total_url = self.base_url + url
        logger.info(f"GET Request URL: {total_url}")
        res = requests.get(total_url, headers=self.headers)
        res_json = res.json()
        logger.info(f"RESPONSE: {res}, statusCode: {res.status_code}, json: {json.dumps(res_json)}")
        return res_json

    def post_request(self, url, data=None):
        total_url = self.base_url + url
        logger.info(f"POST Request URL: {total_url}")
        res = requests.post(total_url, headers=self.headers, json=data)
        res_json = res.json()
        logger.info(f"RESPONSE: {res}, statusCode: {res.status_code}, json: {json.dumps(res_json)}")
        return res_json

    def create_completion(
        self,
        model,
        prompt=None,
        suffix=None,
        max_tokens=None,
        temperature=None,
        top_p=None,
        n=1,
        stream=None,
        logprobs=None,
        echo=None,
        stop=None,
        presence_penalty=None,
        frequency_penalty=None,
        best_of=None,
        logit_bias=None,
        user=None
    ):
        url = 'completions'
        data = {
            'model': model,
            'prompt': prompt,
            # 'suffix': suffix,
            'max_tokens': max_tokens,
            # 'temperature': temperature,
            # 'top_p': top_p,
            # 'n': n,
            # 'stream': stream,
            # 'logprobs': logprobs,
            # 'echo': echo,
            # 'stop': stop,
            # 'presence_penalty': presence_penalty,
            # 'frequency_penalty': frequency_penalty,
            # 'best_of': best_of,
            # 'logit_bias': logit_bias,
            # 'user': user
        }
        return self.post_request(url, data=data)
    
    def create_chat_completion(self, prompt_messages):
        url = 'chat/completions'
        body = {
            "model": "gpt-3.5-turbo",
            "messages": prompt_messages,
            "temperature": 0.5,
            "user": 'user'
        }
        return self.post_request(url, data=body)

