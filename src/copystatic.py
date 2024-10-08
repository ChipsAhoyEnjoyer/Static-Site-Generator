import os, shutil, pathlib

from block_md import markdown_to_blocks, block_to_block_type, raw_md_to_text, markdown_to_html_node


def copy_static(source: str, destination: str) -> None:
    if not os.path.exists(destination):
        os.mkdir(destination)
        print(f"{destination} directory created")
    else:
        shutil.rmtree(destination)
        os.mkdir(destination)
        print(f"{destination} directory deleted. Recreating...")
    for item in os.listdir(source):
        branch = os.path.join(source, item)
        copy_destination = os.path.join(destination, item)
        if os.path.isfile(branch):
            shutil.copy(branch, destination)
            print(f"{branch} -> {copy_destination} copied over")
        else:
            copy_static(branch, copy_destination)

def extract_title(markdown):
    block_list = markdown_to_blocks(markdown)
    for block in block_list:
        block_type = block_to_block_type(block)
        if block_type == "h1":
            return raw_md_to_text(block)
    raise Exception("Title not found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as markdown:
        string_repr = markdown.read()
        html_file = markdown_to_html_node(string_repr).to_html()
        title = extract_title(string_repr)
    with open(template_path, "r") as template:
        template_str = template.read()
        final_template = template_str.replace("{{ Title }}", title).replace("{{ Content }}", html_file)
    os.makedirs(dest_path, exist_ok=True)
    new_file = pathlib.Path(from_path).stem + ".html"
    with open(f"{dest_path}/{new_file}", "w") as new_file:
        new_file.write(final_template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        return
    for path in os.listdir(dir_path_content):
        branch = os.path.join(dir_path_content, path)
        destination = os.path.join(dest_dir_path, path)
        suffix = pathlib.Path(branch).suffix
        if os.path.isfile(branch) and suffix == ".md":
            generate_page(branch, template_path, dest_dir_path)
        else:
            generate_pages_recursive(branch, template_path, destination)
