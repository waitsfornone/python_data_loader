"""
Module Docstring for Flake8 (for now)
"""


import os
import logging
import requests

END_POINT = 'http://127.0.0.1:5000/api/upload_files/'


def upload_file_multi(file_path):
    ret_array = []
    funclogger = logging.getLogger('dataExtract.getData')
    for fle in [f for f in os.listdir(file_path) if not f.startswith('.')]:
        response = requests.post(END_POINT + fle,
                                 files={'file_set': open(os.path.join(file_path, fle), 'r')},
                                 )
        funclogger.info(response.text)
        ret_array.append((fle, response.status_code, response.text))
    return ret_array


def upload_file(file_path):
    funclogger = logging.getLogger('dataExtract.getData')
    response = requests.post(END_POINT + os.path.basename(file_path),
                             files={'file_set': open(file_path, 'r')},
                             )
    funclogger.info(response.text)
    return response.status_code


if __name__ == "__main__":
    results = upload_file_multi('/Users/tenders/Documents/testing/out')
    print results
