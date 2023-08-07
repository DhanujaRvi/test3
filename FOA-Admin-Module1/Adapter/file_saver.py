import os
import json
import requests

class FILESAVERADAPTER:
    def __init__(self):
        pass

    # Internal API call to create jobs and save files in the processor side and return list of jobs created for the uploaded batch
    def save(self,admin_id, bId, uploaded_files, auth_headers, auth_type, default_docType):
        try:
            url = "http://localhost:8000/api/file_saver"
            
            if auth_type == "Bearer":
                headers = {
                    'Authorization': auth_headers
                }
            elif auth_type == "x-api-key":
                headers = {
                    "x-api-key":auth_headers
                }
        
            payload = {
                "admin_id":admin_id,
                "batch_id":bId,
                "default_docType": default_docType
                }
                
            response = requests.request("POST", url, headers=headers, data = payload, files = uploaded_files)
            status_code = response.status_code
            return status_code
        except Exception as e:
            # print(e)
            return []
