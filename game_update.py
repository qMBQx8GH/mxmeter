import subprocess
import xml.etree.ElementTree as ET

path_to_game = 'C:\\Games\\World_of_Warships'

res = subprocess.run(['hg', 'update', 'release'])
if res.returncode != 0:
    exit()

f = open('version.txt', 'r')
version = f.read()
f.close()
print('version: {}'.format(version))

res_mods = ''
f = open(path_to_game + '\\paths.xml', 'r')
xml = ET.fromstring(f.read())
f.close()
for path in xml.iter('Path'):
    if path.text.startswith('res_mods'):
        res_mods = path.text[9:]
print('res_mods: {}'.format(res_mods))

if version != res_mods:
    subprocess.run(['hg', 'merge', 'default'])
    subprocess.run(['hg', 'com', '-v', '-m', 'merge'])

    f = open('version.txt', 'w')
    f.write(res_mods)
    f.close()
    subprocess.run(['hg', 'com', '-v', '-m', res_mods, 'version.txt'])
    subprocess.run(['hg', 'tag', res_mods])
    
subprocess.run(['hg', 'update', 'default'])
