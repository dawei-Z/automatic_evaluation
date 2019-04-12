from google import google
import re
import urllib
from bs4 import BeautifulSoup
import pandas as pd


staffList = {'header': "", 'name': ""}
errorList = {}
queryHeader = "computer science academic staff of"


def readDepList():
    f = open("list.txt", encoding='utf-8')
    for line in f:
        line.encode("ascii", "ignore")
        query = queryHeader + line
        results = google_query(query)
        if len(results) != 0:
            result = results[0]
            new_staffs = ""
            staffs = get_staff_info(result.name, result.link)
            if staffs:
                for staff in staffs:
                    clear_staff = staff.strip()
                    splitstr = clear_staff.split(" ", 1)
                    if len(splitstr) > 1:
                        staffList['header'] = splitstr[0]
                        staffList['name'] = splitstr[1]
                        print(staffList['name'])
                        new_staffs += staffList['name'] + '\n'
                with open('staffLists\\' + line.strip() + '.txt', 'w', encoding='utf-8') as newFile:
                    newFile.write(new_staffs)
            else:
                errorList[line] = result.link
                print('Can not find staff info from ', line)
        else:
            errorList[line] = 'noURL'
            print("no query result of " + line)
    file = open('invalidUni.txt', 'a')
    for key, value in errorList.items():
        file.write(key.rstrip() + ':' + value + '\n')
    file.close()
    f.close()


def init_series(uni_name, staff,  citation, hindex):
    if uni_name == 'university':
        return None
    else:
        newSerires = pd.Series({'university': uni_name,
                            'staffName': staff,
                            'citationInfo': citation,
                            'hindex': hindex})
        return newSerires


def google_query(query):
    query_result = google.search(query)
    return query_result


def get_staff_info(name, url):
    try:
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page)
        htmlLine = soup.get_text()
        staffs = find_staff(htmlLine)
        return staffs
    except urllib.error.HTTPError:
        errorList[name] = url
        print(urllib.error.HTTPError)


def find_staff(htmlLine):
    professor = re.findall('Prof\w+\s[A-Z]\w+\s[A-Z]\w+', htmlLine)
    doctor = re.findall('Dr\s[A-Z]\w+\s[A-Z]\w+',htmlLine)
    staff = professor + doctor
    return staff


def testing(query):
    results = google_query(query)
    result = results[0]
    staffs = get_staff_info(result.name, result.link)
    print(staffs)

#  readDepList()
