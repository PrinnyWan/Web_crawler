from http import cookiejar
from urllib import request, error
from urllib.parse import urlparse


class HtmlDownLoader(object):
    def download(self, url, retry_count=3, headers=None, proxy=None, data=None):
        if url is None:
            return None
        try:
            req = request.Request(url, headers=headers, data=data)
            cookie = cookiejar.CookieJar()
            cookie_process = request.HTTPCookieProcessor(cookie)
            opener = request.build_opener()
            if proxy:
                proxies = {urlparse(url).scheme: proxy}
                opener.add_handler(request.ProxyHandler(proxies))
            content = opener.open(req).read()
        except error.URLError as e:
            print('HtmlDownLoader download error:', e.reason)
            content = None
            if retry_count > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    ##HTTPError and HTTP CODE is 5XX, download again
                    return self.download(url, retry_count-1, headers, proxy, data)
        return content