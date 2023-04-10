from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pyautogui
import logging
import traceback
from typing import Union

logger = logging.getLogger(__name__)


class SeleniumHandler():
    def __init__(self, driver_pass: str, wait_time: int = 10, headless: bool = False, window_max: bool = False, log_view: bool = False) -> None:
        options = Options()
        # optionsでdriverの設定
        options.add_argument('--headless') if headless else None
        options.add_experimental_option(
            'excludeSwitches', ['enable-logging']) if not log_view else None
        options.add_argument('--ignore-certificate-errors')
        # --start-maximizedというウィンドウを最大化するoptionがあるが、headlessにした際に機能しないことがあるので--window-sizeで最大値を指定する
        if window_max:
            width, height = pyautogui.size()
            options.add_argument(f'--window-size={width},{height}')
        self._driver = webdriver.Chrome(
            executable_path=driver_pass, options=options)
        # 待機時間の設定,wait_time秒以上経つとエラーになる
        self._wait = WebDriverWait(self._driver, wait_time)

    def _wait_element(self, by: By, value: str):
        self._wait.until(EC.presence_of_element_located((by, value)))

    def open_url(self, url: str):
        self._driver.get(url)

    def switch_to_frame(self, by: By, value: Union[str, None] = None):
        if value is None:
            self._driver.switch_to.frame(value)
        else:
            self._wait_element(by, value)
            self._driver.switch_to.frame(
                self._driver.find_element(by, value))

    def switch_to_default_frame(self):
        self._driver.switch_to.default_content()

    def get_text(self, by: By, value: str):
        self._wait_element(by, value)
        return self._driver.find_element(by, value).text

    def click(self, by: By, value: str):
        self._wait_element(by, value)
        self._driver.find_element(by, value).click()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._driver.close()
        if exc_type is not None:
            logger.error("Type: %s", exc_type)
            logger.error("Value: %s", exc_val)
            logger.error("Traceback: %s", traceback.format_tb(exc_tb))
