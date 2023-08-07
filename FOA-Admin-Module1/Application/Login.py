"""
Description     : The class LOGIN serves as a "POST" request functionality to 
                check whether the user logged in is admin or not.

Error Codes     : 200 - OK
                  400 - Bad Request

Authorization   : Done by IND-ONE 
"""

from Application.imports import *
from Database.AdminDb import ADMINDB

class LOGIN(Resource):
    def __init__(self, **kwargs):
        self.o_adminDb = ADMINDB()

                   
    @indone.indone_auth('32f8dca8-1f9c-4db2-938e-dc49c54ff69a', is_authorize = False)
    def get(self, **kwargs):
        try:
            admin_id = str(kwargs['user_id'])
            adminstatus = kwargs['is_admin']

            return make_response(jsonify({'is_admin': adminstatus}), 200)
        except:
            print(traceback.print_exc())
            return make_response(jsonify({'message': 'Request could not be handled'}), 400)
    