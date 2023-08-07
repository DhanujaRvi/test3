"""
Description : Handling Fields Table Creation, Deletion, Display and Other Functionalities.
* Necessary Code Comments for function description added before the function definition.
"""

from sqlalchemy import or_, and_

from Database.schema import FieldsSchema
from Database import Session
#session = Session()

class FIELDSDB():
    def __init__(self):
        self.session = Session()

    #BASIC FUNCTIONALITIES
    # insert - For Inserting a New Field to the Database.
    def insert(self, field_name, descp, dType, field_category, adminId, kwargs={}, logger=None):
        try:
            # print(field_name, descp, dType, field_category, adminId)
            name = field_name.lower().replace(" ","_")
            if field_category == "Name Address Details":
                category = "name_address"
            if field_category == "Invoice Details":
                category = "invoice_details"
            if field_category == "Amount Details":
                category = "amount_details"
            if field_category == "Table Details":
                category = "table"
            if field_category == "Container Details":
                category = "container_details"
            if field_category == "Shipment Details":
                category = "shipment_details"

            #Insert Only when Field doesn't already exists.
            if self.getId(name, adminId) == -1:
                f1 = FieldsSchema(name, field_name, descp, dType, category, field_category, adminId)
                self.session.add(f1)
                self.session.commit()
                return 1
            else:
                return -1
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # delete - For Deleting a Field in the Database.
    def delete(self, id, adminId, kwargs={}, logger=None):
        try:
            # Checking if the Field Id exists to delete.
            if(self.existId(id, adminId)):
                if(self.is_default(id) == False):
                    cond = and_(FieldsSchema.id == id, FieldsSchema.type == adminId)
                    self.session.query(FieldsSchema).filter(cond).delete()
                    self.session.commit()        
                    #return documentDb.delete_fields(id, adminId)
                    return 1
            # Field not found or a default Field
            return -1
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # display - Displaying the available Field for the specified admin.
    def display(self, adminId, version, kwargs={}, logger=None):
        try:
            cond = or_(FieldsSchema.type == adminId, FieldsSchema.type == 'default')
            fields = self.session.query(FieldsSchema).filter(cond).order_by(FieldsSchema.id.desc())
            results = {}
            if fields:
                for field in fields:
                    if field.field_category in results:
                        results[field.field_category].append({"id"            : field.id,\
                                                            "name"          : field.field_name,\
                                                            "description"   : field.description,\
                                                            "dataType"      : field.dataType,\
                                                            "type"          : field.type})
                    else:
                        results[field.field_category] = [{"id"            : field.id,\
                                                        "name"          : field.field_name,\
                                                        "description"   : field.description,\
                                                        "dataType"      : field.dataType,\
                                                        "type"          : field.type}]
            if version == 'v3.0':                       
                return results
            elif version == 'v3.1':
                data_types = ['Number','Float', 'Date','Currency', 'Alphanumeric(Single word)', 'Alphanumeric(Multiple words)', 'String(Single word)', 'String(Multiple words)','Alphabets(Single word)','Alphabets(Multiple words)']
                return {"Fields" : results, "DataTypes" : data_types}

        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2
    
    # update - For Updating a Field
    def update(self, fields, adminId, kwargs={}, logger=None):
        try:
            for category in fields.keys():
                for field in fields[category]:
                    id = field['id']
                    field_name = field['name']
                    description = field['description']
                    dataType = field['dataType']
                    if self.is_default(id):
                        continue     #No change in default Field 
                    elif(self.existId(id, adminId)):
                        cond = and_(FieldsSchema.id == id, FieldsSchema.type == adminId)
                        self.session.query(FieldsSchema).filter(cond).update({FieldsSchema.field_name:field_name,FieldsSchema.description:description,FieldsSchema.dataType:dataType})
                    else:
                        # print("Field id does not exist..")
                        return -1
            self.session.commit()
            return 1
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    #OTHER FUNCTIONALITIES
    # getId - Getting the Id of the Field from the Database.
    def getId(self, name, adminId, kwargs={}, logger=None):
        try:
            cond = and_(FieldsSchema.name == name, FieldsSchema.type == adminId)
            field = self.session.query(FieldsSchema).filter(cond)
            if self.session.query(field.exists()).scalar() :
                return field.id
            else:
                return -1        #Field not already exist
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2
    
    def getName(self, id, adminId, kwargs={}, logger=None):
        try:
            cond = and_(FieldsSchema.id == id, or_(FieldsSchema.type == adminId, FieldsSchema.type == 'default'))
            field = self.session.query(cond).first()
            return field.field_name
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return -2

    # is_default - To check if the Field is default.
    def is_default(self, fid, kwargs={}, logger=None):
        try:
            field = self.session.query(FieldsSchema).filter(FieldsSchema.id == fid).first()  
            if(field.type == 'default'):
                return True
            else:
                return False
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return False

    # existId - Checking if the Field Id already exists.
    def existId(self, id, adminId, kwargs={}, logger=None):
        try:
            cond = and_(FieldsSchema.id == id, or_(FieldsSchema.type == adminId, FieldsSchema.type == 'default'))
            queue = self.session.query(FieldsSchema).filter(cond)
            return self.session.query(queue.exists()).scalar()  
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return False
    def check_ifexists(self,name,default_flag,kwargs={}, logger=None):
        try:
            if default_flag==True:
                default_flag='default'
            cond=and_(FieldsSchema.name==name,FieldsSchema.type==default_flag)
            field = self.session.query(FieldsSchema).filter(cond)
            is_exists=self.session.query(field.exists()).scalar() 
            self.session.commit()
            return is_exists
        except:
            self.session.rollback()
            if logger != None:
                logger.error("Exception Occured.", exc_info=True)
            return False


       

