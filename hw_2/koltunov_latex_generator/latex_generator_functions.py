def tex_document_format(content: str) -> str:
    template = r"""\documentclass{article}
    \usepackage{graphicx}
    \begin{document}

        %s

    \end{document}"""
    
    return template % content


def tex_table_format(content: list[list]) -> str:
    ncols = max([len(row) for row in content])
    padded_content = pad_rows(content, ncols)
    formatted_table = r'\begin{tabular}{%s}' % '|'.join(['c']*ncols)
    for row in padded_content:
        formatted_table += "\n" + r"\hline"
        formatted_table += "\n" + format_row(row) + r" \\"
    formatted_table += "\n" + r"\hline"
    formatted_table += "\n" + r"\end{tabular}"

    return formatted_table


def pad_rows(rows: list[list], pad_len: int) -> list[list]:
    padded_rows = [row + ['']*(pad_len-len(row)) for row in rows]
    return padded_rows


def format_row(row: list) -> str:
    str_row = [str(el) for el in row]

    return ' & '.join(str_row)


def tex_picture_format(img_path: str) -> str:
    formatted_pic = r"\begin{figure}"
    formatted_pic += "\n" + r"\includegraphics{%s}" % img_path
    formatted_pic += "\n" + r"\end{figure}"

    return formatted_pic


def combine_blocks(blocks: list[str], sep: str ='\n') -> str:
    return sep.join(blocks) 
