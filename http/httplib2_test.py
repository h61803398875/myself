# -*- coding:utf8 -*-

import httplib2

# h = httplib2.Http()
# url = "https://accounts.google.com/o/oauth2/auth?scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fspreadsheets.readonly&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&response_type=code&client_id=340200921793-s3gk7fbo4o8g3qunmvnlgmvesqrg7glt.apps.googleusercontent.com&access_type=offline"
# resp, content = h.request(url, "GET")
# print resp
# print content

h = httplib2.Http(
    proxy_info=httplib2.ProxyInfo(httplib2.socks.PROXY_TYPE_HTTP, 'dev-proxy.oa.com', 8080, proxy_user="chazzhuang",
                                  proxy_pass="Tencent201611"))
# url = 'https://www.googleapis.com/auth/spreadsheets.readonly'
url = "https://accounts.google.com/o/oauth2/auth?scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fspreadsheets.readonly&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&response_type=code&client_id=340200921793-s3gk7fbo4o8g3qunmvnlgmvesqrg7glt.apps.googleusercontent.com&access_type=offline"
resp, content = h.request(url, "GET")
print (content)
