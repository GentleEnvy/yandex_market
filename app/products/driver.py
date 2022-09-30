from django.conf import settings
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


class Driver(WebDriver):
    def __init__(
        self, port=0, service_args=None,
        desired_capabilities=None, service_log_path=None, chrome_options=None,
        keep_alive=True
    ) -> None:
        options = Options()
        options.headless = True
        options.binary_location = settings.PATH_TO_GOOGLE_CHROME
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('get_trade_ids-maximized')
        options.add_argument('disable-infobars')
        executable_path = settings.PATH_TO_CHROMEDRIVER
        super().__init__(
            executable_path, port, options, service_args, desired_capabilities,
            service_log_path, chrome_options, keep_alive
        )
