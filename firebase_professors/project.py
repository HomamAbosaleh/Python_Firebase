import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import re

daysDic = {"ÇARŞAMBA":"Wednesday", "PERŞEMBE":"Thursday", "CUMA":"Friday", "PAZARTESİ":"Monday", "SALI":"Tuesday"}

def main():
    T = pd.read_excel(r'C:/Users/Hammam/VisualCode/Python_programming/firebase_professors/professors.xlsx')
    cred = credentials.Certificate("C:/Users/Hammam/VisualCode/Python_programming/firebase_yemekhane/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    namesOfFaculity = {"Computer Engineering":"Faculty of Engineering", "Electrical and Electronics Engineering": "Faculty of Engineering", "Industrial Engineering":"Faculty of Engineering", "Mechanical Engineering":"Faculty of Engineering", "Civil Engineering":"Faculty of Engineering", "Nanotechnology Engineering": "Faculty of Engineering", "Architecture":"Faculty of Architecture", "Political Science and International Relations":"Faculty of Humanities and Social Sciences", "Psychology":"Faculty of Humanities and Social Sciences", "Molecular Biology and Genetic":"Faculty of Life and Natural Sciences", "Bioengineering":"Faculty of Life and Natural Sciences", "Business Administration": "Faculty of Managerial Sciences","Economy":"Faculty of Managerial Sciences"}
    c = []

    for column in T:
        c.append(column)
    

    file = pd.DataFrame(T, columns= [c[0], c[1], c[2], c[3], c[4], c[5], c[6]])

    professors = []

    names = file[c[0]]
    surnames = file[c[1]]
    emails = file[c[2]]
    positions = file[c[3]]
    titles = file[c[4]]
    departments = file[c[5]]
    images = file[c[6]]

    for name, surname, email, position, title, department, image in zip(names, surnames, emails, positions, titles, departments, images):
        professors.append({
            "name": name.strip(),
            "surname": surname.strip(),
            "email": email.strip(),
            "position": position,
            "title": title,
            "department": department.strip(),
            "faculty": namesOfFaculity[department],
            "image": image.strip(),
        })
    
    mapOfProfessors = {"Computer Engineering":[], "Electrical and Electronics Engineering": [], "Industrial Engineering":[], "Mechanical Engineering":[], "Civil Engineering":[], "Nanotechnology Engineering": [], "Architecture":[], "Political Science and International Relations":[], "Psychology":[], "Molecular Biology and Genetic":[], "Bioengineering":[], "Business Administration":[],"Economy":[]}
    listOfDepartments = ["Computer Engineering", "Electrical and Electronics Engineering", "Industrial Engineering", "Mechanical Engineering", "Civil Engineering", "Nanotechnology Engineering", "Architecture", "Political Science and International Relations", "Psychology", "Molecular Biology and Genetic", "Bioengineering", "Business Administration","Economy"] 

    for i in range(len(listOfDepartments)):
        for professor in professors:
            if professor["department"] == listOfDepartments[i]:
                mapOfProfessors[listOfDepartments[i]].append(professor)

        

    for department in mapOfProfessors:
        newdoc = db.collection("faculties").document(namesOfFaculity[department]).collection(department).document("professors")
        newdoc.set({ "professors" : mapOfProfessors[department]})


main()


