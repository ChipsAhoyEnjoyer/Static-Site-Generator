from copystatic import copy_static, generate_pages_recursive, generate_page

def main():
    copy_static(source="./static", destination="./public")
    generate_pages_recursive(dir_path_content="./content", dest_dir_path="./public", template_path="template.html")

main()