# -*- encoding: utf-8 -*-
"""
@File: auto_grab.py
@Description: 自动填写问卷
@Author: Ray
@Time: 2025/05/21 14:05:16
"""


import time
from datetime import datetime

import ntplib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service


class NTPTime:
    def __init__(self):
        self.ntp_url_pools = [
            "pool.ntp.org",
            "cn.pool.ntp.org",
            "ntp.ntsc.ac.cn",
        ]
        self.ntp_client = ntplib.NTPClient()

    def get_network_time(self):
        ntp_t = None
        for ntp_url in self.ntp_url_pools:
            try:
                response = self.ntp_client.request(ntp_url)
                ntp_t = datetime.fromtimestamp(response.tx_time)
                print(f"{ntp_url} response, {response.delay}")
                break
            except ntplib.NTPException:
                print(f"{ntp_url} not response")
                continue
        return ntp_t

    def sleep_until_specified_time(self, time_h_m_s_f, time_date=None):
        """
        time_h_m_s_f: hh:mm:ss.f
        time_data: yyyy-mm-dd  default: now date
        """
        if time_date is None:
            specified_time = datetime.strptime(
                f"{datetime.now().strftime('%Y-%m-%d')} {time_h_m_s_f}", "%Y-%m-%d %H:%M:%S.%f"
            )
        else:
            specified_time = datetime.strptime(f"{time_date} {time_h_m_s_f}", "%Y-%m-%d %H:%M:%S.%f")

        print(f"""设置时间: {specified_time.strftime("%Y-%m-%d %H:%M:%S.%f")}""")

        ntp_t = self.get_network_time()
        assert ntp_t is not None

        if ntp_t is not None and ntp_t < specified_time:
            time_to_sleep = (specified_time - ntp_t).total_seconds()
            print(f"sleep: {time_to_sleep}s")
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)


docs_qq_web = {
    "module": ".question-main-content",  # 问题模块class
    "title": ".question-title",  # 问题标题class
    "content": ".question-content",  # 内容
    "text": "textarea",  # 内容填写class
    "select": ".form-select",
    "commit": ".question-commit",
}

college_info = "某某学院"
name_info = "某某某"
Student_ID_info = "1234567890"
contact_info = "12345678900"
grade_info = "研二"
class_info = "xxx"
self_info = [
    [name_info, "姓名|名字"],
    ["某某大学", "院校"],
    [Student_ID_info, "学号|职工号"],
    ["xxx@xx.com", "邮箱"],
    [college_info, "学院|院系|单位"],
    [grade_info, "年级"],
    [class_info, "班级"],
    ["xxx", "专业"],
    [contact_info, "联系方式|电话|手机|手机号"],
    ["xxx", "QQ|qq"],
    [contact_info, "微信"],
    ["无", "其他|其它|备注"],
    ["无", "收件地址"],
]
self_info = {k: v for v, ks in self_info for k in ks.split("|")}


def find_answer(title):
    if title in self_info:
        return self_info[title]
    else:
        for k in self_info:
            if k in title or title in k:
                return self_info[k]


def get_driver() -> webdriver:
    # 实例化一个option对象
    options = webdriver.EdgeOptions()

    # 隐藏chrome浏览器的窗口（该步骤可忽略）
    # options.add_argument('headless')
    # 无痕模式
    options.add_argument("--incognito")
    # 去掉 webdriver 痕迹
    options.add_argument("disable-blink-features=AutomationControlled")

    # 关闭一些无用的输出（主要是该步骤）
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    service = Service(executable_path="./msedgedriver.exe")
    driver = webdriver.Edge(service=service, options=options)

    return driver


def fillQuestions(inputField, title):
    info = find_answer(title)
    inputField.clear()
    inputField.send_keys(info)


def fillSelect(driver, selectField, title):
    info = find_answer(title)
    selectField.click()
    time.sleep(0.1)
    option = driver.find_elements(By.XPATH, f"//*[.//*[contains(text(), '{info}')] and @role='option']")
    if option:
        option[0].click()
    else:
        option = driver.find_elements(By.XPATH, f"//*[@role='option']")
        if option:
            option[0].click()


def grab(driver, url=None):
    if url is None:
        driver.refresh()
    else:
        driver.get(url)

    questions = driver.find_elements(By.CSS_SELECTOR, f"{docs_qq_web['module']}")
    for q in questions:
        title = q.find_element(By.CSS_SELECTOR, f"{docs_qq_web['title']}").text.strip()
        content = q.find_element(By.CSS_SELECTOR, f"{docs_qq_web['content']}")
        inputField = content.find_elements(By.CSS_SELECTOR, f"{docs_qq_web['text']}")
        if inputField:
            fillQuestions(inputField[0], title)
            pass
        else:
            selectField = content.find_elements(By.CSS_SELECTOR, f"{docs_qq_web['select']}")
            if selectField:
                fillSelect(driver, selectField[0], title)
        q.click()
    time.sleep(0.1)
    commit = driver.find_element(By.CSS_SELECTOR, f"{docs_qq_web['commit']}")
    commit.click()
    driver.find_element(By.XPATH, "//button[.//*[contains(text(), '确认')]]").click()


def login(driver):
    driver.find_element(By.XPATH, "//button[.//*[contains(text(), '登录')]]").click()
    time.sleep(1)
    driver.find_element(
        By.XPATH,
        "//*[contains(text(), 'QQ登录')][not(string-length(text()) > string-length(//*[contains(text(), 'QQ登录')][1]/text()))]",
    ).click()
    t = driver.find_elements(By.XPATH, "//div[contains(text(), '服务协议和隐私政策')]")
    if len(t) > 0:
        t = t[0]
        t.find_element(By.XPATH, "..//button[contains(div/text(), '同意')]").click()


if __name__ == "__main__":
    try:
        driver = get_driver()
        driver.get("https://docs.qq.com")
        time.sleep(1)
        login(driver)
        print("请登录")
        url = input("输入问卷网址 > ")
        driver.get(url)

        time.sleep(1)
        t = driver.find_elements(
            By.CSS_SELECTOR, "div.detail-page-bottom-client-modal-module_modal-close__ak1Qy"
        )
        if len(t) > 0:
            print("关闭")
            t[0].click()

        t = input("请输入设定时间 hh:mm:ss.f > ")
        ntp = NTPTime()
        ntp.sleep_until_specified_time(time_h_m_s_f=t)
        try:
            grab(driver)
        except:
            time.sleep(0.1)
            grab(driver)
        print("finish!")
        time.sleep(10)
        driver.quit()
        print("quit")
    except KeyboardInterrupt as e:
        print("KeyboardInterrupt")
