"""
Author: Harrison Gropper
Date: 6/16/2021
Version: 1.0.0
Title: Easy Whiteboard

PURPOSE: This program automatically
checks every whiteboard and adds missing 
instructors if needed.
"""


# Imports packages
try:
    # Python libraries
    continue_ = True
    import requests
    from bs4 import BeautifulSoup as bs 
    import time
    import json
    import random
    import collections
    from datetime import date
except:
    log("Could not import libraries!")
    log("Check ReadMe to see what needs to be installed.")
    log("Exiting program...")
    continue_ = False


def log(string):
    from datetime import date
    '''Prints and logs information to the log.txt file'''
    file = open(str(date.today().strftime("%B %d, %Y").replace(",","").replace(" ","-")) + '-log.txt', 'a+')
    file.write("\n" + string)
    file.close()
    print(string)

def start():
    '''starts running the program'''
    from datetime import date
    # Create a starting file with today's date
    todaysDate = date.today().strftime("%B %d, %Y").replace(",","").replace(" ","-")
    file = open((str(todaysDate) + "-log.txt"), 'a+')

    # Write the first line to the console
    print("Hello! Today's date is " + str(todaysDate))
    file.write("Hello! Today's date is " + str(todaysDate))
    file.close()

    # Add small delay
    time.sleep(random.randint(1,2))

    # Initializing application
    log("Initializing application...")
    log("Checking for the config file...")

    try:
        file = open("config.txt", "r")
        file.close()
    except:
        log("No config file detected.")
        log("Creating new config file...")
        file.close()

        file = open('config.txt', 'w')
        file.write("email = \npassword = \ntotal instructors =\n")
        file.close()
        log("A new config file has been created!")
        log("The program has stopped running.")
        log("Please input the correct information in the config file.")
        continue_ = False

    log("Logging in to ConexED...")
    log("Submitting email and password...")
    
def login(email,password, continue_):
    '''Logs the user in and establishes a connection'''
    if continue_:
        loop = True
        counter = 0
        while loop:
            try:
                # making the call using this link
                loginLink = 'https://my.craniumcafe.com/login/authenticate'

                # Starting a session that will hold cookies
                session = requests.Session()

                # creating session header before sending request
                session.headers = {
                    'authority': 'my.craniumcafe.com',
                    'method': 'POST',
                    'path': '/login/authenticate',
                    'scheme': 'https',
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-length': '115',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'origin': 'https://my.craniumcafe.com',
                    'referer': 'https://my.craniumcafe.com/login/external?i=176&sics=0',
                    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest'
                }

                loginInfo = {
                    'login_field': email,
                    'password': password
                }

                # Logging in and getting boolean value if true
                loginResponse = session.post(loginLink, data = loginInfo)
                loginResponse = json.loads(loginResponse.text)['success']

                if (loginResponse):
                    log("Login successful!")
                    loop = False
                    return session, continue_
                else:
                    log("Login unsuccessful! Please check the config file and type in a correct email/password.")
                    counter += 1
                    log("Connection error. Attempt number " + str(counter))
                    log("Retrying in 5 seconds...")
                    for i in range(1,6):
                        print(str(i) + " second(s) left.")
                        time.sleep(1)

                    if counter >= 2:
                        loop = False
                        continue_ = False
            except:
                pass
                

        if continue_ == False and loop == False:
            log("Cannot connect to the internet.")
            log("The program has ended.")

def getData(session, continue_):
    '''Retrieves data about all the whiteboards'''
    if continue_:
        # creating session headers for getting whiteboard ids
        session.headers = {
            'authority': 'mathnasium.craniumcafe.com',
            'method': 'GET',
            'path': '/document-library',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'referer': 'https://mathnasium.craniumcafe.com/directory/by-department',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
        }

        log("Retrieving all existing whiteboards...")
        wib = session.get('https://mathnasium.craniumcafe.com/document-library')


        if wib.ok:
            log("Whiteboards successfully retrieved!")
            return session, wib, continue_
        else:
            log("Could not retrieve whiteboards.")
            log("Please try restarting the program.")
            continue_ = False

     
