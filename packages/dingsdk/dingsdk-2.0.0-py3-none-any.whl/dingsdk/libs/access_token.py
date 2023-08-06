from dingsdk.core import DingSDKCore


class AccessToken(DingSDKCore):
    
    def get_token(self) -> str:
        """获取企业内部应用的 AccessToken
        """
        pms = {'appkey':self.appkey, 'appsecret':self.appsecret}
        kws = {'method': 'GET', 'url': 'gettoken', 'params': pms}
        return super().oapi(**kws).get('access_token', '')
    