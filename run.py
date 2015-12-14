import json
import paramiko
import logging
import sys
import time
import os

# Clear Log
open('last_run_log', 'w').close()

# Configure Logger
logging.basicConfig(filename='last_run_log',
                    level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger('backup_wpengine')

# Add Logger Success Level
logging.SUCCESS = 25  # between WARNING and INFO
logging.addLevelName(logging.SUCCESS, 'SUCCESS')
setattr(log, 'success', lambda message, *args:
        log._log(logging.SUCCESS, message, args))

# Setup Backup Directory
directory = 'backups/'
if not os.path.exists(directory):
    log.error('The backup directory %s does not exist!' % directory)
    sys.exit(1)

# Load Settings
with open('settings.json', 'r') as f:
    settings = json.load(f)

# Being Main Loop for WPEngine Sites
for site in settings['sites']:
    try:
        # Attempt SFTP Conneciton
        transport = paramiko.Transport((site['hostname'], site['port']))
        transport.connect(username=site['username'], password=site['password'])
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Check that Remote File Exists
        sftp.stat(site['filepath'])

        # Attempt Download of File
        localpath = (directory + site['username'] + '-' +
                     time.strftime('%Y%m%d%H%M%S') + '.sql')
        sftp.get(site['filepath'], localpath)

        # Close Connection
        sftp.close()
        transport.close()

        # Output SUCCESS
        log.success('Successfully backed up %s to %s on %s@%s' % (
                     site['filepath'],
                     localpath,
                     site['username'],
                     site['hostname']))

    except paramiko.AuthenticationException:
        log.error("Failed to connect to %s@%s." % (
                   site['username'],
                   site['hostname']))
    except IOError:
        log.error("Could not find the filepath specified: %s" % (
                   site['filepath']))

sys.exit(0)
