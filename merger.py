import pandas as pd


def get_candidati():
    candidati_df = pd.read_csv('Candidati.csv', infer_datetime_format=True)
    pd.set_option('display.float_format', lambda x: '%.0f' % x)
    candidati_df = candidati_df[
        ['numeroMatricola', 'cognome', 'nome', 'dataNascita', 'cellulare', 'email', 'sesso', 'statoCandidatura']]
    candidati_df = candidati_df[candidati_df['statoCandidatura'] == 'Chiuso']
    candidati_df['cellulare'] = candidati_df['cellulare'].astype('int64')
    # candidati_df = candidati_df.dropna(subset = ['email'])
    candidati_df['dataNascita'] = pd.to_datetime(candidati_df.dataNascita, format='%d/%m/%Y')
    candidati_df['dataNascita'] = candidati_df['dataNascita'].dt.strftime('%Y/%m/%d')

    candidati_df = candidati_df.drop_duplicates().reset_index(drop=True)
    return candidati_df


def get_corsi():
    with open('corsi.txt', 'r') as f:
        content = f.readlines()

    corsi = [x.replace('\n', '') for x in content if x[0] != '#']
    return corsi
    # corsi = ['DSG', 'WDV', 'MGD', 'BSI', 'ISS', 'CSP', 'FSD']


def merge(extract=True):
    filename = 'Conferme_CandidatiAmmessi_def.xlsx'

    ammessi_df = pd.DataFrame()
    corsi = get_corsi()
    candidati_df = get_candidati()

    for s in corsi:
        t_df = pd.read_excel(filename, sheet_name=s, skiprows=1)
        t_df = t_df[t_df['Iscrizione corso'] == 'si']
        t_df = t_df[['Cognome', 'Nome', 'Matricola', 'Mail']]
        t_df['Corso'] = s

        ammessi_df = pd.concat([ammessi_df, t_df], ignore_index=True)

    ammessi_anag_df = ammessi_df.merge(candidati_df, left_on='Matricola', right_on='numeroMatricola', how='left')
    # ammessi_anag_df['dataNascita'] = pd.to_datetime(ammessi_anag_df['dataNascita'])
    ammessi_anag_df = ammessi_anag_df.drop(columns=['numeroMatricola', 'statoCandidatura', 'Cognome', 'Nome', 'Mail'])

    if extract:
        ammessi_anag_df.to_excel("Ammessi.xlsx", index=False)
    return ammessi_anag_df
