import os
import shutil
import sys
from helperfunctions import extract_title, markdown_to_html_node
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

def generate_page(base_path, from_path, template_path, dest_path):
    if not os.path.exists(from_path):
        raise Exception(f"source file does not exist {from_path}")

    if not os.path.exists(template_path):
        raise Exception(f"template file does not exist {template_path}")

    to_create = os.path.dirname(dest_path)
    if not os.path.exists(to_create):
        os.makedirs(to_create)

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_file = open(from_path)
    markdown_text = markdown_file.read()
    markdown_file.close()
    title = extract_title(markdown_text)
    html = markdown_to_html_node(markdown_text).to_html()

    template_file = open(template_path)
    template_text = template_file.read()
    template_file.close()
    full_html = template_text.replace("{{ Title }}", title).replace("{{ Content }}", html)
    full_html_www = full_html.replace("href=\"/", f"href=\"{base_path}").replace("src=\"/", f"src=\"{base_path}")

    destination_file = open(dest_path, "w")
    destination_file.write(full_html_www)
    destination_file.close()

def generate_pages_recursive(base_path, dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        entry_old_path = os.path.join(dir_path_content, entry)
        entry_new_path = os.path.join(dest_dir_path, entry).replace(".md", ".html")

        if os.path.isfile(entry_old_path):
            generate_page(base_path, entry_old_path, template_path, entry_new_path)
            continue

        generate_pages_recursive(base_path, entry_old_path, template_path, entry_new_path)

def main():
    base_path = sys.argv[1]
    print(base_path)
    if not base_path:
        base_path = "/"

    setup_public_dir("./docs/")
    rec_copy_static("./static/", "./docs/")
    generate_pages_recursive(base_path, "./content/", "./template.html", "./docs/")

if __name__ == "__main__":
    main()