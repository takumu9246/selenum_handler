from selenium_handler import SeleniumHandler
from selenium.webdriver.common.by import By


def main():
    with SeleniumHandler(driver_pass="./chromedriver.exe", window_max=True, headless=True) as handler:
        handler.open_url("https://google.com/")
        text = handler.get_text(By.CLASS_NAME, "gb_q")
    print(text)


if __name__ == "__main__":
    main()
