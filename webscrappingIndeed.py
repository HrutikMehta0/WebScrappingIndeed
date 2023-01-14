import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service  # Used to set Chrome location
from selenium.webdriver.chrome.options import Options  # Used to add aditional settings (ex. run in background)
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',}
url = 'https://ca.indeed.com/jobs?q=Data+Scientist&l=Toronto&start=0'


def scrape_job_details(url):
    resp = requests.get(url, HEADERS)
    content = BeautifulSoup(resp.text, 'html.parser')
    print(content)
    jobs_list = []
    for post in content.find_all("a", class_="jobtitle turnstileLink"):
        try:
            data = {
                "job_title": post.select('.jobTitle')[0].get_text().strip(),
                "company": post.select('.companyName')[0].get_text().strip(),
                "rating": post.select('.ratingNumber')[0].get_text().strip(),
                "location": post.select('.companyLocation')[0].get_text().strip(),
                "date": post.select('.date')[0].get_text().strip(),
                "job_desc": post.select('.job-snippet')[0].get_text().strip()

            }
        except IndexError:
            continue
        jobs_list.append(data)
    for post in content.select('.job_seen_beacon'):
        try:
            data = {
                "job_title": post.select('.jobTitle')[0].get_text().strip(),
                "company": post.select('.companyName')[0].get_text().strip(),
                "rating": post.select('.ratingNumber')[0].get_text().strip(),
                "location": post.select('.companyLocation')[0].get_text().strip(),
                "date": post.select('.date')[0].get_text().strip(),
                "job_desc": post.select('.job-snippet')[0].get_text().strip()

            }
        except IndexError:
            continue
        jobs_list.append(data)
    dataframe = pd.DataFrame(jobs_list)

    return dataframe


print(scrape_job_details(url))
