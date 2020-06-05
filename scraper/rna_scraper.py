import os
import logging
from urllib.parse import urlparse

def getRNASequence(url, base_path):
    unique_id = urlparse(url).path.split('/')[-1]

    if os.path.exists("%s/%s" % (base_path, unique_id)):
        with open("%s/%s" % (base_path, unique_id), 'r') as seq_file:
            sequence = seq_file.read()
            return sequence

    return ""
