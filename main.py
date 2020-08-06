import requests
from bs4 import BeautifulSoup
import json

class CoursesOfUser:
    def __init__(self,url): # Borrar el id, eso deberia encontrar solo el programa
        self.url_user = url
        self.id_user =""
        self.url_courses_for_user = ""
        self.url_course_for_user_template = '{0}api-2.0/users/{1}/subscribed-profile-courses/?page_size={2}'
        self.page_size = 100 # la cantidad de cursos que se piden 
        self.url_course_0=""
    
    def make_url_courses(self):
        self.url_course_0 = self.url_user[0:self.url_user.find("user")]
        self.url_courses_for_user = self.url_course_for_user_template.format(self.url_course_0,self.id_user,self.page_size)

    def extract_courses_page(self,json_page):
        courses_page_list = []
        for course in json_page["results"]:
            url_course = self.url_course_0[0:len(self.url_course_0)-1] + course["url"]
            print(url_course)
            courses_page_list.append(url_course)
        return courses_page_list

    def extract_courses(self):
        response = requests.get(self.url_courses_for_user)
        courses_list = []
        if response.status_code!=200:
            return courses_list
        content = response.content
        json_page = json.loads(content)
        count = int(json_page["count"])
        if count <= 0:
            return courses_list
        while True:
            courses_page=self.extract_courses_page(json_page)
            courses_list+=courses_page
            print(json_page["next"])
            if json_page["next"] == None:
                break
            # Esto en otra funcion encapsulada
            response = requests.get(json_page["next"])
            if response.status_code!=200:
                break
            content = response.content
            json_page = json.loads(content)
        return courses_list

    def getId_for_url(self):
        response = requests.get(self.url_user)
        if response.status_code !=200:
            return ""
        content = response.text
        soup = BeautifulSoup(content,'html.parser')
        div_element = soup.find('div',{"data-module-id":"user-profile"})
        jsonData = json.loads(div_element.attrs["data-module-args"])
        return jsonData["user"]["id"]

    def get(self):
        self.id_user= self.getId_for_url()
        print(self.id_user)
        self.make_url_courses()
        print(self.url_courses_for_user)
        courses_list=self.extract_courses()
        return courses_list
    
    def get_to_file(self,file_name):
        courses_list=self.get()
        file_out = open(file_name,"w")
        for course in courses_list:
            file_out.write(course + '\n')
        file_out.close()
        
URL = 'https://XXXX.udemy.com/user/YYYYY/' #un perfil de usuario bussiness que encontre por ahi
                                                           # no necesita autenticacion para ver el perfil

if __name__ == "__main__":
    coursesofuser = CoursesOfUser(URL)
    #courses_list = coursesofuser.get()
    #print(len(courses_list))
    coursesofuser.get_to_file("lista_de_cursos.txt")
    ## podria guardarse en un archivo

