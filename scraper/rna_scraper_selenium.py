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

def allMatchingSubstrings(instring, candidate, min_length=0):
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
                    # retset.append([startpos,startpos+thislen, is_in])
                    retset.append([startpos,thislen, is_in])
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

def getOverlayString3(sequence, match_list):
    for match in match_list:
        length = match[1] - match[0] - 1
        sequence = sequence[:match[0]+1] + "x" * length + sequence[match[0] + length+1:]
    return sequence

def buildReferenceArray(sequence, substring_set):
    reference_array = [0] * len(sequence)
    
    for substring in substring_set:
        start = substring[0]
        length = substring[1]

        if (length == 3):
            reference_array[start+1] = 2
        elif (length == 4):
            reference_array[start+1] = 1
        elif (length > 4):
            for i in range(start+2, start+length-2):
                reference_array[i] = 3
    return reference_array

def buildResultSet(sequence, reference_array):
    string_being_built = ""
    result_set = {}
    for i in range(0,len(sequence)):
        if (reference_array[i] == 0):
            string_being_built += sequence[i]
        elif (reference_array[i] == 1):
            string_being_built += sequence[i]
            if (len(string_being_built) > 2):
                result_set[string_being_built] = 1
            string_being_built = ""
        elif (reference_array[i] == 2):
            string_being_built += sequence[i]
            if (len(string_being_built) > 2):
                result_set[string_being_built] = 1
            string_being_built = "" + sequence[i]
        elif (reference_array[i] == 3):
            if (len(string_being_built) > 2):
                result_set[string_being_built] = 1
            string_being_built = ""
    if (len(string_being_built) > 2):
        result_set[string_being_built] = 1
    return list(result_set.keys())

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    print("start")
    human = getRNASequence("https://www.ncbi.nlm.nih.gov/nuccore/NM_001330348.2?report=fasta")
    human2 = getRNASequence("https://www.ncbi.nlm.nih.gov/nuccore/NM_001382287.1?report=fasta")
    human3 = getRNASequence("https://www.ncbi.nlm.nih.gov/nuccore/NM_004731.5?report=fasta")
    human4 = getRNASequence("https://www.ncbi.nlm.nih.gov/nuccore/NM_001318204.2?report=fasta")
    human5 = getRNASequence("https://www.ncbi.nlm.nih.gov/nuccore/NM_001329452.2?report=fasta")
    human6 = getRNASequence("https://www.ncbi.nlm.nih.gov/nuccore/NM_001040662.2?report=fasta")
    sars2 = getRNASequence("https://www.ncbi.nlm.nih.gov/nuccore/MN988668.1?report=fasta")


    substring_set1 = allMatchingSubstrings(sars2, human, 6)
    substring_set2 = allMatchingSubstrings(sars2, human2, 6)
    substring_set3 = allMatchingSubstrings(sars2, human3, 6)
    substring_set4 = allMatchingSubstrings(sars2, human4, 6)
    substring_set5 = allMatchingSubstrings(sars2, human5, 6)
    substring_set6 = allMatchingSubstrings(sars2, human6, 6)

    substring_set = substring_set1 + substring_set2 + substring_set3 + substring_set4 + substring_set5 + substring_set6

    reference_array = buildReferenceArray(sars2, substring_set)
    result_set = buildResultSet(sars2, reference_array)
    print (result_set)
    print("end")