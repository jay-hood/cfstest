import logging.config
import os

loginipath = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          'logging_config.ini'))
logging.config.fileConfig(loginipath)
logging.getLogger('fLogger')
logging.getLogger('sLogger')

logging.debug('File message one')
logging.info('Stream message one')
