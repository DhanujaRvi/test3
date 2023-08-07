"""
Description     : Class defining the Encrypt, Decrypt functionalities of Ind-one
"""
from Crypto.Cipher import AES
from Crypto import Random
import traceback

SECRET_SALT = b'7x!A%D*G-JaNdRgUkXp2s5v8y/B?E(H+'

class AdminDataGenerator():
    def encrypt(self,user_email,admin_id):
        admin_id = str(admin_id)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(SECRET_SALT, AES.MODE_CFB, iv)
        data_bytes = str.encode(user_email+':'+str(admin_id))
        msg = iv + cipher.encrypt(data_bytes)
        return msg.hex()
    
    def decrypt(self, token, kwargs, logger):
        try:
            iv = Random.new().read(AES.block_size)
            cipher = AES.new(SECRET_SALT, AES.MODE_CFB, iv)
            decrypted = cipher.decrypt(bytes.fromhex(token))[len(iv):]
            return decrypted.decode('utf-8').split(':')
        except:
            print(traceback.print_exc())
            if logger != None:
                logger.error("Exception Occured in Decrypt functionality of Ind-one", exc_info=True)
            return -2, -2

def main():
    admin_data = AdminDataGenerator()
    invite_token = admin_data.encrypt("ridhanya1999@gmail.com","498")
    
    print(invite_token)
    print(admin_data.decrypt(invite_token))

#main()