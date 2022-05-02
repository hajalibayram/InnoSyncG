import datetime
import logging
import os
import string
import random

import pandas as pd


def setup_log():
    start_time = datetime.datetime.now()
    logs_folder = "logs/"
    logs_file = f"{logs_folder}/{start_time.strftime('%Y-%m-%d_%H-%M')}.log"

    if os.path.exists(logs_folder):
        print(FileExistsError(f"{logs_folder} already exists!"))
    else:
        os.makedirs(logs_folder, exist_ok=True)
    # base_formatter = logging.Formatter('%(asctime)s   %(message)s', "%Y-%m-%d %H:%M")
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)

    open(logs_file, 'a').close()

    logging.basicConfig(filename=logs_file, filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    logging.info(f"Log file: {start_time.strftime('%Y-%m-%d_%H-%M')} \n \n ")


def get_random_pwd(length):
    # With combination of lower and upper case
    source = string.ascii_letters + string.digits

    result_str = ''.join(random.choice(source) for i in range(length))
    result_str = result_str + str(random.randint(0, 9))
    # print random string
    # print(result_str)
    return result_str


def reformat_GUsers(users):
    #### GMAIL USERS
    act_email = []
    act_name = []
    act_surn = []

    act_crt_time = []
    for u in users:
        if not u['suspended'] or u['archived'] or u['isAdmin'] or u['isDelegatedAdmin']:
            t_email = u['primaryEmail']
            if t_email.split('@')[1] == 'edu.itspiemonte.it':
                act_email.append(u['primaryEmail'])
                act_name.append(u['name']['givenName'].lower())
                act_surn.append(u['name']['familyName'].lower())
                act_crt_time.append(u['creationTime'])
    act_users_df = pd.DataFrame({'name': act_name, 'surname': act_surn, 'email': act_email, 'creation': act_crt_time})
    return act_users_df


def getNonDBUsers(db_df, g_df):
    # Users that are in Google but not in Innovaplan
    #### IN GM, NOT DB

    non_inno_users_df = g_df.merge(db_df, right_on='googleMailAllievo', left_on='email', how='left')
    non_inno_users_df = non_inno_users_df[non_inno_users_df['Allievo'].isna()].reset_index(drop=True)
    non_inno_users_df[['name', 'surname', 'email', 'creation']].to_excel('Non_DB_Gmail_Users.xlsx', index=False)
    non_inno_users_df.sort_values(by='creation', ascending=True)
    return non_inno_users_df


def getNonGUsers(db_df, g_df):
    #### IN DB, NOT GM
    non_gmail_users_df = db_df.merge(g_df, left_on='googleMailAllievo', right_on='email', how='left')
    non_gmail_users_df = non_gmail_users_df[non_gmail_users_df['Allievo'].isna()].reset_index(drop=True)
    non_gmail_users_df[['name', 'surname', 'email']].to_excel('Non_DB_Gmail_Users.xlsx', index=False)
    return non_gmail_users_df
