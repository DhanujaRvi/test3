"""
Description : Handling Queues Table Creation, Deletion, Display and Other Functionalities.
* Necessary Code Comments for function description added before the function definition.
"""

from sqlalchemy import or_, and_, func

from Database.schema import QueuesSchema, MapQueuesDocument, MapQueuesProcessor, MapQueuesBatch, DocumentTypeSchema, ProcessorSchema
from Database import Session

class QUEUESDB():
    def __init__(self):
        self.session = Session()

    #BASIC FUNCTIONALITIES
    # insert - For Inserting a New Queue in the Database.
    def insert(self, name, adminId, kwargs={}, logger=None):
        try:
            #Insert Only when Queue doesn't already exists.
            if self.getId(name, adminId) == -1:
                p1 = QueuesSchema(name, adminId)
                self.session.add(p1)
                self.session.commit()
                return 1
            else:
                return -1
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # Delete - For Deleting a Queue in the Database.
    def delete(self, id, adminId, kwargs={}, logger=None):
        try:
            # Checking if the Queue Id exists to delete.
            if(self.existId(id ,adminId)):
                cond = and_(QueuesSchema.id == id, QueuesSchema.adminId == adminId)
                self.session.query(QueuesSchema).filter(cond).delete()
                self.session.commit()
                return 1
            else:
                # queue not found 
                return -1         
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # Update - For Updating a Queue
    def update(self, id, name, adminId, kwargs={}, logger=None):
        try:
            #Edit Only when Queue already exists.
            if(self.existId(id, adminId)):
                cond = and_(QueuesSchema.id == id, QueuesSchema.adminId == adminId)
                self.session.query(QueuesSchema).filter(cond).update({QueuesSchema.name:name})
                self.session.commit()
                return 1
             # Queue not found
            else:
                return -1
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    #display - Displaying the available Queues for the specified admin.
    def display(self, adminId, kwargs={}, logger=None):
        try:
            cond = and_(QueuesSchema.adminId == adminId)
            queues = self.session.query(QueuesSchema).filter(cond).all()
            
            response = {}
            queues_list = []
            print("QUEUES",queues)
            if queues:
                for queue in queues:
                    results = {}
                    results["id"] = queue.id
                    results["name"] = queue.name
                    processor_count = self.get_processorcount(queue.id, adminId)
                    batch_count = self.getbatchcount(queue.id, adminId)
                    document_count = self.get_documentcount(queue.id, adminId)
                    documentTypes = self.get_MappeddocumentTypes(queue.id, adminId)
                    processorList = self.get_mapprocesorlist(queue.id, adminId)
                    if processor_count != -2 and document_count != -2 and processorList != -2 and documentTypes != -2 and batch_count != -2:
                        results['processor_count'] = processor_count
                        results['batch_count'] = batch_count
                        results['processor_list'] = processorList
                        results['documentType_count'] = document_count
                        results['documentTypes'] = documentTypes
                    else:
                        return -2
                    queues_list.append(results)
            response["Queues"] = queues_list
            response["Total Queues"] = len(queues_list)
            return response
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2
    
    #OTHER FUNCTIONALITIES
    # getId - Getting the Id of the Queue from the Database.
    def getId(self, name, adminId, kwargs={}, logger=None):
        try:
            cond = and_(QueuesSchema.name == name, QueuesSchema.adminId == adminId)
            queue = self.session.query(QueuesSchema).filter(cond)
            if self.session.query(queue.exists()).scalar() :
                return queue.id
            else:
                return -1     # queues not already exist
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # get the name of queue given id
    def get_queuename(self, id, kwargs={}, logger=None):
        try:
            queue = self.session.query(QueuesSchema).filter(QueuesSchema.id == id).first()
            return queue.name
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2
            
    # existId - Checking if the Queue Id already exists.
    def existId(self, id, adminId, kwargs={}, logger=None):
        try:
            queue = self.session.query(QueuesSchema).filter(QueuesSchema.id == id, QueuesSchema.adminId == adminId)
            return self.session.query(queue.exists()).scalar()  
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return False
    
    # get the count of processors for the given queue
    def get_processorcount(self, id, adminId, kwargs={}, logger=None):
        try:
            cond = and_(MapQueuesProcessor.queuesId == id, MapQueuesProcessor.adminId == adminId)
            processor_count = self.session.query(func.count(MapQueuesProcessor.processorId)).filter(cond).scalar()
            return processor_count
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2
    
    #get the count of batch for the given queue
    def getbatchcount(self, id, adminId, kwargs={}, logger=None):
        try:
            cond = and_(MapQueuesBatch.queuesId == id, MapQueuesBatch.adminId == adminId)
            batch_count = self.session.query(func.count(MapQueuesBatch.batchId)).filter(cond).scalar()
            return batch_count
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    #get the count of document types for the given queue
    def get_documentcount(self, id, adminId, kwargs={}, logger=None):
        try:
            cond = and_(MapQueuesDocument.queuesId == id, MapQueuesDocument.adminId == adminId)
            document_count = self.session.query(func.count(MapQueuesDocument.documentTypeId)).filter(cond).scalar()
            return document_count
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    #get the document type mapped to the given queue
    def get_MappeddocumentTypes(self, id, adminId, kwargs={}, logger=None):
        try:
            cond = and_(MapQueuesDocument.queuesId == id, MapQueuesDocument.adminId == adminId)
            documents = self.session.query(MapQueuesDocument).filter(cond).all()
            response = []
            if documents:
                for document in documents:
                    dId = document.documentTypeId
                    doc = self.session.query(DocumentTypeSchema).filter(DocumentTypeSchema.id == dId).first()
                    response.append(doc.name)
            return response
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # get the processor mapped to the given queue
    def get_mapprocesorlist(self, id, adminId, kwargs={}, logger=None):
        try:
            cond = and_(MapQueuesProcessor.queuesId == id, MapQueuesProcessor.adminId == adminId)
            processors = self.session.query(MapQueuesProcessor).filter(cond).all()
            response = []
            if processors:
                for processor in processors:
                    pId = processor.processorId
                    pro = self.session.query(ProcessorSchema).filter(ProcessorSchema.id == pId).first()
                    response.append(pro.name)
            return response
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2
    def check_ifexists(self,name,default_flag,kwargs={}, logger=None):
        try:
           
            cond=and_(QueuesSchema.name==name,QueuesSchema.default_flag==default_flag)
            queue= self.session.query(QueuesSchema).filter(cond)
            is_exists=self.session.query(queue.exists()).scalar() 
            self.session.commit()
            return is_exists
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return False


       

