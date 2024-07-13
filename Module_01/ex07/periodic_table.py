def string_to_dict(line):
    data_dict = dict()
    list_name_of_elem__other_data = line.split("=")
    data_dict['name'] = list_name_of_elem__other_data[0].strip(" ")
    list_data = list_name_of_elem__other_data[1].split(",")
    for data in list_data:
        list_cat__data = data.split(":")
        data_dict[list_cat__data[0].strip(" ")] = list_cat__data[1].strip(" \n")
    return data_dict


def read_file():
    with open("periodic_table.txt", "r") as f:
        list_of_data_dict = []
        for line in f:
            data_dict = string_to_dict(line)
            list_of_data_dict.append(data_dict)
        return list_of_data_dict


def content(f, list_of_data_dict):
    prev = 0
    cur = 0
    s = "<table>"
    for one_elem_dict in list_of_data_dict:
        cur = int(one_elem_dict['position'])
        if cur == 0:
            s +="<tr>"
        if cur - prev > 1:
            s += "<td colspan='" + str(cur - prev - 1) + "'></td>"
        # s += "<td style='border: 1px solid black; padding:10px'>\n<h4>" + one_elem_dict['name'] + "</h4>\n"
        s += "<td>\n<h4>" + one_elem_dict['name'] + "</h4>\n"
        s += "<ul><li>" + one_elem_dict['number'] +"</li>\n" \
            "<li>" + one_elem_dict['small'] +"</li>\n" \
            "<li>" + one_elem_dict['molar'] + "</li>\n" \
            '<li>' + one_elem_dict['electron'] + "</li>\n" \
            "</ul></td>"
        if cur == 17:
            s += "</tr>"
            cur = 0
        prev = cur
    s += "</table>"
    f.write(s)


def write_to_html(data):
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
        content(f, data)
        f.write("\t</body>\n")
        f.write("</html>\n")

    print(f"✅ HTML file created successfully at: {output_path}")


def write_to_css():
    code_to_write ="""
    body {font-size: 80%;}
    table { width: 100%; table-layout: fixed; border-collapse: collapse; }
    td { padding: 10px; }
    td:not(:empty):not(:only-child) { border: 1px solid red; }
    h4 { text-align: center; color: red; }
    li { list-style: none; margin: 1em; margin-left: -23pt; text-align: left; }
    """
    with open("styles.css", "w") as f:
        f.write(code_to_write)

def generate_html():
    data = read_file()
    write_to_html(data)


def generate_css():
    write_to_css()


def generate_files():
    generate_html()
    generate_css()


def main():
    generate_files()


if __name__ == '__main__' :
    main()
