# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import pyodbc

from GService import GService
from merger import merge
from util import get_random_pwd, reformat_GUsers, getNonGUsers, setup_log

import json

config_json = open('config.json', "r")
config_json = json.loads(config_json.read())
server = config_json['server']
port = config_json['port']
database = config_json['database']
username = config_json['username']
password = config_json['password']

if __name__ == '__main__':
    setup_log()
    # df = merge()
    # print(df)

    # s = GService('admin')
    # user_list = s.list()
    # for u in user_list:
    #     if '@edu.itspiemonte.it' in u['primaryEmail']:
    #         print(u['name']['givenName'])
    # get_random_pwd(10)

    # conn = pyodbc.connect(
    #     'Driver={SQL Server};Server=' + server + ',' + port + ';Database=' + database + ';UID=' + username + ';PWD=' + password)
    #
    # query_str = "SELECT \
    #     c.IDMateria, \
    #     c.Codice, \
    #     c.Titolo, \
    #     c.TipoCorso, \
    #     c.Materia, \
    #     c.AnnoCorso, \
    #     c.NomeBreve, \
    #     \
    #     d.docente, \
    #     d.googleMailDocente, \
    #     d.googleMailRespoCorso, \
    #     d.RespoCorso, \
    #     \
    #     a.Allievo, \
    #     a.googleMailAllievo\
    #     FROM v_classroom_corsi as c \
    #     LEFT JOIN v_classroom_docenti as d ON c.IDMateria = d.IDMateria   \
    #     LEFT JOIN v_classroom_allievo as a ON d.IDMateria = a.IDMateria   \
    #     WHERE c.Materia <> 'Stage' or c.Materia <> 'Esame' \
    #     ORDER BY c.Codice \
    #     "
    #
    # raw_df = pd.read_sql_query(query_str, conn)
    # # print(raw_df)
    # user_service = GService('admin')
    # users = user_service.list()
    # g_users_df = reformat_GUsers(users)
    # # print(g_users_df)
    #
    # # #### INNOVAPLAN USERS
    # inno_users_df = raw_df[['Allievo', 'googleMailAllievo']].drop_duplicates().reset_index(drop=True).sort_values(
    #     by='googleMailAllievo')
    # inno_users_df = inno_users_df.dropna().reset_index(drop=True)
    #
    # nonGUsers_df = getNonGUsers(inno_users_df, g_users_df)
    # # print(nonGUsers_df)
    # test_df = pd.DataFrame({'name': ['federica'], 'surname': ['anzoise']})
    # test_df = pd.DataFrame({'name': ['haji'], 'surname': ['bayram']})

    # s = GService('admin')
    # s.create(users=test_df)
    # s.suspend()

    # s = GService('admin')
    # user_list = s.list()
    # for u in user_list:
    #     if 'adrian.munteanu@edu.itspiemonte.it' in u['primaryEmail']:
    #         print(u)

    ### SUSPEND USERS
    # s = GService('admin')
    # sus_users_df = pd.read_csv('Suspend.csv')
    # users = sus_users_df['Member Email']
    # s.suspend(users)

    ### DELETE USERS
    # s = GService('admin')
    # sus_users_df = pd.read_csv('Delete.csv')
    # users = sus_users_df['Member Email']
    # s.delete(users)
