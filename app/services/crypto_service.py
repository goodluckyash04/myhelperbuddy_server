# import base64
# # pycryptodome library
#
# class CryptoService:
#     def __init__(self, key: str = None):
#         self.KEY = key or ''
#
#     def encrypt_message(self, data):
#         ser_data = str(data).encode('utf-8')
#         # Padding the plaintext
#         padder = padding.PKCS7(algorithms.AES.block_size).padder()
#         padded_plaintext = padder.update(ser_data) + padder.finalize()
#
#         # Encrypt the padded plaintext
#         backend = default_backend()
#         cipher = Cipher(algorithms.AES(self.KEY), modes.CBC(b'\x00' * 16), backend=backend)
#         encryptor = cipher.encryptor()
#         ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
#
#         return base64.b64encode(ciphertext).decode('utf-8')
#
#
#     def decrypt_message(self, encrypted_data):
#         # Decode the base64 encoded ciphertext
#         ciphertext = base64.b64decode(encrypted_data.encode('utf-8'))
#
#         # Initialize the cipher with the same parameters used for encryption
#         backend = default_backend()
#         cipher = Cipher(algorithms.AES(self.KEY), modes.CBC(b'\x00' * 16), backend=backend)
#
#         # Create a decryptor object
#         decryptor = cipher.decryptor()
#
#         # Decrypt the ciphertext
#         decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
#
#         # Unpad the decrypted plaintext
#         unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
#         decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()
#
#         # Decode the decrypted plaintext
#         return decrypted_data.decode('utf-8')
