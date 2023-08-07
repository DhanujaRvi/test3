"""
Description:

This file is for defining the Schema for all the required tables
Required Tables - Processor, Queues, DocumentType, Fields
Mapped Tables   - MapQueuesProcessor, MapQueuesDocument
"""

from sqlalchemy import Column, Integer, Float, String, Sequence, ARRAY, DateTime, func, Boolean, UniqueConstraint
from Database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

# Schema for Admin Table
class AdminSchema(Base):
    """
    id          : Unique Id assigned to each Admin
    emailId     : Email-ID of the Admin
    adminId     : User id from Ind-One
    default_processor : Email Id of default processor else NULL
    is_config   : Is config details available for the admin
    """

    __tablename__ = 'admin'

    admin_id_seq = Sequence('admin_id_seq', metadata=Base.metadata)
    id = Column(Integer,admin_id_seq, server_default=admin_id_seq.next_value())
    emailId = Column(String, nullable= False)
    adminId = Column(String, default = -1, primary_key=True)
    default_processor = Column(String)
    docType = relationship('DocumentTypeSchema', secondary='mapadmindoctype', overlaps='admin')
    is_config = Column(Boolean, default = False)
    
    def __init__(self, adminId, emailId):
        self.adminId = adminId
        self.emailId = emailId

# Schema for Processor Table
class ProcessorSchema(Base):
    """
    id              : Unique Id assigned to each Processor
    name            : Name of the Processor
    emailId         : Email-ID of the Processor
    role            : Role of the Processor
    status          : Status of user Registered with Ind-one (Active or Inactive)
    ind_id          : User id from Ind-One
    adminId         : ID (Admin) under whom the Processor belongs to
    queues          : Relationship defined between processor and queue
    batch_assigned  : List of BatchId assigned to this processor
    pending_count   : No of pending batches
    review_count    : No of reiewed or straight through batches
    default_flag    : Indicates whether the processor is created by default or not
    """

    __tablename__ = 'processor'
    
    processor_id_seq = Sequence('processor_id_seq', metadata=Base.metadata)
    id = Column(Integer,processor_id_seq, server_default=processor_id_seq.next_value(), primary_key=True)
    name = Column(String, nullable= False)
    emailId = Column(String, nullable= False)#, unique=True)
    role = Column(String, nullable= False)
    status = Column(String, nullable= False)
    indId = Column(Integer, default = -1)
    adminId = Column(String, nullable=False)
    queues = relationship('QueuesSchema', secondary = 'mapqueuesprocessor')
    batch_assigned = Column(ARRAY(Integer), server_default='{}')
    pending_count = Column(Integer, default = 0)
    review_count = Column(Integer, default = 0)
    UniqueConstraint('emailId', 'adminId', name='uniq_1')
    default_flag = Column(Boolean, default = False)

    def __init__(self, name, eId, role, status, aId, default=False):
        self.name = name
        self.emailId = eId
        self.role = role
        self.status = status
        self.adminId = aId
        self.default_flag = default
        
 # Schema for Fields Table            
class FieldsSchema(Base):
    """
    id              : Unique ID assigned to each field
    name            : Name of the field - Backend
    field_name      : Name of the field - Frontend 
    description     : Description of the field
    dataType        : Data-Type of the field
    category        : Category that field belongs to\
                      (category - name_address, invoice_details, amount_details, table, others)
    field_category  : Category Frontend
    type            : Default Field or Belongs to particular admin
    """

    __tablename__ = 'fields'

    field_id_seq = Sequence('field_id_seq', metadata=Base.metadata)
    id = Column(Integer, field_id_seq, server_default=field_id_seq.next_value(), primary_key=True)
    name = Column(String, nullable=False)
    field_name  = Column(String, nullable=False)
    description = Column(String, default="", nullable=False)
    dataType = Column(String, nullable=False)
    category = Column(String, nullable=False)
    field_category = Column(String, nullable=False)
    type = Column(String, nullable=False)          #default or adminId
    docType = relationship('DocumentTypeSchema', secondary='mapfielddoctype', overlaps='fields')
    
    def __init__(self, name, field_name, description, dataType, category, field_category, type):
        self.name = name
        self.field_name = field_name
        self.description = description
        self.dataType = dataType
        self.category = category
        self.field_category = field_category
        self.type = type

