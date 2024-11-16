from chrome_module import *


class CodePTIT:
    
    def select_language(self, driver: ChromiumPage, language):
        language_code = {
            'java': '788',
            'python': '779'
        }
        driver.get('https://code.ptit.edu.vn/student/question?course='+ language_code[language])
        
        driver.get('https://code.ptit.edu.vn/student/question')
    
    def get_num_of_page(self, driver: ChromiumPage):
        if 'student/question?page=1' not in driver.url:
            driver.get('https://code.ptit.edu.vn/student/question?page=1')

        page_items = driver.eles('xpath://li[@class="page-item"]')
        
        return len(page_items)
    
    def get_unsolved_tasks(self, page_num, driver: ChromiumPage):
        ques_data = []
        for i in range(page_num):
            driver.get('https://code.ptit.edu.vn/student/question?page=' + str(i + 1))
            question_table = driver.ele('xpath://table[@class="ques__table"]/tbody')
            unsolv_ques = question_table.eles('xpath:.//tr[not(contains(@class, "bg--10th"))]')  
            for ques in unsolv_ques:
                ques_id = ques.ele('xpath:.//td[3]').text
                ques_title = ques.ele('xpath:.//td[4]').text
                ques_url = ques.ele('xpath:.//td[3]/a').attr('href')
                ques_data.append({'id': ques_id, 'title': ques_title, 'url': ques_url})
        
        return ques_data
    
    def upload_file(self, driver: ChromiumPage, task_url, file_path):
        driver.get(task_url)
        driver.ele('xpath://input[@id="fileInput"]').input(file_path)
        submit_btn = driver.ele('xpath://button[@type="submit"]')
        submit_btn.click()
        sleep(10)
    

if __name__ == '__main__':
    driver = getDriver()
    driver.get('https://code.ptit.edu.vn')
    input('continue once finished logging in')
    code_ptit = CodePTIT()
    print(code_ptit.get_unsolved_tasks(code_ptit.get_num_of_page(driver), driver))


    
    
        
        
    