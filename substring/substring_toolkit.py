from enum import Enum

class Split(Enum):
    CONTINUE = 0
    SPLIT = 1
    DUP = 2
    SKIP = 3

def allMatchingSubstrings(target_string, string_to_match, min_length=0):
    matches = []
    length_of_target = len(target_string)
    # each iteration of the outer loop is a length 
    # the inner loop below iterates through all substrings of that length
    for length_of_substring in range(min_length, length_of_target):

        # keep track of how many matches were found for each length iteration
        matches_per_length = 0 

        # inner loop: all possible substrings that are of length length_of_substring
        for start_index in range(0, length_of_target - length_of_substring + 1):

            # only analyze substrings in bounds of the target
            if (start_index + length_of_substring <= length_of_target):

                # check if the substring of the target is in the string to match
                if (target_string[start_index:start_index+length_of_substring] in string_to_match):
                    # only add matches to the match set
                    matches_per_length += 1
                    matches.append([start_index,length_of_substring])

        if (matches_per_length == 0):
            # matches per length = 0? we're done computing new matches for this sequence pair
            # i.e. if we can't find a matching substring that's 100 characters long,
            # logic stands that we can't find one that's 101 characters long either, because
            # it would have included the 100 length string
            print("stopping, found all possible matching substrings after (length %s)" % length_of_substring)
            break

    return matches

def getRemainingSubstrings(target_string, substring_set, min_length):
    # given a target string and an array of arrays that list known matches to one or more other strings,
    # generate a list of substrings of the target string that aren't covered by any of the substrings
    # described by the substring set (i.e. the remainder)

    # first, generate a reference array
    # reference array is a parallel array to the target string
    # it describes with an enum (Split) how the remainder substrings should be built
    # the buildReferenceArray function uses the substring matches to build the reference array
    reference_array = buildReferenceArray(target_string, substring_set)

    # then, use the reference array to split the target string into a list of "remainder substrings"
    # the set of remainder subtrings is the set of substrings in the target string
    # that were in no way covered by any of the matching substrings given by the substring_set
    # i.e. the only substrings that didn't match
    result_set = buildResultSet(target_string, reference_array, min_length)

    return result_set


def buildReferenceArray(sequence, substring_set):
    # given a sequence and a set of substrings that match it, build a reference array
    reference_array = [Split.CONTINUE] * len(sequence)
    for substring in substring_set:
        start = substring[0]
        length = substring[1]

        # if the match is 3 characters, the middle one could be also used later, so duplicate it when splitting
        if (length == 3):
            reference_array[start+1] = Split.DUP

        # if the match is 4 characters, all characters might be used in other substrings, so just split (2 characters on either side)
        elif (length == 4):
            reference_array[start+1] = Split.SPLIT

        # anything longer than 4, skip all characters except for the first 2 and the last 2
        elif (length > 4):
            for i in range(start+2, start+length-2):
                reference_array[i] = Split.SKIP

    return reference_array

def buildResultSet(sequence, reference_array, min_length):
    # use a dict to control for duplicate substrings, but return an array (see return statement below)
    result_set = {}
    string_being_built = ""
    for i in range(0,len(sequence)):

        # on a Split.CONTINUE, we just add to the string_being_built
        if (reference_array[i] == Split.CONTINUE):
            string_being_built += sequence[i]

        # on a Split.SPlIT, we close out the string and start a new string with the next character
        elif (reference_array[i] == Split.SPLIT):
            string_being_built += sequence[i]
            if (len(string_being_built) > min_length):
                result_set[string_being_built] = '-'
            string_being_built = ""

        # on a Split.DUP, it's like SPLIT, but we reuse this character in the next string too (DUPlicating it)
        elif (reference_array[i] == Split.DUP):
            string_being_built += sequence[i]
            if (len(string_being_built) > min_length):
                result_set[string_being_built] = '-'
            string_being_built = "" + sequence[i]

        # on a Split.SKIP, the character won't end up in any string (close out the last string if needed)
        elif (reference_array[i] == Split.SKIP):
            if (len(string_being_built) > min_length):
                result_set[string_being_built] = '-'
            string_being_built = ""

    # there may be one last string lingering in the string_being_build var..
    if (len(string_being_built) > min_length):
        result_set[string_being_built] = '-'

    return list(result_set.keys())