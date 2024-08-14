from copystatic import copy_static, generate_page

def main():
    copy_static(source="./static", destination="./public")
    generate_page(from_path="content/index.md", dest_path="public/index.html", template_path="template.html")

main()