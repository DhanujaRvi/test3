"""
Description : Definition of APIs, Creation of Tables.
"""

from flask import Flask, send_from_directory, render_template
from flask_restful import Api
from flask_cors import CORS

from Database import engine
from Database.schema import MapQueuesProcessor, MapQueuesDocument,ProcessorSchema, QueuesSchema,\
                            DocumentTypeSchema, FieldsSchema, BatchDbSchema

from Database import defaults 

from Application.Add import ADD
from Application.Display import DISPLAY, DISPLAY_BATCH
from Application.Delete import DELETE
from Application.Map import MAP
from Application.Unmap import UNMAP
from Application.Edit import EDIT
from Application.Activate import ACTIVATE
#from Application.Login import LOGIN
from Application.Upload import UPLOAD

###################################################################################

ProcessorSchema.metadata.create_all(engine)
QueuesSchema.metadata.create_all(engine)
DocumentTypeSchema.metadata.create_all(engine)
FieldsSchema.metadata.create_all(engine)
MapQueuesProcessor.metadata.create_all(engine)
MapQueuesDocument.metadata.create_all(engine)
BatchDbSchema.metadata.create_all(engine)

# Loading default data to the tables (fields and documentTypes)
defaults.add_default()

###################################################################################

app = Flask(__name__)
api = Api(app)
CORS(app)

app.config.update(
    # UPLOADED_PATH = path["upload"],
    # DATA_PATH = os.path.join("DocIdentifier","uploads"),
    # DOWNLOAD_PATH = path["data_dir"],
    DROPZONE_MAX_FILE_SIZE=30000,
    DROPZONE_MAX_FILES=3000,
    DROPZONE_IN_FORM=True,
    DROPZONE_UPLOAD_ON_CLICK=True,
    DROPZONE_UPLOAD_ACTION='upload_batch',  # URL or endpoint
    DROPZONE_UPLOAD_BTN_ID='submit',
    JSON_SORT_KEYS = False,
    SQLALCHEMY_ECHO = False
)

###################################################################################
#add end point
api.add_resource(ADD, '/admin/add_processor',\
                resource_class_kwargs={'table': 'processor'},\
                endpoint='add_processor')
            
api.add_resource(ACTIVATE, '/admin/activate_processor',\
                endpoint='activate_processor')

api.add_resource(ADD, '/admin/add_queues',\
                resource_class_kwargs={'table': 'queues'},\
                endpoint='add_queues')

api.add_resource(ADD, '/admin/add_fields',\
                resource_class_kwargs={'table': 'fields'},\
                endpoint='add_fields')

api.add_resource(ADD, '/admin/add_documenttype',\
                resource_class_kwargs={'table': 'document'},\
                endpoint='add_documenttype')

###################################################################################
#display end point
api.add_resource(DISPLAY, '/admin/display_processor',\
                resource_class_kwargs={'table': 'processor'},\
                    endpoint='display_processor')

api.add_resource(DISPLAY, '/admin/display_queues',\
                resource_class_kwargs={'table': 'queues'},\
                endpoint='display_queues')

api.add_resource(DISPLAY, '/admin/display_fields',\
                resource_class_kwargs={'table': 'fields'},\
                endpoint='display_fields')
                
api.add_resource(DISPLAY, '/admin/display_documenttype',\
                resource_class_kwargs={'table': 'document'},\
                    endpoint='display_documenttype')

###################################################################################
#delete end point
api.add_resource(DELETE, '/admin/delete_processor',\
                resource_class_kwargs={'table': 'processor'},\
                endpoint='delete_processor')

api.add_resource(DELETE, '/admin/delete_queues',\
                resource_class_kwargs={'table': 'queues'},\
                endpoint='delete_queues')

api.add_resource(DELETE, '/admin/delete_fields',\
                resource_class_kwargs={'table': 'fields'},\
                endpoint='delete_fields')

api.add_resource(DELETE, '/admin/delete_documenttype',\
                resource_class_kwargs={'table': 'document'},\
                endpoint='delete_documenttype')

###################################################################################
#edit end point
api.add_resource(EDIT, '/admin/edit_processor',\
                resource_class_kwargs={'table': 'processor'},\
                endpoint='edit_processor')

api.add_resource(EDIT, '/admin/edit_queues',\
                resource_class_kwargs={'table': 'queues'},\
                endpoint='edit_queues')
    
api.add_resource(EDIT, '/admin/edit_fields',\
                resource_class_kwargs={'table': 'fields'},\
                endpoint='edit_fields')

api.add_resource(EDIT, '/admin/edit_documenttype',\
                resource_class_kwargs={'table': 'document'},\
                endpoint='edit_documenttype')

###################################################################################
#map end point
api.add_resource(MAP, '/admin/map_processor',\
                resource_class_kwargs={'table': 'processor'},\
                endpoint='map_processor')

api.add_resource(MAP, '/admin/map_document',\
                resource_class_kwargs={'table': 'document'},\
                endpoint='map_document')

###################################################################################
#unmap end point
api.add_resource(UNMAP, '/admin/unmap_processor',\
                resource_class_kwargs={'table': 'processor'},\
                endpoint='unmap_processor')

api.add_resource(UNMAP, '/admin/unmap_document',\
                resource_class_kwargs={'table': 'document'},\
                endpoint='unmap_document')

###################################################################################

api.add_resource(DISPLAY_BATCH, '/admin/display_batch',\
                resource_class_kwargs={'table': 'batch'},\
                endpoint='display_batch')

api.add_resource(DELETE, '/admin/delete_batch',\
                resource_class_kwargs={'table': 'batch'},\
                endpoint='delete_batch')

###################################################################################

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
    #app.run()