"""
Description : Handling Admin Table Functionalities.
* Necessary Code Comments for function description added before the function definition.
"""
import traceback
from sqlalchemy import or_, and_, func

from Database.schema import AdminSchema
from Database import Session
import os, requests, json

class ADMINDB:
    def __init__(self):
        self.session = Session()

    # existId - Checking if the DocumentType Id already exists.
    def check_if_exists(self, adminId, kwargs={}, logger=None):
        try:
            admin = self.session.query(AdminSchema).filter(AdminSchema.adminId ==adminId)
            val = self.session.query(admin.exists()).scalar()  
            self.session.commit()
            return val
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2