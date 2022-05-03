import logging
import os

import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from util import get_random_pwd, strip_accents


class GService:
    name = None
    service = None
    SCOPES = ['https://www.googleapis.com/auth/classroom.courses',
              'https://www.googleapis.com/auth/admin.directory.user',
              'https://www.googleapis.com/auth/apps.licensing']

    CREDENTIALS_FILE = 'credentials.json'

    def __init__(self, name='admin'):
        self.name = name
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        if self.name == 'classroom':
            self.service = build('classroom', 'v1', credentials=creds)
        elif self.name == 'admin':
            self.service = build('admin', 'directory_v1', credentials=creds)
        else:
            self.service = build('licensing', 'v1', credentials=creds)
        # return cls.service

    def getService(self):
        return self.service

    def list(self, **kwargs):
        if self.name == 'classroom':
            # Call the Classroom API
            print('Getting list of classes>>>>')
            logging.info('Getting list of classes>>>>')

            #     results = service.courses().list(pageSize=10).execute()
            #     courses = results.get('courses', [])

            classrooms_all = []
            page_token = None
            while True:
                classrooms_t = self.service.courses().list(pageToken=page_token).execute()
                classrooms_all.extend(classrooms_t['courses'])

                page_token = classrooms_t.get('nextPageToken')
                if not page_token:
                    break
            # print(classrooms_all)
            return classrooms_all
        elif self.name == 'admin':
            # Call the Admin API
            print('Getting list of users>>>>')
            logging.info('Getting list of users>>>>')

            users_all = []
            page_token = None
            while True:
                users_t = self.service.users().list(customer='my_customer',
                                                    orderBy='email',
                                                    pageToken=page_token).execute()
                users_all.extend(users_t['users'])

                page_token = users_t.get('nextPageToken')
                if not page_token:
                    break
            # print(users_all)
            return users_all
        if kwargs.get('isLicense'):
            print('Getting list of licenses>>>>')
            logging.info('Getting list of licenses>>>>')

            lic = self.service.licenseAssignments().get(productId='101031',
                                                        userId=kwargs.get('userId'),
                                                        skuId='1010310008').execute()
            print(lic)
            logging.info(lic)

    def emailExist(self, email, domain, username, number=1):
        try:
            if self.service.users().get(userKey=email).execute()['kind'] == 'admin#directory#user':
                username2 = username + str(number)
                email2 = username2 + domain
                self.emailExist(email2, domain, username2, number=number + 1)
                return email2, username2
        except HttpError:
            return email, username
        except Exception as e:
            print(e)
            logging.error(e)

    def create(self, **kwargs):
        if self.name == 'admin':
            domain = '@edu.itspiemonte.it'
            emails = []
            pwds = []
            users_df = kwargs.get('users')
            for index, u in users_df.iterrows():
                pwd = get_random_pwd(8)
                name = u['name'].split(' ')[0]
                name = name.strip().replace("\'", "")
                name = name.strip().replace(" ", "")
                name = name.strip().replace("\"", "")

                surname = u['surname']
                surname = surname.strip().replace("\'", "")
                surname = surname.strip().replace(" ", "")
                surname = surname.strip().replace("\"", "")

                if ' ' in surname:
                    if surname.startswith('di') or surname.startswith('de') or surname.startswith('al'):
                        surname = u['surname']
                    else:
                        surname = surname.split(' ')[0]

                username = strip_accents(name + '.' + surname)
                email = username + domain
                print(email)
                logging.info(email)
                # print(self.service.users().get(userKey=email).execute())

                email, username = self.emailExist(email, domain, username)

                emails.append(username)
                pwds.append(pwd)

                req_body = {
                    "primaryEmail": email,
                    "name": {
                        "givenName": u['name'].title(),
                        "familyName": u['surname'].title(),
                        "fullName": u['name'].title() + ' ' + u['surname'].title()
                    },
                    "isAdmin": False,
                    "isDelegatedAdmin": False,
                    "password": pwd,
                    "changePasswordAtNextLogin": True,
                    "kind": "admin#directory#user",
                    "orgUnitPath": "/itspiemonte.it/edu.itspiemonte.it",
                    "languages": [
                        {
                            "languageCode": "it",
                            "preference": "preferred"
                        }
                    ],
                    # "recoveryEmail": "",
                    # "recoveryPhone": ""
                }
                if u['email']:
                    req_body['recoveryEmail'] = u['email']
                if u['phone']:
                    req_body['recoveryPhone'] = u['phone']

                # self.service.users().insert(body=req_body).execute()
            pd.DataFrame({'uname': emails, 'pwd': pwds}).to_excel('upwd.xlsx', index=False)
            print('Created: \n', emails)
            logging.info('Created: \n', emails)

            # setLicense(email)

    def suspend(self, users, **kwargs):
        for user in users:
            try:
                user = user.strip()
                self.service.users().update(userKey=user, body={'suspended': True}).execute()
                print(user, ' is suspended')
                logging.info(user + ' is suspended')
            except:
                continue

    def delete(self, **kwargs):
        if kwargs.get('users'):
            for user in kwargs.get('users'):
                user = user.strip()
                self.service.users().delete(userKey=user).execute()
                print(user, ' is suspended')
                logging.info(user + ' is suspended')

    def setLicence(self, userId):
        req_body = {
            'userId': userId
        }
        lic = self.service.licenseAssignments().insert(productId='101031',
                                                       skuId='1010310008',  # Education Plus
                                                       body=req_body).execute()
        print('License is created for ', userId)
        logging.info('License is created for ', userId)
        return lic

    def deleteLicence(self, userId):
        req_body = {
            'userId': userId
        }
        try:
            lic = self.service.licenseAssignments().delete(productId='101031',
                                                           skuId='1010310008',  # Education Plus
                                                           body=req_body).execute()
            print('License is deleted for ', userId)
            logging.info('License is deleted for ', userId)

            return lic

        except HttpError:
            print('Alert! Error occurred while deleting license from', userId)
            logging.error('Alert! Error occurred while deleting license from', userId)
