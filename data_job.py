import sqlalchemy
import csv
import time
import os
import psutil
import logging
import hashlib


logging.config.fileConfig('logging.ini')


def db_conn_create(db_info):
    if db_info['type'] == 'postgresql':
        return 'postgresql://{}:{}@{}/{}'.format(
                                                 db_info['db_user'],
                                                 db_info['db_pass'],
                                                 db_info['db_host'],
                                                 db_info['db_name'])
    if db_info['type'] == 'sqlite':
        return 'sqlite+pysqlite:///{}'.format(db_info['db_file'])


def freespace_check():
    return getattr(
            psutil.disk_usage(os.path.abspath(os.sep)),
            'free')/1073741824


def dir_write_check(file_path):
    if not os.path.isdir(file_path) or not os.access(file_path, os.W_OK):
        return False
    else:
        return True


def file_purge(purge_files, file_epoch, file_path):
    funclogger = logging.getLogger('dataExtract.getData')
    freespace = freespace_check()
    if freespace < 10:
        if purge_files:
            files = os.listdir(file_path)
            if files:
                for fle in files:
                    file_mtime = int(os.stat(fle).st_mtime)
                    if (file_epoch - file_mtime) >= 7776000:
                        os.remove(fle)
                freespace = freespace_check()
                if freespace < 10:
                    funclogger.error('Purging files did not free enough space to generate data. Aborting job.')
                    return False
            else:
                funclogger.error('There are no files to purge to free space. Aborting job.')
                return False
        else:
            funclogger.error('Integration does not allow purging of files and there is not enough free space to generate data. Aborting job')
            return False
        funclogger.info('Purging of files is complete. Now generating data.')
        return True
    else:
        return True


def get_data(int_uuid, tenant_id, out_dir, query, db_info, purge_files=True):
    funclogger = logging.getLogger('dataExtract.getData')
    # Get current unix timestamp for filename
    epoch = int(time.time())

    # Get current PID for temp file
    cur_pid = os.getpid()

    # Check the output directory for proper access
    if not dir_write_check(out_dir):
        funclogger.error('Output directory provided is not a directory, or is not writeable. Aborting job.')
        return False
    tmp_dir = os.path.join(out_dir, 'out')
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    if not dir_write_check(tmp_dir):
        funclogger.error('No write access to directory for temp files. Aborting job.')
        return False

    # Setup the output file
    tmp_filename = "{}.csv".format(str(cur_pid))
    tmp_file = os.path.join(tmp_dir, tmp_filename)

    if not file_purge(purge_files, epoch, tmp_dir):
        return False

    # Hash the provided query for use in the output filename
    query_hash = hashlib.md5(query).hexdigest()

    # Creating output filename for Upload script
    out_filename = '{}_{}_{}_{}.csv'.format(tenant_id, int_uuid, epoch, query_hash)
    out_file = os.path.join(tmp_dir, out_filename)

    # Query DB and generate temprary file
    # There will need to be a logic set for different DB types
    db_connection = db_conn_create(db_info)
    engine = sqlalchemy.create_engine(db_connection)
    conn = engine.connect()
    result = conn.execute(query)
    with open(tmp_file, 'w') as tmp:
        fl = csv.writer(tmp)
        fl.writerow(result.keys())
        fl.writerows(result)

    # Rename temp file permanently
    if not os.path.exists(tmp_file):
        funclogger.error('Not output file was created. Aborting job.')
        return False

    if os.rename(tmp_file, out_file):
        return out_file
    else:
        funclogger.error('Rename of file failed. Aborting job.')
        return False


if __name__ == '__main__':
    get_data(
        'testin',
        'testing',
        '/Users/tenders/Documents/testing',
        'query',
        'Host',
        'user',
        "pass",
        'db'
        )
