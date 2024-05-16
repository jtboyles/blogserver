import re
import os
from markdown_blocks import markdown_to_HTML

def extract_header(markdown):
    header = re.search(r"<h1>(.*)<\/h1>", markdown)
    if header == None:
        raise Exception("Error: A header (indicated by starting a line with '# ') is required.")

    start_idx = header.start() + 4
    end_idx = header.end() - 5

    return markdown[start_idx:end_idx]

def generate_page(from_path, template_path, dest_path):
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"Error: source file does not exist to generate from: {from_path}")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Error: template file does not exist to generate from: {template_path}")
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    print(f"Generating page from: {from_path} to: -> {dest_path} using: {template_path}\n")

    markdown = ""
    template = ""

    with open(from_path, 'r') as f:
        markdown = markdown_to_HTML(f.read())

    with open(template_path, 'r') as f:
        template = f.read()

    title = extract_header(markdown)

    result = template.replace("{{ Title }}", title)
    result = result.replace("{{ Content }}", markdown)

    with open(dest_path, 'w') as f:
        f.write(result)

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise FileNotFoundError(f"Error: content not available to generate from: {dir_path_content}")

    for i in os.listdir(dir_path_content):
        add_file = lambda x: dir_path_content + x
        add_dest = lambda x: dest_dir_path + x[:-3] + '.html'
        add_dir = lambda x: dir_path_content + x + '/'
        add_dest_dir = lambda x: dest_dir_path + x + '/'

        if os.path.isfile(add_file(i)):
            generate_page(add_file(i), template_path, add_dest(i))
        else:
            os.makedirs(add_dest_dir(i))
            generate_pages_recursively(add_dir(i), template_path, add_dest_dir(i))

