import sqlalchemy
import csv
import time
import os
import psutil
import logging


# Work on getting postgresql working first,
# then worry about how to properly handle the other typical databases
def freespace_check():
    return getattr(
            psutil.disk_usage(os.path.abspath(os.sep)),
            'free')/1073741824


def GetData(int_uuid, tenant_id, out_dir, purge_files=True):
    funclogger = logging.getLogger('dataExtract.getData')
    # Get current unix timestamp for filename
    epoch = int(time.time())
    print(epoch)

    # Get current PID for temp file
    cur_pid = os.getpid()

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
    return True

# connect to the database
# engine = create_engine('postgresql://scott:tiger@localhost/mydatabase')


if __name__ == '__main__':
    GetData(
        'testin',
        'testing',
        '/Users/tenders/Documents/code/python_data_loader')
