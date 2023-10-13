# coding=utf-8
import requests
from apig_sdk import signer

if __name__ == '__main__':
    sig = signer.Signer()
    sig.Key = "apigateway_sdk_demo_key"
    sig.Secret = "apigateway_sdk_demo_secret"

    r = signer.HttpRequest("POST",
                           "https://30030113-3657-4fb6-a7ef-90764239b038.apigw.exampleRegion.com/app1?a=1",
                           {"x-stage": "RELEASE"},
                           "body")
    sig.Sign(r)
    print(r.headers["X-Sdk-Date"])
    print(r.headers["Authorization"])
    resp = requests.request(r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body)
    print(resp.status_code, resp.reason)
    print(resp.content)
