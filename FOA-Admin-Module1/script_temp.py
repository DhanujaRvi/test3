from sqlalchemy import or_, and_, func

from Database.schema import MapAdminDocType, AdminSchema
from Database import Session
import traceback

session = Session()



def get_admin_without_config():
    try:
        admins = session.query(AdminSchema).filter(AdminSchema.is_config == False)
        return [admin.adminId for admin in admins]
    except:
        session.rollback()
        return -2

# map - Mapping docType with admin
def map_admin(adminId, docTypeId):
    try: 
        session.add(MapAdminDocType(docTypeId=docTypeId, adminId =adminId))
        session.commit()
        return 1
    except:
        session.rollback()
        print(traceback.print_exc())
        return -2

# New document Type manually added DocumentDB
doc_list = [14,15,16,17]

# Admin who has no config defined
admin_list = get_admin_without_config()

for admin in admin_list:
    for doc in doc_list:
        print( admin, doc, map_admin(admin, doc))