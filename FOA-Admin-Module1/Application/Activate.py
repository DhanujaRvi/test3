"""
Description     : The class ACTIVATE serves as a "POST" request functionality to activate processor in Ind-one.

Error Codes     : 200 - Activated
                  400 - Bad Request/ Already Exist

Authorization   : Done by IND-ONE 
"""

from Application.imports import *
from Database.ProcessorDb import PROCESSORDB
from Models.encrypt_decrypt import AdminDataGenerator

class ACTIVATE(Resource):

    # A decorator function         
    #@indone.indone_auth('32f8dca8-1f9c-4db2-938e-dc49c54ff69a', is_authorize = False)
    def post(self, *args, **kwargs):
        try:
            # --- LOG
            APIStartTime = datetime.now()
            # UserEmail = kwargs['user_email'] 
            # CompanyName = kwargs['company_name']
            kwargs["api"] = "/admin/activate_processor"
            kwargs['logger'] = logger
            uid = str(uuid4()) + str(datetime.now()).replace(':','').replace(' ','').replace('.','')
            kwargs["uid"] = uid
            kwargsformation(kwargs, '', '', APIStartTime)
            DBlogger.info("Entering "+kwargs["api"]+" API" ,kwargs)
            # --- LOG

            # File Logger
            logger.info("UID: {}.".format(str(kwargs["uid"])))

            data = request.get_json() 

            if 'invite_token' in data:
                invite_token = data['invite_token']
            else:
                error_message = "Invite Token Missing."
                logger.error(error_message)
                kwargsformation(kwargs, '400', response, APIStartTime)
                DBlogger.info("Exiting "+kwargs["api"]+" API", kwargs)
                return make_response(jsonify({'message':error_message}), 400)

            if 'set_password' in data:
                password = data['set_password']
            else:
                error_message = "Password Missing."
                logger.error(error_message)
                kwargsformation(kwargs, '400', response, APIStartTime)
                DBlogger.info("Exiting "+kwargs["api"]+" API", kwargs)
                return make_response(jsonify({'message':error_message}), 400)

            admin_data = AdminDataGenerator()
            emailId, admin_id = admin_data.decrypt(invite_token, kwargs, logger)
            
            processor_db = PROCESSORDB()
            response = processor_db.activate_processor(invite_token, password, emailId, admin_id, logger=logger)
            
            if response == 1 :
                logger.info('Activation Successful')
                kwargsformation(kwargs, '200', 'Activation Successful', APIStartTime)
                DBlogger.info("Exiting "+kwargs["api"]+" API", kwargs) 
                return make_response(jsonify({'message':'Activated Successful'}), 200)
            
            elif response == -2 or response == -1 :
                error_message = 'Activation Not successful'
                logger.error(error_message)
                kwargsformation(kwargs, '400', error_message, APIStartTime)
                DBlogger.info("Exiting "+kwargs["api"]+" API", kwargs) 
                return make_response(jsonify({'message': error_message}), 400)
            
            else:
                logger.error(response)
                kwargsformation(kwargs, '400', response, APIStartTime)
                DBlogger.info("Exiting "+kwargs["api"]+" API", kwargs)
                return make_response(jsonify({'message':response}), 400)
        
        except:
            print(traceback.print_exc())
            logger.error("Exception has occured, UID: "+str(kwargs["uid"]), exc_info=True)
            kwargsformation(kwargs, '400', "Bad Request", APIStartTime)
            DBlogger.info("Exiting "+kwargs["api"]+" API", kwargs)
            return make_response(jsonify({'message': 'Bad Request'}), 400)  

