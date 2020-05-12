import os
import logging
import pprint
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

    if os.path.exists("sequences/%s" % unique_id):
        with open("sequences/%s" % unique_id, 'r') as seq_file:
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

    with open("sequences/%s" % unique_id, 'x') as seq_file:
        seq_file.write(sequence)

    return sequence

def substringFinder(string1, string2, minimum_length=2):
    answer = ""
    match_list=[]
    len1, len2 = len(string1), len(string2)
    for i in range(len1):
        match = ""
        matched_index_list = []
        for j in range(len2):
            if (i + j < len1 and string1[i + j] == string2[j]):
                match += string2[j]
                matched_index_list.append(j)
            else:
                #if (len(match) > len(answer)): 
                answer = match
                if answer != '' and len(answer) > minimum_length:
                    match_list.append({'match':answer, 'start': matched_index_list[0], 'end':matched_index_list[-1]})
                match = ""
                matched_index_list = []

        # flush the last match out of the match var after the loop
        if match != '' and len(match) > minimum_length:
            match_list.append({'match':match, 'start': matched_index_list[0], 'end':matched_index_list[-1]})

    return match_list


if __name__ == "__main__":
    print("start")
    human = getRNASequence("https://www.ncbi.nlm.nih.gov/nuccore/NM_001330348.2?report=fasta")
    sars2 = getRNASequence("https://www.ncbi.nlm.nih.gov/nuccore/MN988668.1?report=fasta")

    substrings = substringFinder(human, sars2, 3)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(substrings)
    print("found %s substrings" % len(substrings))


    print("end")