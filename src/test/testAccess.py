import os

path = "/root/nltk_data"
if os.access(path, os.R_OK | os.W_OK):
    print("Python process has read and write access to the directory.")
else:
    print("Python process does not have read and write access to the directory.")