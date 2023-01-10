from urllib.parse import urlsplit, urlunsplit, urljoin

def cleanUrl(url):
    url = urlsplit(url)
    url = url.scheme+'://'+url.netloc+url.path
    return url