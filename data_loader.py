import logging
import logging.config
import logging.handlers
from data_job import get_data
from file_uploader import upload_file
import thread

from apscheduler.schedulers.blocking import BlockingScheduler


logging.config.fileConfig('logging.ini')
logger = logging.getLogger('dataExtract')


def get_jobs(tenant_id, integration_id):
    pass


def job_wrapper_for_sub():
    fle = get_data(
                   'testin',
                   'testing',
                   '/Users/tenders/Documents/testing',
                   'select * from table',
                   'IP address',
                   'username',
                   "password",
                   'DB'
                   )
    if fle:
        upload_file(fle)
    else:
        logger.error("No File to Upload!")


def job():
    thread.start_new_thread(
        job_wrapper_for_sub()
        )


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', seconds=20)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        # this needs corrected
        pass