# Schema for DocumentType Table
class DocumentTypeSchema(Base):
    """
    id          : Unique ID assigned to each document type
    name        : Name of the document type - Backend
    doc_name    : Name of the document type - Frontend
    fieldsId    : Fields assigned to the document type
    type        : Default Document Type or Belongs to particular admin
    queues      : Relationship defined between document and queue
    """
    __tablename__ = 'documentType'

    doctype_id_seq = Sequence('doctype_id_seq', metadata=Base.metadata)
    id = Column(Integer, doctype_id_seq, server_default=doctype_id_seq.next_value(), primary_key=True)
    name = Column(String, nullable=False)
    doc_name = Column(String, nullable=False)
    description = Column(String, default="", nullable=False)
    #fieldsId = Column(ARRAY(Integer), server_default='{}')
    type = Column(String, nullable=False)          #default or adminId
    queues = relationship('QueuesSchema', secondary = 'mapqueuesdocument')
    admin = relationship(AdminSchema, secondary = 'mapadmindoctype')
    fields = relationship(FieldsSchema, secondary = 'mapfielddoctype')

    def __init__(self, name, doc_name, description, type):
        self.name = name
        self.doc_name = doc_name
        self.description = description
        self.type = type

# Schema for Queues Table
class QueuesSchema(Base):
    """
    id                  : Unique ID assigned to each queue created
    name                : Name of the queue
    adminId             : ID (Admin) under which the Queues belongs to
    default_flag        : Indicates whether the queue is created by default or not
    classification_flag : Indicates whether the batches in the queue shoud proceed with docType classification or not (by default it is True)
    extraction_flag     : Indicates whether the batches in the queue shoud proceed with docType extraction or not (by default it is True)
    classification_review_flag : Indicates whether the batches in the queue shoud go to pending tab or not ( i.e classification correction or split merge functionality) (by default it is True)
    review_mandatory_flag      : Indicates whether the batches should be reviewed before going to export or not (Applicable only for E2E API) (by default it is True)
    """

    __tablename__ = 'queues'

    queue_id_seq = Sequence('queue_id_seq', metadata=Base.metadata)
    id = Column(Integer, queue_id_seq, server_default=queue_id_seq.next_value(), primary_key=True)
    name = Column(String, nullable=False)
    adminId = Column(String, nullable=False)
    processor = relationship(ProcessorSchema, secondary = 'mapqueuesprocessor', overlaps="queues")
    documentType = relationship(DocumentTypeSchema, secondary = 'mapqueuesdocument', overlaps="queues")
    batch = relationship('BatchDbSchema', secondary = 'mapqueuesbatch', overlaps="queues")
    default_flag = Column(Boolean, default = False)
    classification_flag = Column(Boolean, default = True)
    extraction_flag = Column(Boolean, default = True)
    classification_review_flag = Column(Boolean, default = True)
    review_mandatory_flag = Column(Boolean, default = True)
    
    def __init__(self, name, aId="",default_flag=False):
        self.name = name
        self.adminId = aId
        self.default_flag=default_flag

#Schema for Mapping Admin and Document
class MapAdminDocType(Base):
    """
    (adminId, docTypeId)   : Unique IDs assigned to the mapping
    """

    __tablename__   = 'mapadmindoctype'

    adminId		    = Column(String,  ForeignKey('admin.adminId', ondelete="CASCADE"), primary_key = True)
    docTypeId	    = Column(Integer, ForeignKey('documentType.id', ondelete="CASCADE"), primary_key = True)

#Schema for Mapping Fields and DocType
class MapFieldDocType(Base):
    __tablename__	= 'mapfielddoctype'

    docTypeId		= Column(Integer, ForeignKey('documentType.id', ondelete="CASCADE"), primary_key = True)
    fieldId		    = Column(Integer, ForeignKey('fields.id', ondelete="CASCADE"), primary_key = True)
    adminId         = Column(String, nullable=False, primary_key = True)
    threshold		= Column(Float, default=0.85)

    def __init__(self, docTypeId, fieldId, adminId, threshold):
        self.docTypeId = docTypeId
        self.fieldId = fieldId
        self.adminId = adminId
        self.threshold = threshold

#Schema for Mapping Queues and Processor
class MapQueuesProcessor(Base):
    """
    (processorId, queuesId) : Unique IDs assigned to the mapping
    adminId                 : ID (Admin) under which the Queues-Processor Mapping belongs to
    """
    __tablename__ = 'mapqueuesprocessor'

    processorId = Column(Integer,  ForeignKey('processor.id', ondelete="CASCADE"), primary_key = True)
    queuesId = Column(Integer,  ForeignKey('queues.id', ondelete="CASCADE"), primary_key = True)
    adminId = Column(String, nullable=False)

