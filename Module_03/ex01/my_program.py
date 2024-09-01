#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from path import Path

# if __name__ == '__main__':
# 	path = Path('.')
# 	new_path = path / 'data'
# 	if not new_path.isdir():
# 		new_path.mkdir()
# 	new_file = new_path / 'file.txt'
# 	if not new_file.isfile():
# 		new_file.touch()
# 	new_file.write_lines(["_"*20, "File containment:", "Text sample"])
# 	new_file.write_text("Another text sample", append=True)
# 	for line in new_file.lines():
# 		print(line.replace('\n', ''))






from path import Path


def main():
    try:
        Path.makedirs('something')
    except FileExistsError as e:
        print(e)
    Path.touch('something/something')
    f = Path('something/something')
    f.write_lines(['hello', 'world!'])
    print(f.read_text())


if __name__ == '__main__':
    main()