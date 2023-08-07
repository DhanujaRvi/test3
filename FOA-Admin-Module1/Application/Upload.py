"""
Description     : The class UPLOAD serves as a "POST" request functionality to upload the data

Error Codes     : 200 - OK
                  400 - Bad Request
                  401 - Unauthorized

Authorization   : Done by IND-ONE 

"""

from Application.imports import *

class UPLOAD(Resource):
    def __init__(self, **kwargs):
        pass

    @indone.indone_auth('32f8dca8-1f9c-4db2-938e-dc49c54ff69a', is_authorize = False)
    def post(self, *args, **kwargs):
        try:
            # --- LOG
            print("Entering Upload")
            APIStartTime = datetime.now()
            UserEmail = kwargs['user_email'] 
            CompanyName = kwargs['company_name']
            kwargs["api"] = "/admin/upload_batch"
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
            
            queuesId = request.form["queuesId"]
            #processor_batch_limit = request.form["processor_batch_limit"]
            processor_batch_limit = 150
            uploaded_files = request.files
            
            o_uploader = UPLOADER()

            if 'Accept-Version' in request.headers:
                version = request.headers['Accept-Version']
                logger.info("VERSION -- version: {}".format(version))
            else:
                error_message = "Version is not specified."
                logger.error(error_message)
                kwargsformation(kwargs, '400', error_message, APIStartTime)
                DBlogger.info("Exiting "+kwargs["api"]+" API", kwargs)
                print("Error")
                return make_response(jsonify({'message': error_message}), 400)

            if version == 'v3.0':
                bId, batch_name, response = o_uploader.upload(queuesId, admin_id, admin_email,uploaded_files, auth_headers, auth_type, processor_batch_limit, kwargs, logger)

                if response == -2:
                    logger.error("Not successful.")
                    kwargsformation(kwargs, '400', "Not successful", APIStartTime)
                    DBlogger.info("Exiting "+kwargs["api"]+" API", kwargs)
                    print("V3.0")
                    return make_response(jsonify({'message':'Not successful'}), 400)
                else:
                    message = "Batch Uploaded Successfully, BID:"+str(bId)
                    logger.info(message)
                    kwargsformation(kwargs, 200, message, APIStartTime)
                    DBlogger.info("Exiting "+kwargs["api"]+" API", kwargs)
                    print("Successful")
                    return make_response(jsonify({'message':'Batch Uploaded Successfully',"bId":bId, "batch_name": batch_name}), 200)
        except:
            print(traceback.print_exc())
            logger.error("Exception has occured, UID: "+str(kwargs["uid"]), exc_info=True)
            kwargsformation(kwargs, '400', "Bad Request", APIStartTime)
            DBlogger.info("Exiting "+kwargs["api"]+" API", kwargs)
            print("Bad Request")
            return make_response(jsonify({'message': 'Bad Request'}), 400)
            
