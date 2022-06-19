import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import re

daysDic = {"ÇARŞAMBA":"Wednesday", "PERŞEMBE":"Thursday", "CUMA":"Friday", "PAZARTESİ":"Monday", "SALI":"Tuesday"}

def main():
    T = pd.read_excel(r'C:/Users/Hammam/VisualCode/Python_programming/firebase_yemekhane/Menüsü.xlsx')
    cred = credentials.Certificate("C:/Users/Hammam/VisualCode/Python_programming/firebase_yemekhane/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

    db = firestore.client()


    c = []

    for column in T:
        c.append(column)

    file = pd.DataFrame(T, columns= [c[0], c[1], c[2], c[3], c[4], c[5]])


    dates = file[file.columns[0]]
    days = file[file.columns[1]]
    soups = file[file.columns[2]]
    maindishes = file[file.columns[3]]
    sidedishes = file[file.columns[4]]
    appetisers = file[file.columns[5]]

    dates = omitDate(dates, dates[0])
    days = omitDate(days, days[0])
    soups = omitDate(soups, soups[0])
    maindishes = omitDate(maindishes, maindishes[0])
    sidedishes = omitDate(sidedishes, sidedishes[0])
    appetisers = omitDate(appetisers, appetisers[0])

    days = translateDays(days)
    weeks = []

    week = {}
    for j, day, soup, maindish, sidedish, appetiser in zip(range(len(dates)), days, soups, maindishes, sidedishes, appetisers):
        if(j - 1 > -1 or j == 0):
            if endOfWeeks(date0= dates[j - 1], date1= dates[j]):
                weeks.append(week)
                week = {}
                week[dates[j]] = {
                "day" : day,
                "mainDish": removeCalories(maindish),
                "sideDish": removeCalories(sidedish),
                "soup": removeCalories(soup),
                "appetiser": removeCalories(appetiser),
                "mainCal": getCalories(maindish),
                "sideCal": getCalories(sidedish),
                "soupCal": getCalories(soup),
                "appetiserCal": getCalories(appetiser),
                }
            else:
                week[dates[j]] = {
                "day" : day,
                "mainDish": removeCalories(maindish),
                "sideDish": removeCalories(sidedish),
                "soup": removeCalories(soup),
                "appetiser": removeCalories(appetiser),
                "mainCal": getCalories(maindish),
                "sideCal": getCalories(sidedish),
                "soupCal": getCalories(soup),
                "appetiserCal": getCalories(appetiser),
                }
                if j + 1 == len(dates):
                    weeks.append(week)

      
    i = 1
    for week in weeks:
        newdoc = db.collection("foodMenu").document("Week" + str(i))
        newdoc.set(week)
        i += 1

def getCalories(input):
    calorie = re.findall(r'[0-9]+', input)
    return ' '.join(map(str,calorie))

def removeCalories(input):
    normalizedMeal = re.sub('[(0-9)]+', '', input)
    normalizedMeal = normalizedMeal.replace('Kcal', "")
    return capitalize(str(normalizedMeal).strip().replace('.', " ").lower())

def capitalize(input):
    string = input.split(" ")
    newString = []
    for element in string:
        newString.append(element.capitalize())
    return ' '.join(newString)
        

def translateDays(days):
    for i in range(len(days)):
        days[i] = daysDic[days[i]]
    return days

def endOfWeeks(date0, date1):
    yesterday = int(date0[len(date0) - 2])*10 + int(date0[len(date0) - 1])
    today = int(date1[len(date1) - 2])*10 + int(date1[len(date1) - 1])
    if today - yesterday > 1:
        return True
    else:
        return False

def omitDate(genre, lookUpWord):
    filtered = []
    for element in genre:
        if str(lookUpWord) not in str(element):
            filtered.append(str(element).replace(" 00:00:00",""))
    return filtered

def omitEmpty(genre, lookUpWord):
    filtered = []
    for element in genre:
        if str(lookUpWord) not in str(element):
            filtered.append(str(element))
    return filtered

main()


