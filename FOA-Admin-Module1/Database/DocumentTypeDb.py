"""
Description : Handling DocumentType Table Creation, Deletion, Display and Other Functionalities.
* Necessary Code Comments for function description added before the function definition.
"""

import traceback
from sqlalchemy import or_, and_, func

from Database.schema import DocumentTypeSchema, MapAdminDocType, MapFieldDocType,MapQueuesDocument, QueuesSchema, FieldsSchema
from Database import Session

#session = Session()

from Database.QueuesDb import QUEUESDB
queuesDb = QUEUESDB()

from Database.AdminDb import ADMINDB
o_adminDb = ADMINDB()

from Database.FieldsDb import FIELDSDB
o_fieldsDb = FIELDSDB()

class DOCUMENTDB:
    def __init__(self, kwargs={}, logger=None):
        self.session = Session()

    #BASIC FUNCTIONALITIES
    # insert - For Inserting a New DocumenType in the Database.
    """
    def insert(self, doc_name, description, fieldsId, adminId, kwargs={}, logger=None):
        try:
            name = doc_name.lower().replace(" ","_")
            #Insert Only when DocumentType doesn't already exists.
            if self.getId(name, adminId) == -1:
                p1 = DocumentTypeSchema(name,doc_name, description, fieldsId, adminId)
                self.session.add(p1)
                self.session.commit()
                return 1
            return -1
        except:
            self.session.rollback()
            return -2
    """

    def insert(self, doc_name, description, fieldIds, adminId, kwargs={}, logger=None):
        try:
            name = doc_name.lower().replace(" ","_")
            #Insert Only when DocumentType doesn't already exists.
            if self.getId(name, adminId) == -1:

                # Inserting DocumentType
                p1 = DocumentTypeSchema(name,doc_name, description, adminId)
                self.session.add(p1)
                self.session.commit()
                
                # Create a mapping between admin and doctype
                #self.session.refresh(p1)
                docTypeId = p1.id
                map_response = self.map_admin(adminId, docTypeId)
                # print("admin map response: ", map_response)
                if map_response != 1:
                    return -2, -2

                # Creating a mapping between fields and docType
                map_response = self.map_fields(docTypeId, fieldIds, adminId)
                # print("field map response: ", map_response)
                if map_response != 1:
                    return -2, -2

                # print("docTypeId: ", docTypeId)
                return docTypeId, 1
            return -1, -1
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2, -2

    # map - Mapping docType with admin
    def map_admin(self, adminId, docTypeId, kwargs={}, logger=None):
        try: 
            # Checking if Admin Exists
            if o_adminDb.check_if_exists(adminId):
                self.session.add(MapAdminDocType(docTypeId=docTypeId, adminId =adminId))
                self.session.commit()
                return 1
            # Either Admin or DocumentType doesnot exists
            return -1
        except:
            self.session.rollback()
            print(traceback.print_exc())
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # is_mapped - Checking if Admin and DocType is mapped from MapAdminDocType Table.
    def is_mapped_field(self, docTypeId, fId, adminId, kwargs={}, logger=None):
        try:
            cond = and_(MapFieldDocType.docTypeId == docTypeId, MapFieldDocType.fieldId == fId, MapFieldDocType.adminId == adminId)
            fielddocType = self.session.query(MapFieldDocType).filter(cond)
            return self.session.query(fielddocType.exists()).scalar()
        except:
            self.session.rollback()
            print(traceback.print_exc())
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # map_fields - Mapping fields with documentType(s).
    def map_fields(self, docTypeId, field_ids, adminId, kwargs={}, logger=None):
        try:
            # Checking if DocType Exists
            if self.existId(docTypeId, adminId):
                for fId in field_ids:
                    # Checking if field exists and mapped to the docType already.
                    if o_fieldsDb.existId(fId, adminId) and not self.is_mapped_field(docTypeId,fId,adminId, kwargs={}, logger=None):
                        self.session.add(MapFieldDocType(docTypeId = docTypeId , fieldId = fId, adminId = adminId, threshold=0.85))
                self.session.commit()
                return 1
             # Either Field or DocType not exists.
            return -1 
        except:
            self.session.rollback()
            print(traceback.print_exc())
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # unmap_fields - UnMapping fields with documentType(s).
    def unmap_fields(self, docTypeId, field_ids, adminId, kwargs={}, logger=None):
        # print("Unmap Fields")
        try:
            # Checking if DocType Exists
            if self.existId(docTypeId, adminId):
                for fId in field_ids:
                    # print("fId: ", fId, o_fieldsDb.existId(fId, adminId), self.is_mapped_field(docTypeId,fId,adminId))
                    # Checking if field exists and mapped to the docType already.
                    if o_fieldsDb.existId(fId, adminId) and self.is_mapped_field(docTypeId,fId,adminId):
                        cond = and_(MapFieldDocType.docTypeId == docTypeId, MapFieldDocType.fieldId == fId, MapFieldDocType.adminId == adminId)
                        self.session.query(MapFieldDocType).filter(cond).delete()
                self.session.commit()
                return 1
             # Either Field or DocType not exists.
            return -1 
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2
    

    # delete - For Deleting a DocumentType in the Database.
    def delete(self, id, adminId, kwargs={}, logger=None):
        try:
            # Checking if the documentType Id exists to delete.
            if(self.existId(id, adminId)):
                if (self.is_default(id) == False):
                    cond = and_(DocumentTypeSchema.id == id, DocumentTypeSchema.type == adminId)
                    self.session.query(DocumentTypeSchema).filter(cond).delete()
                    self.session.commit()
                    return 1
            # documentType not found or a default documentType
            return -1      
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2
      
    # update - For Updating a documentType
    def update(self,id, doc_name, description, new_fieldIds, adminId, kwargs={}, logger=None):
        try:
            # Checking if the documentType Id exists to edit it.
            if(self.existId(id, adminId)):
                response = self.update_fields(id, adminId, new_fieldIds)
                #response = self.update_fieldlist(id, adminId, new_fieldIds)
                if(response == 1):
                    cond = and_(DocumentTypeSchema.id == id, DocumentTypeSchema.type == adminId)
                    self.session.query(DocumentTypeSchema).filter(cond).update({DocumentTypeSchema.doc_name:doc_name, DocumentTypeSchema.description:description})
                    self.session.commit()
                    return 1
            # documentType not found or a default documentType
            return -1      
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    """
    # display - Displaying the available DocumentTypes for the specified admin.
    def display(self, adminId, kwargs={}, logger=None):
        try:
            cond = or_(DocumentTypeSchema.type == adminId, DocumentTypeSchema.type == 'default')
            documents = self.session.query(DocumentTypeSchema).filter(cond).order_by(DocumentTypeSchema.id.desc())
            response = {}
            document_list = []
            if(documents, kwargs={}, logger=None):
                for document in documents:
                    results = {}
                    results['id']= document.id
                    results["name"] = document.doc_name
                    results["description"] = document.description
                    results['fieldsId'] = document.fieldsId
                    results['fields_count'] = len(document.fieldsId)
                    queue_count = self.get_queuescount(document.id, adminId)
                    queues_mapped = self.mappedQueues(document.id, adminId)
                    fields_name = self.fieldsName(document.fieldsId, adminId)
                    if queue_count != -2 and queues_mapped != -2 and fields_name != -2:
                        results['fields'] = fields_name
                        results['queues_count'] = queue_count
                        results['mapping'] = {}
                        for queue in queues_mapped:
                            results['mapping'][queue] = "Yes"
                    else:
                        return -2
                    document_list.append(results)
            response["Documents"] = document_list
            response["Total Documents"] = len(document_list)
            return response
        except:
            self.session.rollback()
            return -2
    """

    def get_docTypes_for_admin(self, adminId, kwargs={}, logger=None):
        try:
            cond = MapAdminDocType.adminId == adminId
            admindocTypes = self.session.query(MapAdminDocType).filter(cond).all()
            docTypeIds = [admindocType.docTypeId for admindocType in admindocTypes]
            return docTypeIds
        except:
            self.session.rollback()
            print(traceback.print_exc())
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    def display(self, adminId, kwargs={}, logger=None):
        try:
            response = {}
            document_list = []

            docTypeIds = self.get_docTypes_for_admin(adminId)

            if docTypeIds != -2:
                for docTypeId in docTypeIds:
                    cond = DocumentTypeSchema.id == docTypeId
                    document = self.session.query(DocumentTypeSchema).filter(cond).first()
                    results = {}
                    results['id']= document.id
                    results["name"] = document.doc_name
                    results["description"] = document.description
                    
                    fields_count, field_ids, field_names = self.get_mappedFields(document.id, adminId)
                    
                    results['fields_count'] = fields_count
                    results['fieldsId'] = field_ids
                    results['fields'] = field_names

                    queue_count = self.get_queuescount(document.id, adminId)
                    queues_mapped = self.mappedQueues(document.id, adminId)

                    if queue_count != -2 and queues_mapped != -2:
                        results['queues_count'] = queue_count
                        results['mapping'] = {}
                        for queue in queues_mapped:
                            results['mapping'][queue] = "Yes"
                    else:
                        return -2
                    document_list.append(results)

            response["Documents"] = document_list
            response["Total Documents"] = len(document_list)
            return response
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    #OTHER FUNCTIONALITIES
    # getId - Getting the Id of the DocumentType from the Database.
    def getId(self, name, adminId, kwargs={}, logger=None):
        try:
            cond = and_(DocumentTypeSchema.name == name, DocumentTypeSchema.type == adminId)
            document = self.session.query(DocumentTypeSchema).filter(cond).first()
            if document:
                return document.id
            else:
                return -1    #documentType doesn't exists
        except:
            print(traceback.print_exc())
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # is_default - To check if the DocumentType is default.
    def is_default(self, fid, kwargs={}, logger=None):
        try:
            document = self.session.query(DocumentTypeSchema).filter(DocumentTypeSchema.id == fid).first()
            if (document.type == 'default'):
                return True
            else:
                return False
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return False

    # existId - Checking if the DocumentType Id already exists.
    def existId(self, id, adminId, kwargs={}, logger=None):
        try:
            cond = and_(DocumentTypeSchema.id ==id, or_(DocumentTypeSchema.type == adminId, DocumentTypeSchema.type == 'default'))
            document = self.session.query(DocumentTypeSchema).filter(cond)
            return self.session.query(document.exists()).scalar()  
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return False

    # is_mapped - Checking if Queue and DocumentType is mapped from MapQueuesDocument Table.
    def is_mapped(self, qId, dId, adminId, kwargs={}, logger=None):
        try:
            cond = and_(MapQueuesDocument.queuesId == qId, MapQueuesDocument.documentTypeId==dId, MapQueuesDocument.adminId==adminId)
            document = self.session.query(MapQueuesDocument).filter(cond)
            return self.session.query(document.exists()).scalar()
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return False

    # map - Mapping queue with documentType(s).
    def map(self, qId , document, adminId, kwargs={}, logger=None):
        try:
            # Checking if Queues Exists
            if queuesDb.existId(qId, adminId):
                for dId in document:
                    # Checking if documentType exists and mapped to the queue already.
                    if self.existId(dId, adminId) and not self.is_mapped(qId,dId,adminId):
                        self.session.add(MapQueuesDocument(queuesId = qId, documentTypeId = dId , adminId = adminId))
                self.session.commit()
                return 1
             # Either Queue or documentTypes not exists.
            return -1 
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2
    
    # unmap - UnMapping queue with documentType(s).
    def unmap(self, qId , document, adminId, kwargs={}, logger=None):
        try:
            # Checking if Queues Exists.
            if queuesDb.existId(qId,adminId):
                for dId in document:
                    # Checking if documentType exists and mapped to the queue.
                    if self.existId(dId, adminId) and self.is_mapped(qId, dId, adminId):
                        cond = and_(MapQueuesDocument.queuesId == qId, MapQueuesDocument.documentTypeId == dId, MapQueuesDocument.adminId == adminId)
                        self.session.query(MapQueuesDocument).filter(cond).delete()
                self.session.commit()
                return 1
            # Either Queue or documentTypes not exists.
            return -1   
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2
    
    """
    # delete_fields - Deleting a field Mapped to the documentType when a field is deleted.
    def delete_fields(self, fId, adminId, kwargs={}, logger=None):
        try:
            cond = and_(DocumentTypeSchema.fieldsId.any(fId), DocumentTypeSchema.type == adminId)
            self.session.query(DocumentTypeSchema).filter(cond).\
                update({DocumentTypeSchema.fieldsId: func.array_remove(DocumentTypeSchema.fieldsId, fId)}, synchronize_session = False)
            self.session.commit()
            return 1
        except:
            self.session.rollback()
            return -2
    """

    def update_fields(self, id, adminId, new_fieldIds, kwargs={}, logger=None):
        try:
            _, old_fieldIds, _  = self.get_mappedFields(id, adminId)

            unmap_elements      = list(set(old_fieldIds) - set(new_fieldIds))
            map_elements        = list(set(new_fieldIds) - set(old_fieldIds))

            map_response        = self.map_fields(id, map_elements, adminId)
            if map_response != 1:
                return -2

            unmap_response      = self.unmap_fields(id, unmap_elements, adminId)
            if unmap_response != 1:
                return -2

            return 1
        except:
            self.session.rollback()
            print(traceback.print_exc())
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    """
    # updating fields column in DocumentType table
    def update_fieldlist(self, id, adminId, new_fId, kwargs={}, logger=None):
        try:
            cond = and_(DocumentTypeSchema.id == id, or_(DocumentTypeSchema.type == adminId, DocumentTypeSchema.type == 'default'))
            document = self.session.query(DocumentTypeSchema).filter(cond).first()
            old_fId = document.fieldsId
            remove_elements = list(set(old_fId) - set(new_fId))
            append_elements = list(set(new_fId) - set(old_fId))
            for fId in remove_elements:
                self.session.query(DocumentTypeSchema).filter(cond).\
                        update({DocumentTypeSchema.fieldsId: func.array_remove(DocumentTypeSchema.fieldsId, fId)}, synchronize_session = False)
        
            for fId in append_elements:
                self.session.query(DocumentTypeSchema).filter(cond).\
                        update({DocumentTypeSchema.fieldsId: func.array_append(DocumentTypeSchema.fieldsId, fId)}, synchronize_session = False)
            return 1
        except:
            self.session.rollback()
            return -2
    """

    # get the count of queues mapped to the given document type
    def get_queuescount(self, id, adminId, kwargs={}, logger=None):
        try:
            cond = and_(MapQueuesDocument.documentTypeId == id, MapQueuesDocument.adminId == adminId)
            queue_count = self.session.query(func.count(MapQueuesDocument.queuesId)).filter(cond).scalar()
            return queue_count
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # get the fields mapped to the given document type
    def get_mappedFields(self, id, adminId, kwargs={}, logger=None):
        try:
            cond = and_(MapFieldDocType.adminId == adminId, MapFieldDocType.docTypeId == id)
            fieldsdocType = self.session.query(MapFieldDocType).filter(cond).all()

            fieldCount = len(fieldsdocType)

            fieldIds = []
            fieldNames = []
            
            if fieldsdocType:
                for fielddocType in fieldsdocType:
                    fieldIds.append(fielddocType.fieldId)

                    cond = and_(FieldsSchema.id == fielddocType.fieldId, or_(FieldsSchema.type == adminId, FieldsSchema.type == 'default'))
                    field = self.session.query(FieldsSchema).filter(cond).first()
                    fieldNames.append(field.field_name)

                return fieldCount, fieldIds, fieldNames

            return 0, [], []
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # get the queues mapped to the given document type
    def mappedQueues(self, id, adminId, kwargs={}, logger=None):
        try:
            cond = and_(MapQueuesDocument.documentTypeId == id, MapQueuesDocument.adminId == adminId)
            queues = self.session.query(MapQueuesDocument).filter(cond).all()
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
    
    def fieldsName(self, fields_id, adminId, kwargs={}, logger=None):
        try:
            cond = or_(FieldsSchema.type == adminId, FieldsSchema.type == 'default')
            fields = self.session.query(FieldsSchema).filter(cond).order_by(FieldsSchema.id.desc())
            results = []
            if fields:
                for field in fields:
                    if field.id in fields_id:
                        # results.append({"id": field.id, "name": field.field_name})
                        results.append(field.field_name)
            return results
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2
    def check_ifexists(self,name,default_flag,kwargs={}, logger=None):
        try:
            if default_flag==True:
                default_flag='default'
            cond=and_(DocumentTypeSchema.name==name,DocumentTypeSchema.type==default_flag)
            doc = self.session.query(DocumentTypeSchema).filter(cond)
            is_exists=self.session.query(doc.exists()).scalar() 
            self.session.commit()
            return is_exists
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return False

