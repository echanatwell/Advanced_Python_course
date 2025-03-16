import json
from koltunov_latex_generator import tex_table_format, tex_document_format, tex_picture_format, combine_blocks


if __name__ == '__main__':
    with open('artifacts/table_data.txt', 'r') as f:
        data = json.load(f)
    
    formatted_table = tex_table_format(data)
    formatted_img = tex_picture_format('artifacts/python_logo.png')
    combined_content = combine_blocks([formatted_table, formatted_img])

    formatted_doc = tex_document_format(combined_content)
    
    with open('artifacts/doc.tex', 'w') as f:
        f.write(formatted_doc)