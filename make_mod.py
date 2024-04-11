# -*- coding: utf-8 -*-

import os
import sys
import glob
import subprocess
import xml.etree.ElementTree as ET
import configparser
import zipfile
import shutil

config = configparser.ConfigParser()
config.read(sys.argv[1])
path_to_game = config['Game']['folder']
print(path_to_game)

xml_root = ET.parse(os.path.join(path_to_game, 'game_info.xml'))
xml_version = xml_root.findall(".//version[@name='client']")
version = xml_version[0].attrib['installed']
version = '.'.join(version.split('.')[0:4])
print(version)

base_dir = os.path.abspath(os.path.dirname(__file__))
dist_dir = os.path.join(base_dir, 'dist')
os.makedirs(dist_dir, exist_ok=True)

# Clean up dist folder
files = glob.glob(os.path.join(dist_dir, '*'))
for f in files:
    os.remove(f)

# Compile
project_file = config['FlashDevelop']['project']
subprocess.run([
    "C:\\Program Files (x86)\\FlashDevelop\\Tools\\fdbuild\\fdbuild.exe",
    project_file,
    "-version",
    "4.6.0; 3.1",
    "-compiler",
    "C:\\src\\flex_sdk_4.6",
    "-library",
    "C:\\Program Files (x86)\\FlashDevelop\\Library",
], shell=True, check=True)

target_dir = config['Destination']['folder']
target_suffix = config['Destination']['suffix']
target_file = 'mxmeter-' + version + '-' + target_suffix + '.zip'
zip_archive = os.path.join(target_dir, target_file)
print(zip_archive)

# Make zip archive
files = glob.glob(os.path.join('mxMeter', '**'), recursive=True)
with zipfile.ZipFile(zip_archive, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file in files:
        if os.path.isfile(file):
            zipf.write(file, os.path.join('PnFMods', file))
    zipf.write('PnFModsLoader.py', 'PnFModsLoader.py')

