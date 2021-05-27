import pandas as pd
from os import listdir
from os.path import isfile, join
import pymysql
import shutil

print("Insertion BDD auto")

#mapping "à la main " id_j/nom_j
id_dic = {'Charlie Hebdo':9, 'Closer':7, 'Figaro':4, 'Gorafi':5, 'Le Point':3,
       'Le Monde':1, 'Libération':2, 'Nord Presse':6, 'Public':8, 'Science et Avenir':10}

id_dic_inv =  {v: k for k, v in id_dic.items()}


#récupération noms csv
path = 'titres_journaliers_to_bdd'
liste_csv = [f for f in listdir(path) if isfile(join(path, f))]

#pour récupération des erreurs
dfe =pd.DataFrame()
#loop
for file in liste_csv:
    #lecture
    df = pd.read_csv('titres_journaliers_to_bdd/'+file)

    #s'assurer type(titre) == str
    df.titre = df.titre.astype(str)

    #transformer nom du journal (id journal)
    df.replace({"journal": id_dic}, inplace=True)

    #changer l'ordre des colonnes
    df = df[['date','journal','titre']]

    #insertion dans la BDD
    connection = pymysql.connect(host='localhost', user='JmAuDiCc', password='mdp', db='journaux_db')
    cursor=connection.cursor(pymysql.cursors.DictCursor)
    l_e = []
    for row in df.values.tolist():
        try:    
            cursor.execute("insert into articles (Date_art,Id_journal,Titre) values(%s,%s,%s)", row)
        except Exception as e:
            print(e)
            print(row)
            l_e.append(row)
    connection.commit()   
    connection.close()
    

    #retransforme nom journal (pour lisibilité dans les csv)
    df.replace({"journal": id_dic_inv}, inplace=True)

    #on bouge le csv
    shutil.move("titres_journaliers_to_bdd/"+file, "../supervision_model/titres_journaliers_supervision/"+file)
    
    #sauvegarde des insertions en erreur
    if l_e:
        for row in l_e:
            r = pd.Series(row, index = df.columns)
            dfe = dfe.append(r, ignore_index=True)
        dfe.to_csv('err_insert_bdd/err.csv', encoding = 'utf-8',mode='a',header=False)