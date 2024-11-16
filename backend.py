from code_ptit import CodePTIT
from git_content import GitContent
from chrome_module import *
import random
from time import sleep
import traceback

class Backend:
    def __init__(self):
        self.code_ptit = CodePTIT()
        self.git_content = GitContent()
        self.driver = None
        
    def login(self):
        self.driver = getDriver()
        self.driver.get('https://code.ptit.edu.vn')
        
        
    def login_finished(self):
        try: 
            if self.driver:
                self.driver.quit()
        except:
            pass
        
    
    def run(self, type, limit = 30, min_wait = 30, max_wait = 100):
        type = type.lower()
        if not self.driver:
            driver = getDriver()
        else:
            driver = self.driver
        self.code_ptit.select_language(driver, type)
        sleep(5)
        tasks = self.code_ptit.get_unsolved_tasks(self.code_ptit.get_num_of_page(driver), driver)
        for task in tasks:
            if limit <= 0:
                break
            try:
                if task.get('url', None):
                    file_path = self.git_content.get_file(type, task.get('id'), task.get('title'))
                    if file_path == 'file not founded':
                        continue
                    self.code_ptit.upload_file(driver, task.get('url'), file_path)
                    sleep(random.uniform(min_wait, max_wait))
                    limit -= 1
                else:
                    continue
                
            except:
                traceback.print_exc()
        try:
            if driver:
                driver.quit()
        except:
            traceback.print_exc()
            
            
        
if __name__ == '__main__':
    be = Backend()
    
    # login to code ptit
    driver = getDriver()
    driver.get('https://code.ptit.edu.vn')
    input('continue once finished logging in')
    
    
    
    be.run(driver, 'java', limit= 10, min_wait= 10, max_wait=30)
    