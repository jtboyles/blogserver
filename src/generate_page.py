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

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

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