def main():
    continue_ = True
    '''Runs the program'''

    try:
        file = open('config.txt','r')
        data = file.readlines()
        for credentials in data:
            if 'email' in credentials:
                email = (credentials.split("=")[1].strip())
            if 'password' in credentials:
                password = (credentials.split("=")[1].strip())
            if 'delay' in credentials:
                delay = int(credentials.split("=")[1].strip())
        file.close()
    except:
        log("Could not read config file properly.")
        continue_ = False

    if continue_:
        start()

    if continue_:
        session, continue_ = login(email ,password, continue_)

    if continue_:
        session, wib, continue_ = getData(session, continue_)

    if continue_:
        try:
            # Looks for all existing whiteboards and their ids
            wibHtml = bs(wib.content, 'html.parser')
            ids = []
            for wib in wibHtml.findAll('tr'):
                try:
                    whiteboardID = (wib.findAll('div')[0].get('id').strip('checkbox-holder-'))
                    if int(whiteboardID) >= 0:
                        ids.append(whiteboardID)
                except:
                    pass
            if len(ids) == 0 or whiteboardID == None:
                log("Failed to grab whiteboard ids.")
                log("Ending program.")
                continue_ = False

        except:
            log("Could not grab whiteboard ids.")
            log("Was the html code of the ConexED page updated?")
            continue_ = False
        log(str(len(ids)) + " whiteboards detected!")

        log("Opening config file to view the total number of instructors...")
        try:
            file = open('config.txt', 'r')
            instructorData = []
            currentData = []
            configData = file.readlines()
            i = 0
            for data in configData:
                if 'mr.' in data.lower() or 'ms.' in data.lower():
                    
                    # Instructor Name
                    currentData.append(str(data.split(" ")[0] + " " + data.split(" ")[1].strip()))

                    # Instructor ID
                    currentData.append(str(data.split(" ")[-1].strip()))

                    
                    instructorData.append(currentData)
                    currentData = []

            if len(instructorData) != 0:
                log(str(len(instructorData)) + " instructors detected!")
            else:
                log("Could not detcted any instructors!")
                log("Ending Program")
                continue_ = False

        except:
            log("Instructor detection failed!")
            log("Please check the config file and restart the program.")
            log("Program Ending...")
            continue_ = False

        # Splitting the instructorData into two lists
        instructorNames = []
        instructorIDs = []
        if continue_:
            for data in instructorData:
                instructorNames.append(data[0])
                instructorIDs.append(data[1])
            instructorNames.append("Mathnasium of Hillsborough")

    if continue_:
        log("Collecting whiteboard ids...")
        log("Collecting added instructors...")
        log("Collecting whiteboard titles...")
        log("Collecting dates of whiteboards...")

        # Contains all import data
        ALLDATA = []

        # holds the data of one whiteboard to add to a 
        # list of whiteboards
        dataHolder = []

        # counter
        counter = 0

        try:
            for boards in ids:
                try:
                    counter += 1

                    # contains added instructors and students
                    wibInfo = wibHtml.findAll('tr')[counter].text.strip().lower()

                    # Checks to see if html page changed
                    if wibHtml.findAll('tr')[0].text.strip().lower() != 'select\nwhiteboard name\nusers\ndate created\ntimestamp\n\nadd/remove users\nlink\ndelete':
                        log("HTML DETECTION - WEBSITE CHANGED")
                        log("Tell Harrison! He will know what to do!")
                        log("Ending program...")
                        time.sleep(5)
                        continue_ = False
                        break

                    # finding date of creation
                    dateCreated = wibInfo.split("\n")[:-1][-1].capitalize()

                    # finding student name 
                    student = wibInfo.split("\n")[0].split(" ")[:-1]
                    # student = (student[0].capitalize() + " " + student[1].capitalize() + " " + student[2])

                    # finding all instructors
                    instructors = wibInfo.split("\n")
                    instructors.pop(0)
                    instructors.pop(-1)
                    worker = ''
                    totalInstructors = []

                    # Capitalizing first and last names
                    for instructor in instructors[0].split(","):
                        for word in instructor.split(" "):
                            if word != "of":
                                word = word.capitalize()
                            worker += (word + " ")

                        # sometimes extra watchers are added
                        if '_' not in worker:
                            totalInstructors.append(worker.strip())
                        worker = ''

                     # checks to see if it is a whiteboard   
                     # then adds number of instructors
                     # students
                     # board IDs
                     # date created
                    if 'Mathnasium of Hillsborough' in totalInstructors:
                        dataHolder.append(student)
                        dataHolder.append(dateCreated)
                        dataHolder.append(totalInstructors)
                        dataHolder.append(boards)
                        ALLDATA.append(dataHolder)

                        # resets the dataHolder
                        dataHolder = []
                except:
                    pass
        except:
            log("Unsuccessful! Unknown Error.")
            log("Check config file and restart program.")
            log("Program ended.")
            continue_ = False

        log("Collected all data!")
        log("Successful!")

    end = 0
    if continue_:
        counter = 0
        for section in ALLDATA:
            if continue_:
                try:
                    counter += 1
                    name = ''
                    date = ''
                    whiteboardID = ''
                    numOfInstructors = ''
                    missingInstructors = []
                    instructorIDsToAdd = []
                    currentData = []

                    for word in section[0]:
                        name += (str(word.capitalize()) + " ")

                    date += str(section[1])

                    whiteboardID += str(section[-1])

                    numOfInstructors += str(len(section[2]))
                    
                    for instructor in instructorNames:
                        if instructor not in section[2]:
                            missingInstructors.append(instructor)

                    for data in ALLDATA[counter-1][2]:
                        if '_' not in data:
                            currentData.append(data)

                    if (collections.Counter(currentData) == collections.Counter(instructorNames)) or missingInstructors == []:
                        log("#" + str(counter) + " All instructors already added!")
                    else:
                        # Gets missing instructor's ids to add to the whiteboard
                        for missing in missingInstructors:
                            index = instructorNames.index(missing)
                            instructorIDsToAdd.append(instructorIDs[index])

                        # generating payload to send
                        payload = []
                        for ids in instructorIDsToAdd:
                            pair = ('users[]', ids)
                            payload.append(pair)
                        lastPair = ('wbid', whiteboardID)
                        payload.append(lastPair)

                        # getting session headers ready to make post request
                        session.headers = {
                            'authority': 'mathnasium.craniumcafe.com',
                            'method': 'POST',
                            'path': '/document-library/ajax-update-whiteboard-guests',
                            'scheme': 'https',
                            'accept': 'application/json, text/javascript, */*; q=0.01,',
                            'accept-encoding': 'gzip, deflate, br',
                            'accept-language': 'en-US,en;q=0.9',
                            'content-length': '32',
                            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                            'csrf-token': wibHtml.find('meta',{'name':'csrf'}).get('content'),
                            'origin': 'https://mathnasium.craniumcafe.com',
                            'referer': 'https://mathnasium.craniumcafe.com/document-library',
                            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-fetch-dest': 'empty',
                            'sec-fetch-mode': 'cors',
                            'sec-fetch-site': 'same-origin',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
                            'x-requested-with': 'XMLHttpRequest'
                        }

                        whiteboardLink = 'https://mathnasium.craniumcafe.com/document-library/ajax-update-whiteboard-guests'
                        postResponse = session.post(whiteboardLink, data = payload)
                        success = json.loads(postResponse.content)["success"]
                        if success:
                            log("#" + str(counter) + " Detected missing instructors...")
                            log("#" + str(counter) + " Preparing to add instructors...")
                            log("#" + str(counter) + " Added users(" + str(len(missingInstructors)) + "): " + str(missingInstructors))
                            time.sleep(delay)
                            success = False
                        else:
                            pass
                except:
                    log("Establishing another connection...")
                    session,continue_ = login(email,password,continue_)
                    session, wib,continue_ = getData(session,continue_)
                    end += 1
                    if end == 3:
                        log("Cannot establish a connection...")
                        log("Program ending...")
                        continue_ = False
                        break

        if continue_:
            log("#DONE All users added successfully! Program ending...")
            time.sleep(10)

    if continue_ == False:
        log("The program has ended.")
        time.sleep(5)

if __name__ == "__main__":
    main()
