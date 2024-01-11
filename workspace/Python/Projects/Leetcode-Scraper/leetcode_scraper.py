from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd
import xlsxwriter


root_url = "https://leetcode.com"


def generate_report(data: list, path: str, header: list = None):
    row_counter = 0
    max_col_width = {i: 0 for i, _ in enumerate(data[0].keys())}

    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()

    difficulty_color = {"easy": "#C9E4AA", "medium": "#FAEDAA", "hard": "#FFADAA"}

    if header is not None or len(header) != 0:
        col_counter = 0
        formatting = workbook.add_format()
        for value in header:
            max_col_width[col_counter] = max(
                max_col_width[col_counter], len(str(value))
            )
            formatting.set_bold()
            formatting.set_align("vcenter")
            formatting.set_align("center")
            worksheet.write(row_counter, col_counter, value, formatting)
            col_counter += 1
        row_counter += 1

    for row in data:
        col_counter = 0
        for _, value in row.items():
            max_col_width[col_counter] = max(
                max_col_width[col_counter], len(str(value))
            )
            formatting = workbook.add_format({"text_wrap": True})
            if str(value).lower() in ["easy", "medium", "hard"]:
                formatting.set_bold()
                formatting.set_align("vcenter")
                formatting.set_align("center")
                formatting.set_bg_color(difficulty_color[str(value).lower()])
            worksheet.write(row_counter, col_counter, value, formatting)
            col_counter += 1
        row_counter += 1

    for k, v in max_col_width.items():
        worksheet.set_column(k, k, v + 2)

    workbook.close()


def close_browser(browser):
    browser.close()


def open_url_in_browser(site_url: str):
    chrome_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    chrome_driver.get(site_url)
    time.sleep(2)
    return chrome_driver


def get_data(site_url: str):
    ques_list = []

    browser = open_url_in_browser(site_url)
    page_source = browser.page_source
    WebDriverWait(browser, 10).until(EC.title_contains("LeetCode"))
    soup = BeautifulSoup(page_source, "html.parser")

    if browser.title == "Array - LeetCode":
        close_browser(browser=browser)

        for row in soup.find("tbody", {"class": "reactable-data"}).find_all("tr"):
            ques_dict = {}
            cells = row.find_all("td")
            ques_no = int(cells[1].get_text())
            ques_name = cells[2].get_text()
            ques_url = f"""{root_url}{cells[2].find("div").find("a")["href"]}"""
            difficulty = cells[4].get_text()

            ques_dict = {
                "q_no": ques_no,
                "q_name": ques_name,
                "q_url": ques_url,
                "q_dif": difficulty,
            }

            ques_list.append(ques_dict)
    print(ques_list)
    return ques_list


def main():
    # URL of the website to scrape
    url = "https://leetcode.com/tag/array/"
    question_list = get_data(url)
    generate_report(
        question_list,
        path="leetcode_report.xlsx",
        header=["Question Number", "Question", "Question URL", "Difficulty"],
    )
    # Send an HTTP GET request to the website


if __name__ == "__main__":
    main()
