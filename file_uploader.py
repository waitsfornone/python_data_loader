import requests
import os
# import logging


def UploadFile(file_path):
    for fle in [f for f in os.listdir(file_path) if not f.startswith('.')]:
        response = requests.post('http://127.0.0.1:5000/upload_files',
                                 files={'file_set': open(os.path.join(file_path, fle), 'r')},
                                 )
        print(response.text)
    return


if __name__ == "__main__":
    UploadFile('/Users/tenders/Documents/testing/out')
