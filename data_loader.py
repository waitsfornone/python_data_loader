import logging
import logging.config
import logging.handlers
import requests
from data_job import get_data
from file_uploader import upload_file
from multiprocessing import Pool


logging.config.fileConfig('logging.ini')
logger = logging.getLogger('dataExtract')

END_POINT = 'http://127.0.0.1:5000/api/'
OUT_DIR = '/Users/tenders/Documents/testing'


def get_jobs(tenant_id, integration_id=''):
    url = END_POINT + tenant_id
    if integration_id:
        url = END_POINT + tenant_id + '/' + integration_id
    work = requests.get(url)
    return work.json()


def data_job(tenant_id, integration_id, out_dir, db_info, command):
    fle = get_data(
                   tenant_id,
                   integration_id,
                   out_dir,
                   command,
                   db_info
                   )
    if fle:
        upload_file(fle)
    else:
        logger.error("No File to Upload!")


def job(tenant_id, integration_id=''):
    work_todo = get_jobs(tenant_id, integration_id)
    pool_size = work_todo['job_count']
    if pool_size > 4:
        pool_size = 4
    if work_todo['jobs']:
        worker_pool = Pool(processes=pool_size)
        for task in work_todo['jobs']:
            db_info = work_todo['jobs'][task]['db_info']
            command = work_todo['jobs'][task]['command']
            tenant_id = work_todo['jobs'][task]['tenant_id']
            integration_id = work_todo['jobs'][task]['int_uuid']
            args_tup = (tenant_id, integration_id, OUT_DIR, db_info, command,)
            ack_url = END_POINT + 'ack/' + str(work_todo['jobs'][task]['id'])
            ack = requests.get(ack_url)
            logger.info(ack.text)
            results = worker_pool.apply_async(data_job, args_tup)
            logger.info(results)
    else:
        logger.info('No jobs to run')
        return work_todo['job_count']


if __name__ == '__main__':
    job('ba91c888-a150-4e04-81ce-087d9ccd3a0f')
