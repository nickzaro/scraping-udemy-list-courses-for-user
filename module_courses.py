import requests
from bs4 import BeautifulSoup
import json


class CoursesOfUser:
    def __init__(self, url):
        self.url_user = url
        self.id_user = ""
        self.url_courses_for_user = ""
        self.url_course_for_user_template = '{0}api-2.0/users/{1}/subscribed-profile-courses/?page_size={2}'
        self.page_size = 100  # la cantidad de cursos que se piden
        self.url_course_0 = ""

    # Parte inicial de la direccion, https://XXXXX.udemy.com/ para usuarios y usuarios Business
    def make_url_course_0(self):
        self.url_course_0 = self.url_user[0:self.url_user.find("user")]

    # Arma la direccion api para consultar los cursos
    def make_url_courses_for_user(self):
        self.url_courses_for_user = self.url_course_for_user_template.format(self.url_course_0, self.id_user,
                                                                             self.page_size)

    # Extrae los cursos del json lista de cursos
    def extract_courses_page(self, json_page):
        courses_page_list = []
        for course in json_page["results"]:
            if course["price_detail"]!=None: #cursos gratis no
                url_course = self.url_course_0[0:len(self.url_course_0) - 1] + course["url"]
                print(url_course)
                courses_page_list.append(url_course)
        return courses_page_list

    # Realiza las peticiones a la api de udemy, hasta que se terminen las paginas de cursos
    def extract_courses(self):
        response = requests.get(self.url_courses_for_user)
        courses_list = []
        if response.status_code != 200:
            return courses_list
        content = response.content
        json_page = json.loads(content)
        count = int(json_page["count"])
        if count <= 0:
            return courses_list
        while True:
            courses_page = self.extract_courses_page(json_page)
            courses_list += courses_page
            print(json_page["next"])
            if json_page["next"] == None:
                break
            # Esto en otra funcion encapsulada
            response = requests.get(json_page["next"])
            if response.status_code != 200:
                break
            content = response.content
            json_page = json.loads(content)
        return courses_list

    # Scrapea el contenido de la url, buscando el id de usuario
    def getId_for_url(self):
        response = requests.get(self.url_user)
        if response.status_code != 200:
            return ""
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        div_element = soup.find('div', {"data-module-id": "user-profile"})
        jsonData = json.loads(div_element.attrs["data-module-args"])
        return jsonData["user"]["id"]

    def get(self):
        self.id_user = self.getId_for_url()
        print(self.id_user)
        self.make_url_course_0()
        self.make_url_courses_for_user()

        print(self.url_courses_for_user)
        courses_list = self.extract_courses()
        return courses_list

    # Extrae el id de usuario y la url0 de una cookie
    def read_cookie(self, cook_file):
        cook_file = open(cook_file);
        cook_lines = cook_file.readlines()
        for line in cook_lines:
            # print (line)
            if line.find("referer") >= 0:
                self.url_course_0 = line[line.find('https'):line.find('home')]
                print(self.url_course_0)

            if line.find("x-udemy-cache-user") >= 0:
                self.id_user = line[line.find(':') + 2:-1]
                print(self.id_user)
        cook_file.close()

    # Lista de cursos usando una cookie
    def get_of_cookie(self, cook_file):
        self.read_cookie(cook_file)
        self.make_url_courses_for_user()
        print(self.url_courses_for_user)
        courses_list = self.extract_courses()
        return courses_list

    # guarda en disco la lista de cursos del usuario

    def get_to_file(self, file_name):
        courses_list = self.get()
        file_out = open(file_name, "w")
        for course in courses_list:
            file_out.write(course + '\n')
        file_out.close()

    def get_cookie_to_file(self, cook_file, file_out):
        courses_list = self.get_of_cookie(cook_file)
        file_out = open(file_out, "w")
        for course in courses_list:
            file_out.write(course + '\n')
        file_out.close()
