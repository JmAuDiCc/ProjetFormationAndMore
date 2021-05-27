import numpy as np
import pandas as pd
import pickle
from os import listdir
from os.path import isfile, join
from sklearn.metrics import confusion_matrix , accuracy_score ,  f1_score , precision_score, recall_score
import shutil

print('Supervision des modèles de classification')

#import des vecteurs de mots fastText 
import fasttext
ft = fasttext.load_model('../nlp/fasttext/cc.fr.300.bin')

#fonction permetant la transformation de titres en vecteur ( moy des vecteur de mot fastText)
def to_vec_ft_mean(phrase):
    v=[]
    for token in str(phrase).split():
        v.append(ft.get_word_vector(str(token)))
    return (np.mean(np.array(v),axis=0))

#fonction permetant de calculer les différentes métriques de supervision classqiue de model de classification
def return_metrics(y,yp,liste_classes):
    data = {}
    for classe in liste_classes:
        data[classe+'_precision'] = precision_score(y,yp,average=None,labels=[classe],zero_division=0)
        data[classe+'_recall'] = recall_score(y,yp,average=None,labels=[classe],zero_division=0)
        data[classe+'_f1-score'] = f1_score(y,yp,average=None,labels=[classe],zero_division=0)
        if classe in y.unique():
            data[classe+'_nb'] = y.value_counts()[classe]
        else:
            data[classe+'_nb'] = 0
    data['Avg_weighted_precision'] = precision_score(y,yp,average='weighted',zero_division=0)
    data['Avg_weighted_recall'] = recall_score(y,yp,average='weighted',zero_division=0)
    data['Avg_weighted_f1-score'] = f1_score(y,yp,average='weighted',zero_division=0)
    data['Avg_macro_precision'] = precision_score(y,yp,average='macro',zero_division=0)
    data['Avg_macro_recall'] = recall_score(y,yp,average='macro',zero_division=0)
    data['Avg_macro_f1-score'] = f1_score(y,yp,average='macro',zero_division=0)
    data['Accuracy'] = accuracy_score(y,yp)
    return pd.DataFrame.from_dict(data)

#dictionnaire des types en fonction des nom de journaux
dic_type = {'actu':['Figaro','Le Point','Le Monde','Libération'],
      'people':['Closer','Public'],
      'science':['Science et Avenir'],
      'parodique':['Nord Presse','Gorafi'],
      'satirique':['Charlie Hebdo']}

#pour mapping nom des journaux / type 
def get_key(val):
    for key, value in dic_type.items():
         if val in value:
                return key 

#récupération du nom des models
path = '../nlp/models'
liste_model = [f for f in listdir(path) if isfile(join(path, f))]

#récupération des csv de titres
#path = 'titres_journaliers_supervision'
path = 'titres_journaliers_supervision'
liste_csv = [f for f in listdir(path) if isfile(join(path, f))]

#print('ft chargé!')
#pour chaque model à superviser
for nom_model in liste_model:
    
    #récupéation du model ( sklearn)
    model = pickle.load(open('../nlp/models/'+nom_model,'rb'))
    
    print('Supervision pour le model:'+nom_model)
    #création d'un dataFrame pour stockage des métriques dans un csv 
    df_total_sup = pd.DataFrame()
    
    #pour chaque csv
    for filename in liste_csv:
        
        #récupération des titres dans un dataframe
        path = "titres_journaliers_supervision/"+filename
        df = pd.read_csv(path) 
        
        #récupération du type de journal de chaque titre
        l_type = []
        for j in df['journal']:
            l_type.append(get_key(j))
        df['type'] = l_type
        
        #transformation des titres en vecteur
        vectors = []
        for titre in enumerate (df["titre"]):
            vectors.append(to_vec_ft_mean(titre) )           
        df['vector']=vectors
        
        #predictions du model
        y_pred = model.predict(np.array(np.stack(df["vector"])))
        
        #calcul des métriques et insertions dans une row de dataframe pandas
        df_sup = return_metrics(df['type'],y_pred,model.classes_)
        
        #ajout de la date et du nombre total de titres sur le jour donné
        df_sup['date'] = df['date'].unique()[0]
        df_sup['total_titres'] = len(df)
        
        #insertion de la row dans un dataframe pour écriture (a)
        df_total_sup = df_total_sup.append(df_sup, ignore_index = True)
        
        
    name_path_file = str('resultats_supervision/'+nom_model[:-4]+'_supervision.csv')  
    if not isfile(name_path_file):
        df_total_sup.to_csv(index=False ,path_or_buf=name_path_file,mode='a',encoding = 'utf-8')
    else: 
        df_total_sup.to_csv(index=False ,path_or_buf=name_path_file,mode='a',encoding = 'utf-8',header=False)

        
for filename in liste_csv:
    shutil.move("titres_journaliers_supervision/"+filename, "titres_journaliers_maj_model/"+filename)



