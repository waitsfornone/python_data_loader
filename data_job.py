import sqlalchemy
import csv
import time
import os
import psutil
import logging
import hashlib


def freespace_check():
    return getattr(
            psutil.disk_usage(os.path.abspath(os.sep)),
            'free')/1073741824


def GetData(int_uuid, tenant_id, out_dir, query, db_host, db_user, db_pass, db_name, purge_files=True):
    funclogger = logging.getLogger('dataExtract.getData')
    # Get current unix timestamp for filename
    epoch = int(time.time())
    print(epoch)

    # Get current PID for temp file
    cur_pid = os.getpid()
    print(cur_pid)

    # Check the output directory for proper access
    if not os.path.isdir(out_dir) or not os.access(out_dir, os.W_OK):
        funclogger.error('Output directory provided is not a directory, or is not writeable. Aborting job.')
        return False
    tmp_dir = os.path.join(out_dir, 'out')
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    if not os.access(tmp_dir, os.W_OK):
        funclogger.error('No write access to directory for temp files. Aborting job.')
        return False
    print(tmp_dir)

    # Setup the output file
    tmp_filename = "{}.csv".format(str(cur_pid))
    tmp_file = os.path.join(tmp_dir, tmp_filename)
    print(tmp_filename)

    # Freespace check
    freespace = freespace_check()
    print(freespace)

    # Purge logic
    if freespace < 10:
        if purge_files:
            files = os.listdir(tmp_dir)
            if files:
                for fle in files:
                    file_mtime = int(os.stat(fle).st_mtime)
                    if (epoch - file_mtime) >= 7776000:
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

    # Hash the provided query for use in the output filename
    query_hash = hashlib.md5(query).hexdigest()
    print(query_hash)

    # Creating output filename for Upload script
    out_filename = '{}_{}_{}_{}.csv'.format(tenant_id, int_uuid, epoch, query_hash)
    out_file = os.path.join(tmp_dir, out_filename)

    # Query DB and generate temprary file
    # There will need to be a logic set for different DB types
    engine = sqlalchemy.create_engine('postgresql://{}:{}@{}/{}'.format(db_user, db_pass, db_host, db_name))
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
    GetData(
        'testin',
        'testing',
        '/Users/tenders/Documents/code/python_data_loader',
        'select * from table',
        '192.168.103.102',
        'integration',
        "(qaswedfr{};')",
        'playmaker'
        )
