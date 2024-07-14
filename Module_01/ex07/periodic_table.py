def string_to_dict(line):
    data_dict = {}

    try:
        name, other_data = line.split("=", 1)
        data_dict['name'] = name.strip()
        data_pairs = (data.split(":") for data in other_data.split(","))
        data_dict.update({key.strip(): value.strip() for key, value in data_pairs})
    except ValueError as e:
        print(f"❌ Skipping malformed line: {line.strip()} (Error: {e})")

    return data_dict


def read_file(file_path):
    list_of_data_dict = []

    with open(file_path, "r") as f:
        for line in f:
            data_dict = string_to_dict(line)
            list_of_data_dict.append(data_dict)
        return list_of_data_dict


def format_body_html(f, list_of_data_dict):
    prev_level = 0
    curr_level = 0
    body_cont = "\t\t<table>\n"

    for one_elem_dict in list_of_data_dict:
        curr_level = int(one_elem_dict['position'])
        if curr_level == 0:
            body_cont +="\t\t\t<tr>\n"
        if curr_level - prev_level > 1:
            body_cont += "\t\t\t\t<td colspan='" + str(curr_level - prev_level - 1) + "'></td>\n"
        body_cont += "\t\t\t\t<td>\n\t\t\t\t\t<h4>" + one_elem_dict['name'] + "</h4>\n"
        body_cont += "\t\t\t\t\t<ul>\n\t\t\t\t\t\t<li>" + one_elem_dict['number'] +"</li>\n" \
            "\t\t\t\t\t\t<li>" + one_elem_dict['small'] +"</li>\n" \
            "\t\t\t\t\t\t<li>" + one_elem_dict['molar'] + "</li>\n" \
            '\t\t\t\t\t\t<li>' + one_elem_dict['electron'] + "</li>\n" \
            "\t\t\t\t\t</ul>\n\t\t\t\t</td>\n"
        if curr_level == 17:
            body_cont += "\t\t\t</tr>\n"
            curr_level = 0
        prev_level = curr_level

    body_cont += "\t\t</table>\n"

    f.write(body_cont)


def generate_html(data):
    output_path = "periodic_table.html"

    with open(output_path, "w") as f:
        f.write("""\
                \r<!DOCTYPE html>\
                \r<html lang='en'>\n\
                \r\t<head>\
                    \r\t\t<meta charset='UTF-8'>\
                    \r\t\t<meta name='viewport' content='width=device-width, initial-scale=1.0'>\
                    \r\t\t<title>💥 Periodic table</title>\
                    \r\t\t<link rel="stylesheet" href="styles.css">\
                \r\t</head>
            """)
        f.write("\r\t<body>\n")
        f.write("\t\t<h1>Periodic Table</h1>\n")
        format_body_html(f, data)
        f.write("\t</body>\n\n")
        f.write("</html>\n")

    print(f"✅ HTML file created successfully at <{output_path}>")


def generate_css():
    code_to_write ="""
    body {font-size: 80%; background-color: #bbb; font-family: 'Arial', sans-serif; }
    table { width: 100%; table-layout: fixed; border-collapse: collapse; }
    td:not(:empty):not(:only-child) { border: 1px solid #333; padding: 10px; background-color: #999; }
    h1 { text-align: center; color: black; }
    h4 { text-align: center; color: cyan; }
    li { list-style: none; margin: 1em; margin-left: -20px; text-align: left; position: relative;}
    """
    
    with open("styles.css", "w") as f:
        f.write(code_to_write)


def main():
    file_path = "./periodic_table.txt"
    data = read_file(file_path)
    generate_html(data)
    generate_css()


if __name__ == '__main__' :
    main()
