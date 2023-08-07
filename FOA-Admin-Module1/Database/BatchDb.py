"""
Description : Handling Batch Table Creation, Deletion, Display and Other Functionalities.
* Necessary Code Comments for function description added before the function definition.
"""

from sqlalchemy import or_, and_, desc

from Database.schema import BatchDbSchema, MapQueuesBatch, QueuesSchema, DocumentTypeSchema,\
    MapQueuesDocument
from Database import Session
#session = Session()

from Database.QueuesDb import QUEUESDB
queuesDb= QUEUESDB()

from Database.ProcessorDb import PROCESSORDB
processorDb = PROCESSORDB()

import datetime
from pytz import timezone
import traceback

class BATCHDB():
    def __init__(self):
        self.session = Session()
    
    #BASIC FUNCTIONALITIES
    # insert - For Inserting a New Field to the Database.
    def insert(self, batch_id, batch_name, admin_id, admin_email, kwargs={}, logger=None):
        try:
            dtime = self.format_date()
            status = "Uploading"
            f1 = BatchDbSchema(batch_id,batch_name,admin_id,admin_email, dtime, status)
            self.session.add(f1)
            self.session.commit()
            return 1
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2
    
    def find_assignedprocessor(self, bId, adminId, kwargs={}, logger=None):
        try:
            cond = and_(BatchDbSchema.id == bId, BatchDbSchema.adminId == adminId)
            batch = self.session.query(BatchDbSchema).filter(cond).first()

            if batch:
                assigned_to = batch.assignedTo
                self.session.commit()
                return assigned_to
            else:
                return -2
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # delete - For Deleting a Batch in the Database.
    def admin_batch_delete(self, bIds, adminId, user_email, kwargs={}, logger=None):
        try:
            for bId in bIds:
                assigned_processor = self.find_assignedprocessor(bId, adminId)
                cond = and_(BatchDbSchema.id == bId, BatchDbSchema.adminId == adminId)

                if assigned_processor != "None" and assigned_processor !=-2:
                    pId = processorDb.getId(assigned_processor, adminId)
                    batch = self.session.query(BatchDbSchema).filter(cond).first()
                    status = batch.status
                    response = processorDb.remove_batch(bId, pId, adminId, user_email, status)

                    if response == -2:
                        logger.error("Error in removing Batch from the ProcessorDB")
                        return -2    
                
                self.session.query(BatchDbSchema).filter(cond).delete()
                self.session.commit()

            return 1
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # get_adminId - Get Admin of the Batch
    def get_adminId(self, bId, kwargs={}, logger=None):
        try:
            batch = self.session.query(BatchDbSchema).filter(BatchDbSchema.id == bId).first()
            adminId = batch.adminId
            self.session.commit()
            return adminId
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    def processor_batch_delete(self, bIds, user_id, user_email, kwargs={}, logger=None):
        try:
            for bId in bIds:
                assigned_processor = user_email
                adminId = self.get_adminId(bId)

                cond = and_(BatchDbSchema.id == bId, BatchDbSchema.adminId == adminId)
                # print("assigned_processor",assigned_processor)
                
                if assigned_processor != "None":
                    pId = processorDb.getId(assigned_processor, adminId)
                    # print("pid",pId)

                    batch = self.session.query(BatchDbSchema).filter(cond).first()
                    status = batch.status    
                    # Removing Batch from the Processor
                    response = processorDb.remove_batch(bId, pId, adminId, user_email, status)

                    if response == -2:
                        logger.error("Error in removing Batch from the ProcessorDB")
                        return -2
                self.session.query(BatchDbSchema).filter(cond).delete()
                self.session.commit()
                
            return 1
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # Function to display batchs as required by FrontEnd.
    def display(self, adminId, version, input_parameters, kwargs={}, logger=None):
        try:
            # Internal Function of Function.
            # This is used as a common function for both the versions 'v3.0' and 'v3.1'
            # since there are no changes in the batch response.
            def get_batch_list(batches):
                try:
                    batch_list = []
                    for batch in batches:
                        # print(batch)
                        results = {}

                        results["id"] = batch.id
                        results["batch_id"] = batch.batch_id
                        results["batch_name"] = batch.batch_name
                        results["uploaded_dateTime"] = str(batch.uploaded_dateTime).replace("GMT", "") + " IST"
                        results["channel"] = batch.channel
                        results["assigned_to"] = batch.assignedTo
                        results["status"] = batch.status
                        results["job_ids"] = batch.job_ids
                        
                        if batch.status != "InComplete":
                            queue = self.get_queue(batch.id, adminId)
                            jobs_count = self.get_jobcount(batch.id, adminId)
                            print("ID",batch.id)
                            print("Que",queue)
                            print("Job Count",jobs_count)
                            if jobs_count != -2 and queue != -2:
                                results["jobs_count"] = jobs_count
                                results["queue"] = queue
                            else:
                                return -2
                        else:
                            results["queue"] = "None"
                            results["jobs_count"] = 0

                        batch_list.append(results)
                    return batch_list
                except:
                    print(traceback.print_exc())
            # Outer Function starts
            
            # Querying to get all the batches and arranging them in the descending order
            # (recent uploads to old uploads) based on the upload dateTime
            cond = BatchDbSchema.adminId == adminId
            batches = self.session.query(BatchDbSchema).filter(cond).order_by(desc(BatchDbSchema.uploaded_dateTime)).all()

            if version == 'v3.0':
                """
                API Method is "GET"
                """
                response = {}
                batch_list = []
                if batches:
                    batch_list = get_batch_list(batches)
                        
                response["Batch"] = batch_list
                response["total_batches"] = len(batch_list)

            elif version == 'v3.1':
                """
                Description: Pagination is implemented.
                API Method is "POST"
                Output Response is changed.
                {
                    "Batch" : []
                    "total_batches": 0
                }
                """

                response = {}
                batch_list = []

                page_no = int(input_parameters.get('page_no'))
                rows_per_page = int(input_parameters.get('rows_per_page'))
                #print("Batches",batches)
                if batches:
                    # Getting the Total No. of Batches.
                    total_batch = len(batches)

                    # Finding the Start and End of the Batch Indices.
                    start = (page_no-1) * rows_per_page
                    end = min(page_no*rows_per_page, total_batch)

                    batch_list = get_batch_list(batches[start:end])

                # Assigning all the Batches that are required in the output response.
                response["Batch"] = batch_list
                # Assigning the Total Number of Batches that are required in the output response..
                response["total_batches"] = total_batch

            return response
        except:
            print(traceback.print_exc())
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    #OTHER FUNCTIONALITIES
    # Function for formating date and time as required by front End
    def format_date(self, kwargs={}, logger=None):
        try:
            date_format = "%Y-%m-%d %H:%M"
            IST = timezone('Asia/Kolkata')
            datetime_ist = datetime.datetime.now(IST)
            exported_time = datetime_ist.strftime(date_format)
            return exported_time
        except:
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2
    
    # existId - Checking if the Batch Id already exists.
    def existId(self, id, adminId, kwargs={}, logger=None):
        try:
            cond = and_(BatchDbSchema.id == id, BatchDbSchema.adminId == adminId)
            batch = self.session.query(BatchDbSchema).filter(cond)
            return self.session.query(batch.exists()).scalar()  
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return False

    # Function to Generate batch Id for each Admin
    def generate_batch_id(self, adminId, kwargs={}, logger=None):
        try:
            if self.existAdmin(adminId):
                batch = self.session.query(BatchDbSchema).filter(BatchDbSchema.adminId == adminId).order_by(BatchDbSchema.batch_id.desc()).first()
                batch_id = batch.batch_id
                return batch_id + 1
            else:
                self.session.rollback()
                return 1
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # existAdmin - Checking if the adminId already exists in BatchDb Database
    def existAdmin(self, adminId, kwargs={}, logger=None):
        try:
            job = self.session.query(BatchDbSchema).filter(BatchDbSchema.adminId == adminId)
            val = self.session.query(job.exists()).scalar() 
            self.session.commit() 
            return val
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return False

    # update job details of batch in the Database
    def update_jobdetails(self, bId, admin_id, job_ids, batch_size, kwargs={}, logger=None):
        try:
            cond = and_(BatchDbSchema.id == bId, BatchDbSchema.adminId == admin_id)
            self.session.query(BatchDbSchema).filter(cond).update({BatchDbSchema.job_ids:job_ids, BatchDbSchema.batch_size:batch_size})
            self.session.commit()
            return 1
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2
    
    # update status of batch in the Database
    def update_status(self, bId, admin_id, status, kwargs={}, logger=None):
        try:
            cond = and_(BatchDbSchema.id == bId, BatchDbSchema.adminId == admin_id)
            self.session.query(BatchDbSchema).filter(cond).update({BatchDbSchema.status:status})
            self.session.commit()
            return 1
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    def update_pending(self, bId, admin_id, status, kwargs={}, logger=None):
        try:
            cond = and_(BatchDbSchema.id == bId, BatchDbSchema.adminId == admin_id)
            self.session.query(BatchDbSchema).filter(cond).update({BatchDbSchema.pending:status})
            self.session.commit()
            return 1
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # get unique id of the batch using batch id and admin id from the Database
    def get_id(self, batch_id, admin_id, kwargs={}, logger=None):
        try:
            cond = and_(BatchDbSchema.batch_id == batch_id, BatchDbSchema.adminId == admin_id)
            batch = self.session.query(BatchDbSchema).filter(cond).first()
            id = batch.id
            self.session.commit()
            return id
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # map - Mapping queue with batch.
    def map(self, qId , bId, adminId, kwargs={}, logger=None):
        try:
            if queuesDb.existId(qId, adminId):
                self.session.add(MapQueuesBatch(queuesId = qId, batchId = bId, adminId = adminId))
                self.session.commit()
                return 1 
            else:
                return -2
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2
    
    # get name of the queue in which the batch has been uploaded
    def get_queue(self, batchId, adminId, kwargs={}, logger=None):
        try:
            cond = and_(MapQueuesBatch.batchId == batchId, MapQueuesBatch.adminId == adminId)
            qb = self.session.query(MapQueuesBatch).filter(cond).first()
            if qb!=None:
                queueId = qb.queuesId
                queueName = queuesDb.get_queuename(queueId)
                self.session.commit()
            else:
                queueName='None'
            return queueName
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2
    
    # get batch id assigned to the queue
    def get_batchs(self, queueId, adminId, kwargs={}, logger=None):
        try:
            cond = and_(MapQueuesBatch.queuesId == queueId, MapQueuesBatch.adminId == adminId)
            batchs = self.session.query(MapQueuesBatch).filter(cond).all()
            bIds = []
            for batch in batchs:
                bId = batch.batchId
                bIds.append(bId)
            return bIds
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # get id of the queue in which the batch has been uploaded
    def get_queueId(self, batchId, adminId, kwargs={}, logger=None):
        try:
            cond = and_(MapQueuesBatch.batchId == batchId, MapQueuesBatch.adminId == adminId)
            qb = self.session.query(MapQueuesBatch).filter(cond).first()
            queueId = qb.queuesId
            return queueId
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # assign processor to the batch by updating the assignedTo field in the Database
    def assign_processor(self, processor_email, adminId, bId, kwargs={}, logger=None):
        try:
            dtime = self.format_date()
            cond = and_(BatchDbSchema.id == bId, BatchDbSchema.adminId == adminId)
            self.session.query(BatchDbSchema).filter(cond).update({BatchDbSchema.assignedTo:processor_email, BatchDbSchema.received_dateTime:dtime})
            self.session.commit()
            return 1
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # get count of the files (invoices) uploaded as a batch
    def get_jobcount(self, id, adminId, kwargs={}, logger=None):
        try:
            cond = and_(BatchDbSchema.id == id, BatchDbSchema.adminId == adminId)
            batch = self.session.query(BatchDbSchema).filter(cond).first()
            jobs_count = len(batch.job_ids)
            return jobs_count
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # gives list of batches which has not assigned any processor (Due to un availability of processor mapped to queue at that time )
    def check_processor_assignment(self, adminId, kwargs={}, logger=None):
        try:
            cond = and_(BatchDbSchema.adminId == adminId, BatchDbSchema.assignedTo == "None", BatchDbSchema.status != "InComplete")
            batchs = self.session.query(BatchDbSchema).filter(cond).all()
            batch_ids = [batch.id for batch in batchs]
            
            result = [(bId, self.get_queueId(bId, adminId)) for bId in batch_ids]
            return result , 1
        except Exception as e:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return [] , -2

    # get_queue_document - get name of the queue in which the batch has been uploaded &  get the  document type mapped to the given queues
    def get_queue_document(self, bId, kwargs={}, logger=None):
        try:
            cond = and_(MapQueuesBatch.batchId == bId)
            qb = self.session.query(MapQueuesBatch).filter(cond).first()
            queueId = qb.queuesId
        
            queue = self.session.query(QueuesSchema).filter(QueuesSchema.id == queueId).first()
            queueName =  queue.name

            cond = and_(MapQueuesDocument.queuesId == queueId)
            documents = self.session.query(MapQueuesDocument).filter(cond).all()
            doc_type = {}

            if documents:
                for document in documents:
                    dId = document.documentTypeId
                    doc = self.session.query(DocumentTypeSchema).filter(DocumentTypeSchema.id == dId).first()
                    doc_type[dId] = doc.doc_name

            return queueId, queueName, doc_type
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2
    