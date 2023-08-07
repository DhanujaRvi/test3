"""
Description : Query to add default values to FieldsSchema and DocumentTypeSchema
"""

import traceback
from Database.schema import DocumentTypeSchema, FieldsSchema,QueuesSchema
from Database import Session
from configs.default_values import fields_default, docType_default,queue_default
from Database.FieldsDb import FIELDSDB
from Database.DocumentTypeDb import DOCUMENTDB
from Database.QueuesDb import QUEUESDB
o_filedsdb=FIELDSDB()
o_docdb=DOCUMENTDB()
o_queue=QUEUESDB()
session = Session()

def add_default():
    # print("Add Default")
    try:
        #if(not session.query(FieldsSchema).first()):
        defaults = []
        for field in fields_default:
            
            check_flag=o_filedsdb.check_ifexists(field['name'],True)
            print(field['name'],check_flag)
            if check_flag==False:
                print("FIeld",field['name'])
                defaults.append(FieldsSchema(name       = field["name"],\
                                        field_name  = field["field_name"],\
                                        description = field["descp"],\
                                        dataType    = field["dType"],\
                                        category    = field["category"],\
                                        field_category= field["field_category"],\
                                        type        = field["type"]))
        session.bulk_save_objects(defaults)
        session.commit()
        
        """
        if(not session.query(DocumentTypeSchema).first()):
            defaults = []
            for dt in docType_default:
                defaults.append(DocumentTypeSchema(name         = dt["name"],\
                                                    doc_name    = dt["doc_name"],\
                                                description  = dt["descp"],\
                                                fieldsId     = dt["fIds"],\
                                                type         = dt["type"]))
            session.bulk_save_objects(defaults)
            session.commit()
        """

        #if(not session.query(DocumentTypeSchema).first()):
        defaults = []
        for dt in docType_default:
            check_flag=o_docdb.check_ifexists(dt['name'],True)
            print(dt['name'],check_flag)
            if check_flag==False:
                print("Doc",dt['name'])
                defaults.append(DocumentTypeSchema(name         = dt["name"],\
                                                    doc_name    = dt["doc_name"],\
                                                description  = dt["descp"],\
                                                type         = dt["type"]))
        session.bulk_save_objects(defaults)
        session.commit()

        defaults = []
        for dt in queue_default:
            check_flag=o_queue.check_ifexists(dt['name'],True)
            print(dt['name'],check_flag)
            if check_flag==False:
                print("Doc",dt['name'])
                defaults.append(QueuesSchema(name         = dt["name"],\
                                                    aId="",\
                                                    default_flag=True,\
                                                    ))
        session.bulk_save_objects(defaults)
        session.commit()

    except:
        # print("Inside Exception")
        print(traceback.print_exc())
        session.rollback()