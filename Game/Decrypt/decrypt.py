#!/usr/bin/python3
from Cryptodome.Cipher import Blowfish
import sys
import os

def walk_the_tree(rooter):
    for root, subdirectories, files in os.walk(rooter):
        for file in files:
            file_name = os.path.abspath(os.path.join(root, file))
            if file_name.endswith('.dat') or file_name.endswith('.tbl'):
                print("Decrypting " + file_name)
                decrypt(file_name)


def decrypt(file_name):
    with open(file_name, 'rb') as encrypted_file:
        # Skipping if there is no magic
        magic = encrypted_file.read(4)
        if magic != b'\x41\x42\x10\x40':
            print(file_name + " seems not to be encrypted.")
            return
        size = int.from_bytes(encrypted_file.read(4), byteorder='little')
        file = encrypted_file.read(size -  size % Blowfish.block_size)
        key = b'ed8psv5_steam'
        cipher = Blowfish.new(key, Blowfish.MODE_ECB)
        output = cipher.decrypt(file)
        with open(file_name+".decrypted", 'wb') as out:
            out.write(output)
            out.write(encrypted_file.read(size % Blowfish.block_size))

n = len(sys.argv)
if n != 2:
    print("Forgot the parent dir arg!")
    #sys.exit(1)
walk_the_tree("F:\GitHub\HajimariQuickTranslation\Game\Decrypt\Files")