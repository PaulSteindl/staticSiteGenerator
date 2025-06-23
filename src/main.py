import os
import shutil
from textnode import TextNode, TextType

def setup_public_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

def rec_copy_static(dir_old_path, dir_new_path):
    for entry in os.listdir(dir_old_path):
        entry_old_path = os.path.join(dir_old_path, entry)
        entry_new_path = os.path.join(dir_new_path, entry)

        if os.path.isfile(entry_old_path):
            shutil.copy(entry_old_path, entry_new_path)
            continue
        
        os.mkdir(entry_new_path)
        rec_copy_static(entry_old_path, entry_new_path)

def main():
    setup_public_dir("./public/")
    rec_copy_static("./static/", "./public/")

if __name__ == "__main__":
    main()