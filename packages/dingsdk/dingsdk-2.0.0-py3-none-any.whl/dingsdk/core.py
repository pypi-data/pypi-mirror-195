import requests

from urllib.parse import urljoin

session = requests.session()


class DingSDKCore:
    appkey:str
    agent_id:int
    appsecret:str
    access_token:str = None
    
    def api(self, method:str, url:str, **kwargs) -> dict:
        """
        """
        kwargs['headers'] = {
            'Host': 'api.dingtalk.com',
            'Content-Type': 'application/json',
            'x-acs-dingtalk-access-token': self.access_token,
        }
        url = urljoin('https://api.dingtalk.com/', url)
        response = session.request(method, url, **kwargs)
        if response.status_code == 200: return response.json()
        raise DingSDKError(response.json())
    
    def oapi(self, method:str, url:str, **kwargs) -> dict:
        """
        """
        defaults = {**kwargs, 'params': {
            **kwargs.get('params', {}),
            'access_token': self.access_token,
        }}
        url = urljoin('https://oapi.dingtalk.com/', url)
        response = session.request(method, url, **defaults).json()
        if response.get('errcode', None) == 0: return response
        raise DingSDKError(response)


class DingSDKError(Exception):
    pass
