
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

#https://twistedmatrix.com/pipermail/twisted-python/2013-October/027579.html

import os
import json
import datetime
import time
import logging
import logging.config

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

import daemon

import config_manager




#http://twistedmatrix.com/documents/13.0.0/core/howto/threading.html
#http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html


# rpi-mqtt <-> xbee <-> xbee sensors (store data in SQL for orginization)
# rpi-mqtt <-> wifi <-> server mqtt (NOT VITAL)
# rpi-mqtt <-> 3G dongle <-> cellphone (VITAL)

# Watchdog 
# Alerts if sensor "update" exceeds the timeout. 
# So if the timeout is 1 second, and 2 seconds have passed, issue an alert. 


# SQLAlchemy

cr = config_manager.ConfigReader()
config = cr.read_config()

assert(config)

db_uri   = cr.get_db_uri()
interval = config['general']['interval']
sensors  = config['sensors']

if not os.path.exists(config['database']['path']):
    print('database does not exist, quitting')
    exit(1)

Base = automap_base()
engine = create_engine(db_uri)
Base.prepare(engine, reflect=True)

session = Session(engine)

logging.config.fileConfig('%s/log.conf' % (config['general']['working_dir']))
logger = logging.getLogger('root')

#logging.getLogger().addHandler(logging.StreamHandler())

def check_sensors(sensors):
    s = Base.classes.sensors
    
    logger.info('checking sensors')

    for sensor in sensors:
        e = sensors[sensor]['expected_value']
        i = sensors[sensor]['interval']

        q    = session.query(s).order_by(s.date.desc()).first()
        diff = datetime.datetime.now() - q.date

        if diff.seconds >= i:
            logger.warn('exceeded watch interval (%s total seconds))' % (diff.seconds))
    

        



while True:
    time.sleep(interval)
    check_sensors(sensors)
