from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import logging.config
import logging.handlers
from data_loader import job


logging.config.fileConfig('logging.ini')
logger = logging.getLogger('dataExtract')


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', seconds=20)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        # this needs corrected
        pass
