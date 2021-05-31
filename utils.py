# Script utils follow users fb
import os
import json
def get_base_dir():
    """
    get base dir project
    """
    return os.path.dirname(os.path.abspath(__file__))
    
def check_path_fb_scraping(path):
    """
        Si no existe el directorio lo generamos en forma cascada
             
    """
    if not os.path.exists(path):
        # si no existe el directorio log lo crea 
        print('Generate directory log..', path)
        os.makedirs(path)
    return

def get_read_html_local(username):
    """Open html label=''ocal"""
    allLines = []
    path = get_base_dir()+'/log/'
    fileList = os.listdir(path)
    for file in fileList:
       file = open(path+username+'.html', 'r')
       allLines.append(file.read())
    return allLines

def save_data_html(name_log, data_html):
    """
    save log in directory /log
    """
    path_base = get_base_dir()+'/log/' 
    path = path_base + name_log
    check_path_fb_scraping(path_base)
    f = open(path+'.html', 'w')
    f.write(str(data_html))
    f.close()
    print('Save html in log..!')
    return

def get_users_json_data():
    """
    open data users json
    """
    path = 'data/data_users.json'
    with open(path) as data_file:    
        return json.load(data_file)