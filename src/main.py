import os
import shutil
from generate_page import generate_pages_recursively
from pathlib import Path

def print_file_path(path):
    temp_path = path.split('/')
    result = ['']

    for i in range(len(temp_path)):
        if temp_path[i] == 'webserver':
            result += temp_path[i:]
            break

    return '/'.join(result)

def generate_static():
    home_dir = Path(os.path.dirname(__file__)).resolve().parents[0]
    new_path = lambda x: os.path.join(home_dir, x)

    if os.path.exists(new_path('public')):
        shutil.rmtree(new_path('public'))
        os.mkdir(new_path('public'))

    copy_static_to_public(new_path('static'), new_path('public'))

def copy_static_to_public(source, dest):
    if not os.path.exists(source):
        raise FileNotFoundError(f"Error: source file does not exist to copy from: {source}")
    if not os.path.exists(dest):
        raise FileNotFoundError(f"Error: destination file does not exist: {dest}")

    add_source = lambda x: os.path.join(source, x)
    add_dest = lambda x: os.path.join(dest, x)

    if len(os.listdir(source)) == 0:
        print(f"-- End of tree: {source} --")
        return

    print(f"Dir: {print_file_path(source)}")
    for i in os.listdir(source):
        if not os.path.isfile(add_source(i)):
            print(f"+ Creating folder: {print_file_path(add_dest(i))}")
            os.mkdir(add_dest(i))
            copy_static_to_public(add_source(i), add_dest(i))

        else:
            print(f"Copying file:\t {print_file_path(add_source(i))} \n-> Destination: {print_file_path(add_dest(i))}\n")
            shutil.copy(add_source(i), add_dest(i))

if __name__ == "__main__":
    home_dir = Path(os.path.dirname(__file__)).resolve().parents[0]
    new_path = lambda x: os.path.join(home_dir, x)

    generate_static()

    generate_pages_recursively(new_path('content/'), new_path('template.html'), new_path('public/'))
