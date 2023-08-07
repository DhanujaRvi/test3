"""
Description : Serves as the ADAPTER function for all the basic and other 
              functionalities of the database.
"""

import traceback
import requests
import json

from Database.ProcessorDb import PROCESSORDB
processor_db = PROCESSORDB()

from Database.QueuesDb import QUEUESDB
queues_db = QUEUESDB()

from Database.FieldsDb import FIELDSDB
fields_db = FIELDSDB()

from Database.DocumentTypeDb import DOCUMENTDB
document_db = DOCUMENTDB()

from Database.BatchDb import BATCHDB
batch_db = BATCHDB()

from Models.uploader import UPLOADER
o_uploader = UPLOADER()

class ADAPTER:
    def __init__(self, table):
        self.table = table

    # insert - adapter insert for the input table
    def insert(self, data, adminId, auth_type, auth_headers, kwargs, logger):
        logger.info("ENTERING INSERT FUNCTIONALITY.")

        try:
            logger.info("INSERT TABLE -- table: {}".format(self.table))

            if(self.table == 'processor'):
                name = data['name']
                emailId = data['emailId']
                role = data['role']
                return processor_db.insert(name, emailId, role, adminId, auth_headers, logger=logger)
        
            elif(self.table == 'queues'):
                name = data['name']
                return queues_db.insert(name, adminId, logger=logger)
            
            elif(self.table == 'fields'):
                name = data['name']
                description = data['description']
                dataType = data['dataType']
                category = data['category']
                return fields_db.insert(name, description, dataType, category, adminId, logger=logger)

            elif (self.table == 'document'):
                name = data['name']
                description = data['description']
                fieldsId = data['fieldsId']

                fieldsId = [int(id) for id in fieldsId]
                # Insert in the database and get the documentId
                documentId, insert_response = document_db.insert(name, description, fieldsId, adminId, logger=logger)
                if insert_response == -2:
                    logger.error("Error in inserting document in the DocumentDb" )
                    return -2

                # Check if Admin has Config File
                config_info, status_code = self.get_config(adminId, auth_type, auth_headers, kwargs, logger)
                if status_code != 200:
                    logger.error("Error in getting config file for admin {}.".format(adminId))
                    return -2

                if len(config_info) > 0:
                    # Config File Exists
                    if "default_docType" in config_info:
                        config_info["default_docType"][str(documentId)] = fieldsId
                            
                        status_code = self.update_config(config_info, auth_type, auth_headers, kwargs, logger)
                        if status_code != 200:
                            logger.error("Error in updating config file for admin {}.".format(adminId))
                            return -2
                    else:
                        config_info["default_docType"] = {}
                        config_info["default_docType"][str(documentId)] = fieldsId

                        status_code = self.update_config(config_info, auth_type, auth_headers, kwargs, logger)
                        if status_code != 200:
                            logger.error("Error in updating config file for admin {}.".format(adminId))
                            return -2
                return 1
        except:
            print(traceback.print_exc())
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # delete - adapter delete for the input table
    def delete(self, data, user_id, user_email, is_admin, auth_type, auth_headers, kwargs, logger):
        logger.info("ENTERING DELETE FUNCTIONALITY.")

        try:
            logger.info("DLETE TABLE -- table: {}".format(self.table))

            if(self.table == 'processor'):
                pId = data['id']
                assigned_batch = processor_db.get_assigned_batch(pId, user_id, logger=logger)
                for bId in assigned_batch:
                    batch_db.assign_processor("None", user_id, bId, logger=logger)

                return processor_db.delete(pId, user_id, auth_headers, logger=logger)

            elif(self.table == 'queues'):
                qid  = data['id']
                # deleting batches uploaded in the queue
                bIds = batch_db.get_batchs(qid ,user_id, logger=logger)
                
                response = batch_db.admin_batch_delete( bIds, user_id, user_email, logger=logger)
                if response == -2:
                    logger.error("Error in admin_batch_delete() While deleting the batch in BatchDb.")
                    return -2
                return queues_db.delete(qid, user_id, logger=logger)

            elif(self.table == 'fields'):
                id = data['id']
                return fields_db.delete(id, user_id, logger=logger)

            elif (self.table == 'document'):
                id = data['id']

                # Check if Admin has Config File
                config_info, status_code = self.get_config(user_id, auth_type, auth_headers, kwargs, logger)
                if status_code != 200:
                    logger.error("Error in getting config file.")
                    return -2

                if len(config_info) > 0:
                    # Config File Exists
                    if "default_docType" in config_info:
                        if str(id) in config_info["default_docType"]:
                            del config_info["default_docType"][str(id)]
                                
                            status_code = self.update_config(config_info, auth_type, auth_headers, kwargs, logger)
                            if status_code != 200:
                                logger.error("Error in updating config file.")
                                return -2

                return document_db.delete(id, user_id, logger=logger)

            elif (self.table == 'batch'):
                # Check if the user is admin or processor
                ids = data['ids']   
                if is_admin == True:
                    return batch_db.admin_batch_delete(ids, user_id, user_email, logger=logger)
                else:
                    return batch_db.processor_batch_delete(ids, user_id, user_email, logger=logger)
                    
        except:
            print(traceback.print_exc())
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # display - adapter display for the input table
    def display(self, adminId, version, kwargs, logger):
        logger.info("ENTERING DISPLAY FUNCTIONALITY.")

        try:
            logger.info("DISPLAY TABLE -- table: {}".format(self.table))

            if(self.table == 'processor'):                  
                return processor_db.display(adminId, logger=logger)
            
            elif(self.table == 'queues'):
                return queues_db.display(adminId, logger=logger)
                
            elif(self.table == 'fields'):
                return fields_db.display(adminId, version, logger=logger)

            elif (self.table == 'document'):
                return document_db.display(adminId, logger=logger)
            
            elif (self.table == 'batch'):
                processor_batch_limit = 150
                return o_uploader.batch_display(adminId, processor_batch_limit, 'v3.0', {}, kwargs, logger)
                
        except:
            print(traceback.print_exc())
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # map - adapter map for the input table
    def map(self, data, adminId, kwargs, logger):
        logger.info("ENTERING MAP FUNCTIONALITY.")

        try:
            if(self.table == 'processor'):
                queues = data['queues']                 # queue id
                processor = data['processor']           # list of processor id
                return processor_db.map(queues, processor, adminId, logger=logger)
            
            elif(self.table == 'document'):
                queues = data['queues']                 # queue id
                document = data['document']             # List of document id
                return document_db.map(queues, document, adminId, logger=logger)
        except:
            print(traceback.print_exc())
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # unmap - adapter unmap for the input table
    def unmap(self, data, adminId, kwargs, logger):
        logger.info("ENTERING UNMAP FUNCTIONALITY.")

        try:
            if(self.table == 'processor'):
                queues = data['queues']                 # queue id
                processor = data['processor']           # list of processor id
                return processor_db.unmap(queues, processor, adminId, logger=logger)
            
            elif(self.table == 'document'):
                queues = data['queues']                 # queue id
                document = data['document']             # List of document id
                return document_db.unmap(queues, document, adminId, logger=logger)
        except:
            print(traceback.print_exc())
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)

            return -2


    # edit - adapter edit for the input table
    def edit(self,data, adminId, auth_type, auth_headers, kwargs, logger):
        logger.info("ENTERING EDIT FUNCTIONALITY.")

        try:
            logger.info("EDIT TABLE -- table: {}".format(self.table))

            if(self.table == 'processor'):
                id = data['id']
                name = data['name']
                emailId = data['emailId']
                role = data['role']
                return processor_db.update(id, name, emailId, role, adminId, logger=logger)

            elif(self.table == 'queues'):
                id = data['id']
                name = data['name']
                return queues_db.update(id, name, adminId, logger=logger)
            
            elif(self.table == 'fields'):
                fields = data['Fields']
                return fields_db.update(fields, adminId, logger=logger)

            elif (self.table == 'document'):
                id = data['id']
                name = data['name']
                description = data['description']
                fieldsId = data['fieldsId']

                # Check if Admin has Config File
                config_info, status_code = self.get_config(adminId, auth_type, auth_headers, kwargs, logger)
                if status_code != 200:
                    logger.error("Error in getting config file for admin {}.".format(adminId))
                    return -2

                if len(config_info) > 0:
                    if "default_docType" in config_info:
                        if str(id) in config_info["default_docType"]:
                            config_info["default_docType"][str(id)] = fieldsId
                            
                            status_code = self.update_config(config_info, auth_type, auth_headers, kwargs, logger)
                            if status_code != 200:
                                logger.error("Error in updating config file for admin {}.".format(adminId))
                                return -2

                return document_db.update(id, name, description, fieldsId, adminId, logger=logger)

        except:
            print(traceback.print_exc())
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # Internal API call to get config file
    def get_config(self,admin_id, auth_type, auth_headers, kwargs, logger):
        logger.debug("ENTERING GET CONFIG FUNCTIONALITY.")

        try:
            url = "http://localhost:8000/api/display_config"
            logger.info("CALLING API -- url: {}".format(url))
            
            if auth_type == "Bearer":
                headers = {
                    'Authorization': auth_headers,
                    'content-type': 'application/json',
                    'Accept-Version': 'v3.0'
                }
            elif auth_type == "x-api-key":
                headers = {
                    "x-api-key":auth_headers,
                    'content-type': 'application/json',
                    'Accept-Version': 'v3.0'
                }
        
            payload = {
                "adminId": str(admin_id),
            }

            response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
            logger.info("STATUS CODE: status_code: {}".format(response.status_code))

            if response.status_code == 200:
                data = response.json()
                return data['result'], response.status_code
            else:
                {}, response.status_code

        except Exception as e:
            print(e)
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return {}, 400

    # Internal API call to get config file
    def update_config(self, config_info, auth_type, auth_headers, kwargs, logger):
        logger.debug("ENTERING UPDATE CONFIG FUNCTIONALITY.")

        try:
            url = "http://localhost:8000/api/update_config"
            logger.info("CALLING API -- url: {}".format(url))

            if auth_type == "Bearer":
                headers = {
                    'Authorization': auth_headers,
                    'content-type': 'application/json',
                    'Accept-Version': 'v3.0',
                    'Edit-DocumentType': '1',
                    'Edit-QueueProperties': '0'
                }
            elif auth_type == "x-api-key":
                headers = {
                    "x-api-key":auth_headers,
                    'content-type': 'application/json',
                    'Accept-Version': 'v3.0',
                    'Edit-DocumentType': '1'
                }

            response = requests.request("PATCH", url, headers=headers, data = json.dumps(config_info))
            logger.info("STATUS CODE: status_code: {}".format(response.status_code))
            
            return response.status_code

        except Exception as e:
            print(e)
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return {}
