from functools import lru_cache
from threading import Lock

from .selenium import _need_install, get_chrome


@lru_cache()
def _chrome_with_cache():
    return get_chrome(headless=True)


_CHROME_LOCK = Lock()


def get_page_html(url: str, *args, render: bool = True, **kwargs):
    if render:
        with _CHROME_LOCK:
            chrome = _chrome_with_cache()
            chrome.get(url)
            return chrome.page_source
    else:
        try:
            import requests
        except ImportError:
            _need_install('requests')
        else:
            resp = requests.get(url, *args, **kwargs)
            resp.raise_for_status()
            return resp.text
