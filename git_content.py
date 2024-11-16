import requests 
import os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
sep = os.sep
links_path = dir_path + sep + 'github.json' 
data_store =  dir_path + sep + 'srcs'


class GitContent:
    def __init__(self):
        self.paths = {}
        self.get_links()
        
    def store_file(self, content, type, id):
        if not os.path.exists(data_store):
            os.mkdir(data_store)
        if not os.path.exists(data_store + sep + type):
            os.mkdir(data_store + sep + type)
            
        if type == 'java':
            ext = '.java'
        elif type == 'python':
            ext = '.py'
        else:
            type = '.txt'
            
        file_path = data_store + sep + type + sep + id + ext
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return file_path
        
    
    def get_links(self):
        if os.path.exists(links_path):
            with open(links_path, 'r', encoding='utf-8') as f:
                self.paths = json.load(f)
                
    
    def format_content(self, content):
        while '/*' and '*/' in content:
            first_content = content.split('/*', 1)[0]
            second_contents = content.split('*/', 1)
            if len(second_contents) > 1:
                second_content = second_contents[1]
            else:
                second_content = ''
            content = first_content + second_content    
            
        return content
    
    def download_content(self, type, code, name):
        root_url = self.paths[type] + '/raw/refs/heads/main/'
        file_url = root_url + code + ' - ' + name
        res = requests.get(file_url)
        if res.status_code != 200:
            return 'file not founded'
        file_content = res.text
        return file_content
    
    def get_file(self, type, id, name):
        file_content = self.download_content(type, id, name)
        if file_content == 'file not founded':
            return 'file not founded'
        file_content = self.format_content(file_content)
        file_path = self.store_file(file_content, type, id)
        return file_path

if __name__ == '__main__':
    get_content = GitContent()
    path = get_content.get_file('java', 'HELLOJAR', 'PHÂN TÍCH THỪA SỐ NGUYÊN TỐ')
    print(path)