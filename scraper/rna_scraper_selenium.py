import os
import pickle
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
    len1 = len(string1) 
    len2 = len(string2)
    for i in range(len2):
        match = ""
        matched_index_list = []
        for j in range(len2):
            if (i + j < len1 and string1[i + j] == string2[j]):
                match += string2[j]
                matched_index_list.append(j)
            else:
                answer = match
                if answer != '' and len(answer) > minimum_length:
                    match_list.append({'match':answer, 'start': matched_index_list[0], 'end':matched_index_list[-1]})
                match = ""
                matched_index_list = []

        # flush the last match out of the match var after the loop
        if match != '' and len(match) > minimum_length:
            match_list.append({'match':match, 'start': matched_index_list[0], 'end':matched_index_list[-1]})

        print("iteration %s" % i)
        print("match list: %s" % len(match_list))

    return match_list

def allSubstr(instring, candidate, min_length=0):
    retset = []
    #retset = set()
    #retset.add(instring)
    totlen = len(instring)
    print("length of input: %s" % totlen)
    tenmillions_counter = 0
    iterations_counter = 0
    # for thislen in range(min_length, totlen):
    for thislen in range(min_length, totlen):
        matches_per_length = 0
        for startpos in range(0, totlen - thislen + 1):
            if (startpos + thislen <= totlen):
                is_in = (instring[startpos:startpos+thislen] in candidate)
                if (is_in):
                    matches_per_length += 1
                    retset.append([startpos,startpos+thislen, is_in])
                #store it out to a db
                iterations_counter += 1
                if (iterations_counter > 10000000):
                    tenmillions_counter += 1
                    if (tenmillions_counter > 1):
                        break
                    print ("passing another million (%s)" % tenmillions_counter)
                    iterations_counter = 0

        if (matches_per_length == 0):
            # matches per length = 0? we're done computing new matches for this sequence pair
            # i.e. if we can't find a matching substring that's 100 characters long,
            # logic stands that we can't find one that's 101 characters long either, because
            # it would have included the 100 length string
            print("stopping, found all possible matching substrings after (length %s)" % thislen)
            break

        # with open("./out/%s" % thislen, 'w') as output_file:
        #     output_file.write(str(retset))
        #     #pickle.dump(retset, output_file)
        # retset = []

    return retset


def getOverlayString(sequence, match_list):
    for match in match_list:
        length = match['end'] - match['start'] - 1
        sequence = sequence[:match['start']+1] + "x" * length + sequence[match['start'] + length+1:]
    return sequence

def getOverlayString2(sequence, match_list):
    for match in match_list:
        length = match[1] - match[0] - 1
        sequence = sequence[:match[0]+1] + "x" * length + sequence[match[0] + length+1:]
    return sequence




if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    print("start")
    #human = getRNASequence("https://www.ncbi.nlm.nih.gov/nuccore/NM_001330348.2?report=fasta")
    human = getRNASequence("https://www.ncbi.nlm.nih.gov/nuccore/NM_001382287.1?report=fasta")
    sars2 = getRNASequence("https://www.ncbi.nlm.nih.gov/nuccore/MN988668.1?report=fasta")


    # substring_set = allSubstr(human, 0)
    # print("all the substrings (min_length=0): %s" % len(substring_set))

    # substring_set = allSubstr(human, 1)
    # print("all the substrings (min_length=1): %s" % len(substring_set))

    # substring_set = allSubstr(human, 2)
    # print("all the substrings (min_length=2): %s" % len(substring_set))

    # substring_set = allSubstr(human, 3)
    # print("all the substrings (min_length=3): %s" % len(substring_set))

    # substring_set = allSubstr(human, 4)
    # print("all the substrings (min_length=4): %s" % len(substring_set))

    # substring_set = allSubstr(human, 5)
    # print("all the substrings (min_length=5): %s" % len(substring_set))

    # substring_set = allSubstr(human, 6)
    # print("all the substrings (min_length=6): %s" % len(substring_set))

    # substring_set = allSubstr(human, 7)
    # print("all the substrings (min_length=7): %s" % len(substring_set))

    substring_set = allSubstr(sars2, human, 5)
    

    #print(substring_set[0:100])

    #substrings = substringFinder(human, sars2, 5)

    
    #pp.pprint(substrings)
    #print("found %s substrings" % len(substrings))

    #test = getOverlayString("TTAAJOHNZECHLIN", [{'end': 3, 'match': 'TTAA', 'start': 0},])
    # expecting ABCDxxxxxJKLMNO
    #0123456789 1011121314
    #ABCxxxxxIJ K L M N O

    test = getOverlayString2(sars2, substring_set)
    print(test)

    print("all the sars2 substrings (min_length=7): %s" % len(substring_set))
    print("analyzed %s substrings" % len(substring_set))


    print("end")