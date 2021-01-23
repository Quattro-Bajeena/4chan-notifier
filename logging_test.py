import logging
import datetime
import time
# logging.basicConfig(filename='example.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
# logging.debug('This message shoudl go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')


now = datetime.datetime.now().strftime('%d-%m-%Y %H:%M')
print(now)
