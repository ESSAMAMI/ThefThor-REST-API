from cryptography.fernet import Fernet
import os
import pathlib

class EncryptDecryptPwd():
    
    def __init__(self):
        pass
        
    def generate_key(self):
        """
        Generates a key and save it into a file
        """
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)

    def load_key(self):
        """
        Load the previously generated key
        """

        return open("secret.key", "rb").read()

    def encrypt_pwd(self, message):
        """
        Encrypts a message
        """
        secret = pathlib.Path("secret.key")
        if not secret.exists():
            self.generate_key()
            
        key = self.load_key()
        encoded_message = message.encode()
        f = Fernet(key)
        encrypted_message = f.encrypt(encoded_message)
        print(encrypted_message)
        return encrypted_message

    def decrypt_pwd(self,encrypted_message):
        """
        Decrypts an encrypted message
        """
        key = self.load_key()
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message)
        return decrypted_message
