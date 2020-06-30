#!/usr/bin/python3
# -*- coding: utf-8 -*-


import configparser
import datetime
import jinja2
import markdown2
import os
import pathlib
import shutil


# Load settings to get build and deployment directories
config = configparser.ConfigParser()
config.read("config.ini")
build_dir = config["directories"]["build"]
site_dir = config["directories"]["site"]


# Archive old site directory
old_site_dir = f"{site_dir}-prev"
try:
    shutil.rmtree(old_site_dir)
except FileNotFoundError:
    print("Old site directory not found")
os.rename(site_dir, old_site_dir)


# Create new site directory by copying build directory
shutil.copytree(build_dir, site_dir)




def get_extension(filename):
    return(pathlib.Path(filename).suffix)



# Load Jinja template
with open("templates/main.html.j2", "r") as template_file:
    template = jinja2.Template(template_file.read())



for root, dirs, files in os.walk(site_dir):
    for filename in files:
        if get_extension(filename) == ".md":
            markdown_file = os.path.join(root, filename)
            html_file = f"{pathlib.Path(markdown_file).with_suffix('')}.html"
            print(f"{markdown_file} --> {html_file}")

            # Render Markdown to HTML
            with open(markdown_file, "r") as mf:
                html = markdown2.markdown(mf.read(), extras=["metadata", "header-ids", "markdown-in-html", "tables"])
                html_output = template.render(title = html.metadata["Title"],
                                              content = html,
                                              last_updated = datetime.date.today().strftime("%Y-%m-%d"))

            with open(html_file, "w") as hf:
                hf.write(html_output)

            os.remove(markdown_file)
