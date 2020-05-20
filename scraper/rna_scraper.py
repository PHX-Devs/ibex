import os
import logging
from urllib.parse import urlparse
from selenium import webdriver

# Set the threshold for selenium to WARNING
from selenium.webdriver.remote.remote_connection import LOGGER as seleniumLogger
seleniumLogger.setLevel(logging.WARNING)
# Set the threshold for urllib3 to WARNING
from urllib3.connectionpool import log as urllibLogger
urllibLogger.setLevel(logging.WARNING)

def getRNASequence(url):
    unique_id = urlparse(url).path.split('/')[-1]

    if os.path.exists("scraper/sequences/%s" % unique_id):
        with open("scraper/sequences/%s" % unique_id, 'r') as seq_file:
            sequence = seq_file.read()
            return sequence

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--silent')
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    driver.get(url)

    pre = driver.find_element_by_css_selector("div.seq > pre")
    try:
        sequence = pre.get_attribute('innerHTML').split('mRNA')[1]
    except IndexError:
        sequence = pre.get_attribute('innerHTML').split('complete genome')[1]

    sequence = "".join(sequence.split())
    print(sequence)

    with open("scraper/sequences/%s" % unique_id, 'x') as seq_file:
        seq_file.write(sequence)

    return sequence
