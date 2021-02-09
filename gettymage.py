import requests
from bs4 import BeautifulSoup
import os, os.path, errno
from zipper import zip
import re

if not os.path.exists('output'):
    os.mkdir('output')


getty_target = input('Enter the page link from which you want to extract images:- ')
if getty_target[-1] != "/":
    getty_target=getty_target+'/'
getty_name=input('Enter a name for the zip file:- ')
try:
    os.makedirs('output/'+getty_name)
except FileExistsError:
    print("[-] Directory Already Exists!!")
    exit()
# print(getty_target)
try:
    getty_target_html = requests.get(getty_target)
except requests.exceptions.MissingSchema:
    print("[-] Invalid Link")
    os.removedirs('output/'+getty_name)
    exit()
soup = BeautifulSoup(getty_target_html.content, features="html.parser")
# print(soup.prettify())
images = []
for img in soup.findAll('img'):
    images.append(img.get('src'))
print(f'Total {len(images)} Images Found...')
# print(images)
i=1
for link in images:
    if link == '':
        continue
    if re.search("(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))",link) is None:
        # print(1)
        link=getty_target+link
    if link[0] == '.':
        updated_link = link.replace('.', '')
        link = getty_target + updated_link
    temp=link.split(".")
    if len(temp)<1:
        link=link+".png"

    filename = link.split('/')[-1]
    print(f'[{i}] Downloading {filename}.....')
    try:
        image = requests.get(link)
        with open('output/'+getty_name+'/'+filename,'wb') as f:
            f.write(image.content)
            i=i+1
    except Exception:
        print('Something Went Wrong')
        os.removedirs('output/'+getty_name)
        exit()

print('[+] Done\n')
zip('output/'+getty_name+'/', 'output/'+getty_name+'/'+getty_name+'.zip')

