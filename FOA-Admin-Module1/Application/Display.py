"""
Description     : The class DISPLAY serves as a "GET" request functionality to display data.

Error Codes     : 200 - OK
                  400 - Bad Request/

Authorization   : Done by IND-ONE 
"""

from Application.imports import *

from Models.uploader import UPLOADER
o_uploader = UPLOADER()

class DISPLAY(Resource):
    def __init__(self, **kwargs):
        self.table = kwargs.get('table')

    @indone.indone_auth('32f8dca8-1f9c-4db2-938e-dc49c54ff69a', is_authorize = False)
    def get(self, *args, **kwargs):
        try:
            # --- LOG
            APIStartTime = datetime.now()
            UserEmail = kwargs['user_email'] 
            CompanyName = kwargs['company_name']
            kwargs["api"] = "/admin/display_"+ self.table
            kwargs['logger'] = logger
            uid = str(uuid4()) + str(datetime.now()).replace(':','').replace(' ','').replace('.','')
            kwargs["uid"] = uid
            kwargsformation(kwargs, '', '', APIStartTime)
            DBlogger.info("Entering "+kwargs["api"]+" API" ,kwargs)
            # --- LOG

            # File Logger
            logger.info("UID: {}.".format(str(kwargs["uid"])))

            admin_id = str(kwargs['user_id'])
            admin_email = kwargs['user_email']
            
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
            
            response = adapter.display(admin_id, version, kwargs, logger)

            table = self.table.capitalize()
            if response == -2:
                logger.error("Not successful.")
                kwargsformation(kwargs, '400', "Not successful", APIStartTime)
                DBlogger.info("Exiting "+kwargs["api"]+" API", kwargs)
                return make_response(jsonify({'message':'Not successful'}), 400)
            else:
                logger.info("Successful.")
                kwargsformation(kwargs, '200', "Successful", APIStartTime)
                DBlogger.info("Exiting "+kwargs["api"]+" API", kwargs)
                return make_response(jsonify({'result':response}), 200)

        except:
            print(traceback.print_exc())
            logger.error("Exception has occured, UID: "+str(kwargs["uid"]), exc_info=True)
            kwargsformation(kwargs, '400', "Bad Request", APIStartTime)
            DBlogger.info("Exiting "+kwargs["api"]+" API", kwargs)
            return make_response(jsonify({'message': 'Bad Request'}), 400)  

class DISPLAY_BATCH(Resource):        
    def __init__(self, **kwargs):
        self.table = kwargs.get('table')

    @indone.indone_auth('32f8dca8-1f9c-4db2-938e-dc49c54ff69a', is_authorize = False)
    def post(self, *args, **kwargs):
        try:
            # --- LOG
            APIStartTime = datetime.now()
            UserEmail = kwargs['user_email'] 
            CompanyName = kwargs['company_name']
            kwargs["api"] = "/admin/display_batch"
            kwargs['logger'] = logger
            uid = str(uuid4()) + str(datetime.now()).replace(':','').replace(' ','').replace('.','')
            kwargs["uid"] = uid
            kwargsformation(kwargs, '', '', APIStartTime)
            DBlogger.info("Entering "+kwargs["api"]+" API" ,kwargs)
            # --- LOG

            # File Logger
            logger.info("UID: {}.".format(str(kwargs["uid"])))

            admin_id = str(kwargs['user_id'])
            admin_email = kwargs['user_email']
            
            adapter = ADAPTER(self.table)
            version = request.headers['Accept-Version']
            
            if version == 'v3.0':
                response = adapter.display(admin_id)

                table = self.table.capitalize()
                if response == -2:
                    logger.error("Not successful.")
                    kwargsformation(kwargs, '400', "Not successful", APIStartTime)
                    DBlogger.info("Exiting "+kwargs["api"]+" API", kwargs)
                    return make_response(jsonify({'message':'Not successful'}), 400)
                else:
                    logger.info("Successful.")
                    kwargsformation(kwargs, '200', "Successful", APIStartTime)
                    DBlogger.info("Exiting "+kwargs["api"]+" API", kwargs)
                    return make_response(jsonify({'result':response}), 200)

            elif version == 'v3.1':
                data = request.get_json()

                # Manually Set for Now
                processor_batch_limit = 150
                response = o_uploader.batch_display(admin_id, processor_batch_limit, version, data, kwargs, logger)
                
                if response == -2:
                    logger.error("Not successful.")
                    kwargsformation(kwargs, '400', "Not successful", APIStartTime)
                    DBlogger.info("Exiting "+kwargs["api"]+" API", kwargs)
                    return make_response(jsonify({'message':'Not successful'}), 400)
                else:
                    logger.info("Successful.")
                    kwargsformation(kwargs, '200', "Successful", APIStartTime)
                    DBlogger.info("Exiting "+kwargs["api"]+" API", kwargs)
                    return make_response(jsonify({'result':response}), 200)

        except:
            print(traceback.print_exc())
            logger.error("Exception has occured, UID: "+str(kwargs["uid"]), exc_info=True)
            kwargsformation(kwargs, '400', "Bad Request", APIStartTime)
            DBlogger.info("Exiting "+kwargs["api"]+" API", kwargs)
            return make_response(jsonify({'message': 'Bad Request'}), 400)  