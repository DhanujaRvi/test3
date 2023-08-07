"""
Description : Handling Processor Table Creation, Deletion, Display and Other Functionalities.
* Necessary Code Comments for function description added before the function definition.
"""

from sqlalchemy import or_, and_, func

from Database.schema import ProcessorSchema, MapQueuesProcessor, QueuesSchema
from Database import Session

from Database.QueuesDb import QUEUESDB
queuesDb= QUEUESDB()

import os, requests, json

class PROCESSORDB():
    def __init__(self):
        self.session = Session()

    #BASIC FUNCTIONALITIES
    # insert - For Inserting a New Processor in the Database.
    def insert(self, name, emailId, role,  adminId, auth_headers, kwargs={}, logger=None):
        try:
            #Insert Only when Processor doesn't already exists.
            if self.getId(emailId, adminId) == -1:
                ind_response = self.send_invite(emailId, auth_headers)
                if ind_response == -2:
                    logger.error("Error in sending invite.")
                    return -2
                elif ind_response == 2:
                    status = "active"
                    p1 = ProcessorSchema(name, emailId, role, status, adminId)
                    self.session.add(p1)
                    self.session.commit()
                    return 2
                else:
                    status = "in_active"
                    p1 = ProcessorSchema(name, emailId, role, status, adminId)
                    self.session.add(p1)
                    self.session.commit()
                    return 1
            else:
                status = self.check_status(emailId, adminId)
                if status == 'in_active':
                    ind_response = self.send_invite(emailId, auth_headers)
                    if ind_response == -2:
                        logger.error("Error in sending invite.")
                        return -2
                    return -3
                else:
                    return -1
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # Delete - For Deleting a Processor in the Database.
    def delete(self, pId, adminId, auth_headers, kwargs={}, logger=None):
        try:
            # Checking if the Processor Id exists to delete.
            if(self.existId(pId, adminId)):
                emailId = self.getemailId(pId, adminId)
                # indId = self.getindId(pId, adminId)
                # if indId != -1:
                #     ind_response = self.deactivate_processor(emailId, auth_headers)
                #     if ind_response == -2:
                #          logger.error("Error in deactivating the processor.")
                #         return -2
                cond = and_(ProcessorSchema.id == pId, ProcessorSchema.adminId == adminId)
                self.session.query(ProcessorSchema).filter(cond).delete()
                self.session.commit()
                return 1
            else:
                # processor not found
                return -1   
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # Update - For Updating a Processor
    def update(self, id, name, emailId, role, adminId, kwargs={}, logger=None):
        try:
            #Edit Only when Processor already exists.
            if(self.existId(id, adminId)):
                cond = and_(ProcessorSchema.id == id, ProcessorSchema.adminId == adminId)
                self.session.query(ProcessorSchema).filter(cond).update({ProcessorSchema.name:name, ProcessorSchema.emailId:emailId, ProcessorSchema.role:role})
                self.session.commit()
                return 1
            #Processor not found
            else:
                return -1
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    #display - Displaying the available Processors for the specified admin.
    def display(self, adminId, kwargs={}, logger=None):
        try:
            cond = and_(ProcessorSchema.adminId == adminId, ProcessorSchema.default_flag == False)
            processors = self.session.query(ProcessorSchema).filter(cond).all()
            response = {}
            processor_list = []
            if(processors):
                for processor in processors:
                    results = {}
                    results["id"] = processor.id
                    results["name"] = processor.name
                    results["emailId"] = processor.emailId
                    results["role"] = processor.role
                    results["status"] = processor.status
                    results["batch_count"] = len(processor.batch_assigned)
                    queue_count = self.get_queuescount(processor.id, adminId)
                    queues_mapped = self.mappedQueues(processor.id, adminId)
                    if(queue_count != -2 and queues_mapped != -2):
                        results['queues_count'] = queue_count
                        results['mapping'] = {}
                        for queue in queues_mapped:
                            results['mapping'][queue] = "Yes"
                    else:
                        return -2
                    processor_list.append(results)
            response["Processors"]= processor_list
            response["Total Processors"] = len(processor_list)
            return response
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    #OTHER FUNCTIONALITIES
    # getId - Getting the Id of the Processor from the Database.
    # append batch Id to batch_assigned field in the ProcessorDb Database
    def get_assigned_batch(self, pId, adminId, kwargs={}, logger=None):
        try:
            #Check if Processor already exists.
            if(self.existId(pId, adminId)):
                cond = and_(ProcessorSchema.id == pId, ProcessorSchema.adminId == adminId)
                processor = self.session.query(ProcessorSchema).filter(cond).first()
                return processor.batch_assigned
            #Processor not found
            else:
                return -2
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    def getId(self, emailId, adminId, kwargs={}, logger=None):
        try:
            cond = and_(ProcessorSchema.emailId == emailId, ProcessorSchema.adminId == adminId)
            processor = self.session.query(ProcessorSchema).filter(cond).first()
            if processor:
                return processor.id
            else:
                return -1    #processor not already exists
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)

            return -2

    # getName - Getting the Name of the Processor from the Database using emailID.
    def getName(self, emailId, adminId, kwargs={}, logger=None):
        try:
            cond = and_(ProcessorSchema.emailId == emailId, ProcessorSchema.adminId == adminId)
            processor = self.session.query(ProcessorSchema).filter(cond).first()
            if processor:
                return processor.name
            else:
                return -1    #processor not already exists
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # getemailId - Getting the emailID of the Processor from the Database using Id.
    def getemailId(self, pId, adminId, kwargs={}, logger=None):
        try:
            cond = and_(ProcessorSchema.id == pId, ProcessorSchema.adminId == adminId)
            processor = self.session.query(ProcessorSchema).filter(cond).first()
            if processor:
                return processor.emailId
            else:
                return -1    #processor not already exists
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    def getindId(self, pId, adminId, kwargs={}, logger=None):
        try:
            cond = and_(ProcessorSchema.id == pId, ProcessorSchema.adminId == adminId)
            processor = self.session.query(ProcessorSchema).filter(cond).first()
            if processor:
                return processor.indId
            else:
                return -1    #processor not already exists
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # existId - Checking if the Processor Id already exists.
    def existId(self, id, adminId, kwargs={}, logger=None):
        try:
            queue = self.session.query(ProcessorSchema).filter(ProcessorSchema.id ==id, ProcessorSchema.adminId == adminId)
            return self.session.query(queue.exists()).scalar()  
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return False
    
    # is_mapped - Checking if Queue and Processor is mapped from MapQueuesProcessor Table.
    def is_mapped(self, qId, pId, adminId, kwargs={}, logger=None):
        try:
            cond = and_(MapQueuesProcessor.queuesId == qId, MapQueuesProcessor.processorId == pId, MapQueuesProcessor.adminId == adminId)
            document = self.session.query(MapQueuesProcessor).filter(cond)
            return self.session.query(document.exists()).scalar()
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return False

    # map - Mapping queue with processor(s).
    def map(self, qId , processor, adminId, kwargs={}, logger=None):
        try:
            if queuesDb.existId(qId,adminId):
                for pId in processor:
                    # Checking if processor exists and mapped to the queue already.
                    if self.existId(pId, adminId) and not self.is_mapped(qId,pId,adminId):
                        self.session.add(MapQueuesProcessor(queuesId = qId, processorId = pId, adminId =adminId))
                self.session.commit()
                return 1
            # Either Queue or processor not exists.
            return -1    
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2
    
    # unmap - UnMapping queue with processor(s).
    def unmap(self, qId , processor, adminId, kwargs={}, logger=None):
        try:
            if queuesDb.existId(qId,adminId):
                for pId in processor:
                    # Checking if processor exists and mapped to the queue.
                    if self.existId(pId, adminId) and self.is_mapped(qId,pId,adminId):
                        cond = and_(MapQueuesProcessor.queuesId == qId, MapQueuesProcessor.processorId == pId, MapQueuesProcessor.adminId == adminId)
                        self.session.query(MapQueuesProcessor).filter(cond).delete()
                self.session.commit()
                return 1
            # Either Queue or processor not exists.
            return -1   
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2
    
    # get the count of queues mapped to the given processor
    def get_queuescount(self, id, adminId, kwargs={}, logger=None):
        try:
            cond = and_(MapQueuesProcessor.processorId == id, MapQueuesProcessor.adminId == adminId)
            queue_count = self.session.query(func.count(MapQueuesProcessor.queuesId)).filter(cond).scalar()
            return queue_count
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2
    
    # get the queues mapped to the given processor
    def mappedQueues(self, id, adminId, kwargs={}, logger=None):
        try:
            cond = and_(MapQueuesProcessor.processorId == id, MapQueuesProcessor.adminId == adminId)
            queues = self.session.query(MapQueuesProcessor).filter(cond).all()
            response = []
            if queues:
                for queue in queues:
                    qId = queue.queuesId
                    que = self.session.query(QueuesSchema).filter(QueuesSchema.id == qId).first()
                    response.append(que.name)
            return response
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    def check_status(self, emailId, adminId, kwargs={}, logger=None):
        try:
            cond = and_(ProcessorSchema.emailId == emailId, ProcessorSchema.adminId == adminId)
            processor = self.session.query(ProcessorSchema).filter(cond).first()
            if processor:
                return processor.status
            else:
                return -1    #processor not exists
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # send email invite from indone
    def send_invite(self, emailId, auth_headers, kwargs={}, logger=None):
        try:
            application = os.environ['APPLICATION']
            product_url = os.environ['PRODUCT_URL']
            url_processor_invite = os.environ['URL_PROCESSOR_INVITE']

            invite_data = {"email_list":[emailId], "application":application, "product_url":product_url}
            invite_response = requests.post(url_processor_invite,\
                                        data=json.dumps(invite_data),\
                                        headers={'Content-Type':'application/json','Authorization':auth_headers})
            # print(invite_response.json())
            if invite_response.status_code == 201:
                return 1                 # user invited
            elif invite_response.status_code == 400 and invite_response.json()['message'] == "users exists already":
                return 2                 # users exists already in ind_one save it in our processor database
            else:
                return -2                # Processor invite not sucessfull
        except:
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2
    
    # deactivate processor in indone
    def deactivate_processor(self, emailId, auth_headers, kwargs={}, logger=None):
        try:
            application = os.environ['APPLICATION']
            product_url = os.environ['PRODUCT_URL']
            url_processor_deactivate = os.environ['URL_PROCESSOR_DEACTIVATE']

            invite_data = {"email":[emailId]}#, "application":application, "product_url":product_url}
            invite_response = requests.post(url_processor_deactivate,\
                                        data=json.dumps(invite_data),\
                                        headers={'Content-Type':'application/json','Authorization':auth_headers})
            if invite_response.status_code == 200:
                return 1                 # user deactivated
            else:
                return -2                # Processor not deactivated
        except:
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # update processor status as active 
    def update_status(self, emailId, adminId, kwargs={}, logger=None):
        try:
            #Edit Only when Processor already exists.
            pId = self.getId(emailId, adminId)
            if(self.existId(pId, adminId)):
                cond = and_(ProcessorSchema.id == pId, ProcessorSchema.adminId == adminId)
                self.session.query(ProcessorSchema).filter(cond).update({ProcessorSchema.status:"active"})
                self.session.commit()
                return 1
            #Processor not found
            else:
                return -1
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # activate processor using ind-one 
    def activate_processor(self, invite_token, password, emailId, adminId, kwargs={}, logger=None):
        try:
            url_processor_activate = os.environ['URL_PROCESSOR_ACTIVATE']

            name = self.getName(emailId, adminId)
            if(name != -2 or name != -1):
                first_name = name
                last_name = ' '
                phone = " "
                payload = dict(token=invite_token, phone=phone, password=password, first_name=first_name, last_name=last_name)
                raw_response = requests.post(url_processor_activate, headers={'Content-Type':'application/json'}, data=json.dumps(payload))
                response = raw_response.json()
                if "flag" in response:
                    if response["flag"] == "Success":
                        db_update_status = self.update_status( emailId, adminId)
                        if db_update_status != 1:
                            logger.error("Error in ProcessorDB update_status")
                        return db_update_status
                else:
                    return response['message']
            return -2
        except:
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # append batch Id to batch_assigned field in the ProcessorDb Database
    def assign_batch(self, pId, adminId, bId, kwargs={}, logger=None):
        try:
            #Check if Processor already exists.
            if(self.existId(pId, adminId)):
                cond = and_(ProcessorSchema.id == pId, ProcessorSchema.adminId == adminId)
                self.session.query(ProcessorSchema).filter(cond).\
                        update({ProcessorSchema.batch_assigned: func.array_append(ProcessorSchema.batch_assigned, bId)}, synchronize_session = False)
                self.session.query(ProcessorSchema).filter(cond).update({ProcessorSchema.pending_count:ProcessorSchema.pending_count+1})
                self.session.commit()
                return 1
            #Processor not found
            else:
                return -1
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # get count of pending batchs for the given processor
    def get_pending_count(self, pId, adminId, kwargs={}, logger=None):
        try:
            #Check if Processor already exists.
            #pId = self.getId(emailId, adminId)
            if(self.existId(pId, adminId)):
                cond = and_(ProcessorSchema.id == pId, ProcessorSchema.adminId == adminId)
                processor = self.session.query(ProcessorSchema).filter(cond).first()
                if processor:
                    return processor.pending_count
            #Processor not found
            else:
                return -2
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # get list of Processor mapped to the queues
    def get_all_processor_in_queue(self, qId, adminId, kwargs={}, logger=None):
        try:
            cond = and_(MapQueuesProcessor.queuesId == qId, MapQueuesProcessor.adminId == adminId)
            processors = self.session.query(MapQueuesProcessor).filter(cond).all()
            # processors = [] means no processor is mapped to that queue
            processor_list = []
            for processor in processors:
                processor_list.append(processor.processorId)
            return processor_list ,1
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return [], -2
            
    # when batches get deleted remove it from batch_assigned in processor Database
    def remove_batch(self, bId, pId, adminId, processor_email, status, kwargs={}, logger=None):
        try:
            cond = and_(ProcessorSchema.id == pId , ProcessorSchema.adminId == adminId)
            self.session.query(ProcessorSchema).filter(cond).\
                update({ProcessorSchema.batch_assigned: func.array_remove(ProcessorSchema.batch_assigned, bId)}, synchronize_session = False)

            if status == "To Be Reviewed" or status == "Uploaded":
                self.session.query(ProcessorSchema).filter(cond).update({ProcessorSchema.pending_count : ProcessorSchema.pending_count - 1})
            if status == "Reviewed" or status == "Straight Through":
                self.session.query(ProcessorSchema).filter(cond).update({ProcessorSchema.review_count : ProcessorSchema.review_count - 1})
                
            self.session.commit()
            return 1
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    