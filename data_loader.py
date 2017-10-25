"""
Demonstrates how to use the blocking scheduler to schedule
a job that executes on 3 second
intervals.
"""

import logging
import logging.config
import logging.handlers
import data_job

from apscheduler.schedulers.blocking import BlockingScheduler


logging.config.fileConfig('logging.ini')
logger = logging.getLogger('dataExtract')


def job():
    data_job.GetData(
        'testin',
        'testing',
        '/Users/tenders/Documents/code/python_data_loader',
        'select * from pm20029.referrals limit 10',
        '192.168.103.102',
        'integration',
        "(qaswedfr{};')",
        'playmaker'
        )


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', seconds=3)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        # this needs corrected
        pass
