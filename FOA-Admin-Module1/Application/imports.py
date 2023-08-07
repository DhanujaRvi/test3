"""
Description : Imports all the (required) defined functions and python packages 
              for the Application Layer. 
"""
from flask_restful import Resource
from flask import request, make_response, jsonify
import traceback
import os

from indone_package import final_indone

env = os.environ['INDONE']
indone = final_indone.indone_auth_class(env)

from Models.model import ADAPTER
from Models.uploader import UPLOADER

# Logging
import logging 
import logging.config
from datetime import datetime
from pytz import timezone
from uuid import uuid4

logging.config.fileConfig(fname='log.conf',defaults = {'logfilename':"payables_file.log"}, disable_existing_loggers=False)
logger = logging.getLogger('filelogger')
logger.propagate = False
logging.config.fileConfig(fname='dblog.conf', disable_existing_loggers=False)
DBlogger = logging.getLogger("myapp")
DBlogger.propagate = False

for handler in logging.root.handlers:
    logging.root.removeHandler(handler)

def kwargsformation(kwargs, statuscode, statusdescription, StartTime):
    # IST = timezone('Asia/Kolkata')
    #EndTime = datetime.now(IST)
    EndTime = datetime.now()
    kwargs["statuscode"] = statuscode
    kwargs["statusdescription"] = statusdescription
    kwargs["StartTime"] = StartTime
    kwargs["time_taken"] = (EndTime - StartTime).total_seconds()
    return ''