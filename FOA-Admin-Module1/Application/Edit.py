"""
Description     : The class EDIT serves as a "PATCH" request functionality to edit data.

Error Codes     : 200 - OK
                  400 - Bad Request
                  401 - Unauthorized

Authorization   : Done by IND-ONE 
"""

from Application.imports import *

class EDIT(Resource):
    def __init__(self, **kwargs):
        self.table = kwargs.get('table')

    @indone.indone_auth('32f8dca8-1f9c-4db2-938e-dc49c54ff69a', is_authorize = False)
    def patch(self, *args, **kwargs):
        try:
            # --- LOG
            APIStartTime = datetime.now()
            UserEmail = kwargs['user_email'] 
            CompanyName = kwargs['company_name']
            kwargs["api"] = "/admin/edit_"+ self.table
            kwargs['logger'] = logger
            uid = str(uuid4()) + str(datetime.now()).replace(':','').replace(' ','').replace('.','')
            kwargs["uid"] = uid
            kwargsformation(kwargs, '', '', APIStartTime)
            DBlogger.info("Entering "+kwargs["api"]+" API" ,kwargs)
            # --- LOG

            # File Logger
            logger.info("UID: {}.".format(str(kwargs["uid"])))

            auth_type  = "Bearer"
            auth_headers = request.headers.get('Authorization')
            
            if auth_headers == None:
                auth_type = "x-api-key"
                auth_headers = request.headers['x-api-key']

            admin_id = str(kwargs['user_id'])
            admin_email = kwargs['user_email']
            data = request.get_json()
            adapter = ADAPTER(self.table)

            if 'Accept-Version' in request.headers:
                version = request.headers['Accept-Version']
                logger.info("VERSION -- version: {}".format(version))
            else:
                error_message = "Version is not specified."
                logger.error(error_message)
                kwargsformation(kwargs, '400', error_message, APIStartTime)
                DBlogger.info("Exiting "+kwargs["api"]+" API", kwargs)
                return make_response(jsonify({'message': error_message}), 400)
            
            if version == 'v3.0':
                response = adapter.edit(data, admin_id, auth_type, auth_headers, kwargs, logger)

                table = self.table.capitalize()
                
                if response == -2:
                    logger.error("Not successful")
                    kwargsformation(kwargs, '400', "Not successful", APIStartTime)
                    DBlogger.info("Exiting "+kwargs["api"]+" API", kwargs)
                    return make_response(jsonify({'message':'Not Successful'}), 400)
                
                elif response == -1:
                    message = '{} does not exists'.format(table)
                    logger.error(message)
                    kwargsformation(kwargs, '400', error_message, APIStartTime)
                    DBlogger.info("Exiting "+kwargs["api"]+" API", kwargs)
                    return make_response(jsonify({'message': message}), 400)
                
                else:
                    message = '{} Updated Successfully'.format(table)
                    logger.info(message)
                    kwargsformation(kwargs, '200', message, APIStartTime)
                    DBlogger.info("Exiting "+kwargs["api"]+" API", kwargs)
                    return make_response(jsonify({'message': message}), 200)
        
        except:
            print(traceback.print_exc())
            logger.error("Exception has occured, UID: "+str(kwargs["uid"]), exc_info=True)
            kwargsformation(kwargs, '400', "Bad Request", APIStartTime)
            DBlogger.info("Exiting "+kwargs["api"]+" API", kwargs)
            return make_response(jsonify({'message': 'Bad Request'}), 400)  
            
