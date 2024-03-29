import json
from selenium import webdriver
import pickle
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By


def get_funk():
    ua = UserAgent()

    url = 'https://market.yandex.ru/catalog--ruli-dzhoistiki-geimpady/26908330/list?srnum=672&was_redir=1&rt=9&rs=eJwzEglgrGLheHucdRYjZ0ppYk5xal5xKgBJFwc_&text=dualsense&hid=91117&allowCollapsing=1&local-offers-first=0&pricefrom=3500&priceto=7200&glfilter=7893318%3A152955'

    options = webdriver.ChromeOptions()
    options.add_argument(f'User-Agent= {ua.random}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.headless = True

    driver = webdriver.Chrome(r'C:\Users\madma\PycharmProjects\Parser_ya-market_dyalsense\parser\chromedriver.exe', \
                              options=options)

    try:
        driver.get(url)
        driver.implicitly_wait(5)

        for cookie in pickle.load(open('session', 'rb')):
            driver.add_cookie(cookie)
        driver.get(url)
        print(driver.window_handles)
        driver.implicitly_wait(5)

        result_data = []
        gamepads = driver.find_elements(By.XPATH, "//img[@data-tid='80e17da7']")
        for gamepad in gamepads:
            gamepad.click()
            driver.implicitly_wait(5)
            driver.switch_to.window(driver.window_handles[1])
            driver.implicitly_wait(5)
            link = driver.current_url
            name_gamepad = driver.find_element(By.XPATH, "//h1[@data-tid='723082e']")
            print(name_gamepad.text)
            price = driver.find_elements(By.XPATH, "//span[@data-auto='mainPrice']")
            print(price[1].text)
            data = (
                {
                    'link': link,
                    'name_gamepad': name_gamepad.text,
                    'price': price[1].text
                }
            )

            result_data.append(data)

            driver.close()

            driver.switch_to.window(driver.window_handles[0])
            driver.implicitly_wait(5)

        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(result_data, file, indent=4, ensure_ascii=False)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def main():
    get_funk()


if __name__ == '__main__':
    main()