#Schema for Mapping Queues and Document
class MapQueuesDocument(Base):
    """
    (documentTypeId, queuesId)  : Unique IDs assigned to the mapping
    adminId                     : ID (Admin) under which the Queues-Document Mapping belongs to
    """
    __tablename__ = 'mapqueuesdocument'

    documentTypeId = Column(Integer,  ForeignKey('documentType.id', ondelete="CASCADE"), primary_key = True)
    queuesId = Column(Integer,  ForeignKey('queues.id', ondelete="CASCADE"), primary_key = True)
    adminId = Column(String, nullable=False)



#######################################################################################################################

class BatchDbSchema(Base):
    """
    id                : Unique Id assigned to each batch uploaded
    batch_id          : Id assigned to each batch uploaded for each admin
    batch_name        : Name of the batch
    adminId           : Unique Id of the admin
    adminEmail        : Email Id of the admin
    uploaded_dateTime : Date and time of the batch upload
    received_dateTime : Date and time at which the processor was assigned
    extracted_start_dateTime    : Date and time at which the extraction was started
    extracted_dateTime : Date and time at which the extraction was done
    validated_dateTime : Date and time at which the validation was done
    exported_dateTime  : Date and time at which the batch was exported
    channel           : Medium through which batch has been uploaded
    assignedTo        : Email Id of the processor who has been assigned to this batch
    status            : Status of upload - InComplete, Waiting, Uploading, Uploaded, Digitizing, ToBeReviewed, Reviewed, StraightThrough, PasswordRequired
    pending           : Status of Batch in Processor side
    reviewed          : Status of Batch in Processor side
    exported          : Status of Batch in Processor side
    deleted           : Status of Batch in Processor side
    job_ids           : For each files in the batch a job Id will be assigned in the Processor Side and will get stored in JobDb (MongoDb), this has the list of all jobs.
    batch_size        : Total size of the uploaded files in the batch.
    method            : Extraction:1, Classification:2, Extraction+Classification:3 (default value: 1) (This Flag is used for Export Functionality)
    """

    __tablename__ = 'batch_db'
    
    id_seq = Sequence('id_seq', metadata=Base.metadata)
    id = Column(Integer,id_seq, server_default=id_seq.next_value(), primary_key=True)
    batch_id = Column(Integer)
    batch_name = Column(String)
    adminId = Column(String, nullable=False)                    # Uploaded_by
    adminEmail = Column(String, nullable=False)
    uploaded_dateTime = Column(DateTime)
    received_dateTime = Column(DateTime)
    extraction_start_dateTime = Column(DateTime)
    extracted_dateTime = Column(DateTime)
    validated_dateTime = Column(DateTime)
    exported_dateTime = Column(DateTime)
    channel = Column(String, default="Web-App")
    assignedTo = Column(String, default = "None")               # Not assigned 
    status = Column(String, default="InComplete")            
    pending = Column(Boolean, default=False)
    reviewed = Column(Boolean, default=False)
    exported =  Column(Boolean, default=False)
    deleted =  Column(Boolean, default=False)

    job_ids = Column(ARRAY(Integer), server_default='{}')
    batch_size = Column(String, default="0 KB")
    method = Column(Integer, default = 1)

    queues = relationship('QueuesSchema', secondary = 'mapqueuesbatch')

    def __init__(self,batch_id,batch_name,admin_id,admin_email, dtime, status, channel="Web-App"):
        self.batch_id = batch_id
        self.batch_name = batch_name
        self.adminId = admin_id
        self.adminEmail = admin_email
        self.uploaded_dateTime = dtime
        self.status = status
        self.channel = channel
        

#Schema for Mapping Queues and Batch
class MapQueuesBatch(Base):
    """
    (BatchId, queuesId)     : Unique IDs assigned to the mapping
    adminId                 : ID (Admin) under which the Queues-Processor Mapping belongs to
    """
    __tablename__ = 'mapqueuesbatch'

    batchId = Column(Integer, ForeignKey('batch_db.id', ondelete="CASCADE"), primary_key = True)
    queuesId = Column(Integer, ForeignKey('queues.id', ondelete="CASCADE"), primary_key = True)
    adminId = Column(String, nullable=False)
