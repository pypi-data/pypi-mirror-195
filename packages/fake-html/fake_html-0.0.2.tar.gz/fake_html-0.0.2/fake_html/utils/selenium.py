import shutil
from typing import Optional
from urllib.request import getproxies

try:
    from selenium import webdriver
except ImportError:
    webdriver = None

USER_AGENT = "PixivIOSApp/7.13.3 (iOS 14.6; iPhone13,2)"
PROXIES = getproxies()


def _need_install(module):
    raise RuntimeError(f'Module {module!r} not installed. Please install with \'pip install fake_html[crawl]\'.')


def get_chromedriver() -> Optional[str]:
    executable_path = shutil.which("chromedriver")
    if executable_path is None:
        try:
            import pyderman
        except ImportError:
            _need_install('pyderman')
        else:
            executable_path = pyderman.install(verbose=False, browser=pyderman.chrome)

    return executable_path


def _get_chrome_option(headless: bool = False):
    options = webdriver.ChromeOptions()

    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

    options.add_argument("--user-agent=" + USER_AGENT)
    if "all" in PROXIES:
        options.add_argument(f"--proxy-server={PROXIES['all']}")
    elif "https" in PROXIES:
        options.add_argument(f"--proxy-server={PROXIES['https']}")
    elif "http" in PROXIES:
        options.add_argument(f"--proxy-server={PROXIES['http']}")
    else:
        options.add_argument('--proxy-server="direct://"')
        options.add_argument("--proxy-bypass-list=*")

    return options


def get_chrome(headless: bool = False) -> webdriver.Chrome:
    if not webdriver:
        _need_install('selenium')

    caps = webdriver.DesiredCapabilities.CHROME.copy()
    caps["goog:loggingPrefs"] = {
        "performance": "ALL"
    }  # enable performance logs

    return webdriver.Chrome(
        executable_path=get_chromedriver(),
        options=_get_chrome_option(headless),
        desired_capabilities=caps,
    )
