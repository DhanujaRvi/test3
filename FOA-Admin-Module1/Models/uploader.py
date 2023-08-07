"""
Description : Serves as the ADAPTER function for all Upload Center functionalities.
"""

import os
import shutil
import traceback

from Database.BatchDb import BATCHDB
batchDb = BATCHDB()

from Database.QueuesDb import QUEUESDB
queuesDb = QUEUESDB()

from Adapter.file_saver import FILESAVERADAPTER
o_filesaver = FILESAVERADAPTER()

from Database.ProcessorDb import PROCESSORDB
processorDb  = PROCESSORDB()


class UPLOADER:
    def __init__(self):
        pass

    # Function for uploading the batch
    def upload(self, queuesId, admin_id, admin_email, uploaded_files, auth_headers, auth_type, processor_batch_limit, kwargs, logger):
        try:
            # Generate batch id for each admin
            batch_id = batchDb.generate_batch_id(admin_id)
            batch_name = "BID"+str(batch_id)
            logger.info("UID: "+str(kwargs["uid"]))
            # print("batchId", batch_id)
            logger.info("batchId: "+ str(batch_id))
            
            # Insert uploaded details in batchDb
            insert_response = batchDb.insert(batch_id, batch_name, admin_id, admin_email)
            # print("insert_response: ", insert_response)
            logger.info("insert_response: "+ str(insert_response))
            if insert_response == -2:
                logger.error("Error in insert functionality of the BatchDb")
                return -2, -2, -2

            # get unique batch Id
            bId = batchDb.get_id(batch_id, admin_id)          

            # Check if the queue has atleast one document type mapped
            if queuesDb.get_documentcount(queuesId, admin_id) < 1: 
                status = "InComplete"
                # print("DocumentType not Mapped")
                logger.error("DocumentType not Mapped")
                batchDb.update_status(bId, admin_id, status)
                return -2, -2, -2

            # Map queues to batches
            batch_map_response = batchDb.map(queuesId, bId, admin_id )
            if batch_map_response == -2:
                # print("Batch Queue Mapping Error")
                logger.error("Batch Queue Mapping Error")
                status = "InComplete"
                batchDb.update_status(bId, admin_id, status)
                return -2, -2, -2

            # get queue where the batch has been uploaded and get the document type assigned to that queue
            _, _, doc_type = batchDb.get_queue_document(bId)  
            if len(doc_type) == 1:      
                default_docType = str(min([int(key) for key in doc_type.keys()]))
            elif len(doc_type) > 1:
                default_docType = 0

            # Assign processor to batch based on constraints
            response  = self.assign_processor(queuesId, bId, admin_id, processor_batch_limit, kwargs, logger)
            # print("Processor Assignment Response: ", response)
            logger.info("Processor Assignment Response: "+ str(response))

            if response != -2:
                # Store the files in local
                file_path = self.store_files(uploaded_files, bId)
                files=[]
                for file in file_path:
                    files.append(('file', open(file, 'rb')))

                # Internal API call to processor module to save files and assign jobs 
                status_code = o_filesaver.save(admin_id, bId, files, auth_headers, auth_type, default_docType) 
                if status_code == 200:
                    # If files are sucessfully stored in Processor delete those files from admin side
                    self.delete_files(bId) 
                    status = "Uploaded"
                    batchDb.update_status(bId, admin_id, status)
                    return bId, batch_name, 1
                else:
                    # print("File Saver Failed")
                    logger.error("File Saver Failed")
                    status = "InComplete"
                    batchDb.update_status(bId, admin_id, status)
                    return -2, -2, -2

            if response == 2:
                status = "Waiting"
                batchDb.update_status(bId, admin_id, status)

            status = "InComplete"
            batchDb.update_status(bId, admin_id, status)
            logger.error("Error in Processor Assignment of the Batch.")
            return -2, -2, -2
        except:
            logger.info("Exception has occured, UID: "+str(kwargs["uid"]), exc_info=1)
            return -2, -2, -2

    # Function for temporarily storing uploaded files on the admin side
    def store_files(self, uploaded_files, bId):
        uploaded_files = list(uploaded_files._iter_hashitems())
        
        file_path = []
        folder_name = "Batch_" + str(bId)
        folder_path = os.path.join("./static", folder_name)
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
        os.makedirs(folder_path)

        print("-----------UPLOADED FILES---------- ")
        for file_ind, (_, files_sent) in enumerate(uploaded_files):
            file_name = files_sent.filename
            file_name = file_name.encode('ascii', 'ignore').decode()
            file_name = file_name.replace(" ", "")
            print(" --- ",file_name)
            
            splited_text = os.path.splitext(file_name)
            file_name = splited_text[0]+splited_text[1]
            
            files_sent.save(os.path.join(folder_path, file_name))
            file_path.append(os.path.join(folder_path, file_name))

        return file_path
    
    # Function to delete temporarily stored files in admin side
    def delete_files(self, bId):
        folder_name = "Batch_" + str(bId)
        folder_path = os.path.join("./static", folder_name)
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
        

    # Function to assign processor under queues to the batch based on constraints
    def assign_processor(self,queuesId, bId, admin_id, processor_batch_limit, kwargs, logger):
        logger.debug("ENTERING ASSIGN PROCESSOR FUNCTIONALITY.")

        try:
            processor_list, response = processorDb.get_all_processor_in_queue(queuesId, admin_id, logger=logger)
            
            if response !=-2:
                if len(processor_list) > 0:

                    pending_count = [processorDb.get_pending_count(pId, admin_id, logger=logger) for pId in processor_list]
                    logger.debug("Pending Count: {}".format(pending_count))
                    
                    idx = pending_count.index(min(pending_count))

                    if pending_count[idx] < processor_batch_limit:
                        selected_processorId = processor_list[idx]   
        
                        assignment_response = processorDb.assign_batch(selected_processorId, admin_id, bId, logger=logger)
                        if assignment_response == -2:
                            error_message = "Assigning Batch {} to Processor {} for Admin {} Failed.".format(bId, selected_processorId, admin_id)
                            logger.error(error_message)
                            return -2
                        elif assignment_response == -1:
                            error_message = "Processor {} Doesn't Exists.".format(selected_processorId)
                            logger.error(error_message)
                            return -2
                        else:
                            message = "Assigned Batch {} to Processor {}.".format(bId, selected_processorId)
                            logger.debug(message)

                        processor_email = processorDb.getemailId(selected_processorId, admin_id, logger=logger)
                        if processor_email == -2:
                            error_message = "Getting Mail Id for Processor {} Failed.".format(selected_processorId)
                            logger.error(error_message)
                            return -2

                        response = batchDb.assign_processor(processor_email, admin_id, bId, logger=logger)
                    
                        if response == -2:
                            error_message = "Assigning Processor {} to Batch {} for Admin {} Failed.".format(selected_processorId, bId, admin_id)
                            logger.error(error_message)
                            return -2
                        
                        return 1
                    
                    else:
                        return 2
                
                return 1
            
            else:
                error_message = "Getting All Processor in Queue {} -- Admin {} Failed.".format(queuesId, admin_id)
                logger.error(error_message)
                return -2
        
        except Exception as e:
            print(traceback.print_exc())
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # Function to display all batches in the upload center
    def batch_display(self, admin_id, processor_batch_limit, version, input_parameters, kwargs, logger):
        logger.debug("ENTERING BATCH DISPLAY FUNCTIONALITY.")

        try:
            # Check if there is any batch with no processors assigned, if so try to assign one.
            batches, batch_response = batchDb.check_processor_assignment(admin_id, logger=logger)
            
            if batch_response != -2:
                if len(batches) > 0:
                    for bId, qId in batches:
                        if qId != -2:
                            response = self.assign_processor(qId, bId, admin_id, processor_batch_limit, kwargs, logger) 
                            
                            if response == 1:
                                status = "Uploaded"
                                batchDb.update_status(bId, admin_id, status, logger=logger)
                            elif response == 2:
                                status = "Waiting"
                                batchDb.update_status(bId, admin_id, status, logger=logger)

            return batchDb.display(admin_id, version, input_parameters, logger=logger)
        
        except Exception as e:
            print(traceback.print_exc())
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2