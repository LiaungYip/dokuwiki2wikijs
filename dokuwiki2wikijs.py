#! /usr/bin/env python3

import os
import re
from zipfile import ZipFile
from os.path import basename


def convert_to_markdown(infile, outfile):
    os.system("pandoc -f dokuwiki -t markdown -o " + outfile + " " + infile)


def unquote_markdown_headings(lines):
    for i in range(len(lines)):
        lines[i] = lines[i].replace('\#', '#')

if __name__ == "__main__":
    for folder, _, files in os.walk(os.path.curdir):
        txt_files = (file for file in files if file.endswith(".txt"))
        for f in txt_files:
            filename_with_txt = os.path.join(folder, f)
            print(filename_with_txt+":", end="")

            filename_with_txt_md = filename_with_txt+".md"
            convert_to_markdown(filename_with_txt, filename_with_txt_md)

            file = open(filename_with_txt_md)

            lines = file.readlines()
            unquote_markdown_headings(lines)

            # Assume first line (heading) is used as page name so use that as title attribute
            title = lines[0].partition(' ')[2]

            basename = filename_with_txt[:-4]

            # Convert %C3 in filename to Unicode
            # ...

            filename_with_md = basename+".md"
            with open(filename_with_md, "w") as file:
                file.write("---\n")
                file.write("title: "+title)
                file.write("---\n")
                file.writelines(lines)

            os.remove(filename_with_txt_md)

    with ZipFile("dokuwiki.zip", 'w') as zipObj:
        # Walk through the files in a directory
        for folder, folders, files in os.walk(os.path.curdir):
            files = (file for file in files if file.endswith(".md"))
            for file in files:
                zipObj.write(os.path.join(folder, file))
    print("'dokuwiki.zip' created\n")