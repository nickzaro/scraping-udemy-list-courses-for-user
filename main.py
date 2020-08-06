from module_courses import CoursesOfUser

        
URL = 'https://XXXX.udemy.com/user/YYYYY/' #un perfil de usuario bussiness que encontre por ahi
                                           # no necesita autenticacion para ver el perfil

if __name__ == "__main__":
    coursesofuser = CoursesOfUser(URL)
    #courses_list = coursesofuser.get()

    # coursesofuser.get_to_file("lista_de_cursos.txt")

    # cok_wiss cokkie
    # lista_de_cirsos.txt archivo de salida
    coursesofuser.get_cookie_to_file('cok_wiss.txt',"lista_de_cursos.txt")
    

