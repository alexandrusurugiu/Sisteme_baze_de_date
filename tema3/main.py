import pymongo
import pandas as pd
import matplotlib.pyplot as plt

conn = pymongo.MongoClient("mongodb://master:stud1234@193.226.34.57:27017/?authSource=daune_leasing&authMechanism=SCRAM-SHA-256")
db = conn["daune_leasing"]
collection = db["clienti_leasing"]
collection2 = db["clienti_daune"]


#Exercitiul 1
query = {
    "VARSTA": {"$gt": 35},
    "SUMA_SOLICITATA": {"$gt": 15000}
}
projection = {
    "_id": 0,
    "NUME_CLIENT": 1,
    "SUMA_SOLICITATA": 1,
    "SUMA_DEPOZIT": 1,
    "FIDELITATE": 1
}

cursor = collection.find(query, projection=projection)
df = pd.DataFrame(list(cursor))
cursor.close()

condition = df['SUMA_DEPOZIT'] > df['SUMA_SOLICITATA']
df.loc[condition, 'FIDELITATE'] = 5

print(df)
df.to_csv('clienti_leasing.csv', index=False)




#Excercitiul 2
pipeline = [
    {
        "$group": {
            "_id": "$PROFESIA",
            "TOTAL_VENIT": {"$sum": "$VENIT_ANUAL"},
            "TOTAL_DEPOZIT": {"$sum": "$SUMA_DEPOZIT"},
            "TOTAL_SOLICITAT": {"$sum": "$SUMA_SOLICITATA"}
        }
    }
]

cursor = collection.aggregate(pipeline)
df = pd.DataFrame(list(cursor))
cursor.close()

df['GRAD_INDATORARE'] = (df['TOTAL_SOLICITAT'] / (df['TOTAL_VENIT'] + df['TOTAL_DEPOZIT'])) * 100
df = df.sort_values(by='GRAD_INDATORARE', ascending=False)

df.plot('_id', 'GRAD_INDATORARE', figsize = (12, 8), kind = 'bar')
plt.ylabel('Gradul de indatorare (%)')
plt.title('Gradul de indatorare pe profesii')
plt.show()




#Exercitiul 3
pipeline = [
    {
        "$match": {
            "AN_FABRICATIE": {"$gte": 2010, "$lte": 2012}
        }
    },
    {
        "$group": {
            "_id": {"MARCA": "$MARCA", "MODEL": "$MODEL"},
            "VALOARE_TOTALA": {"$sum": "$VALOARE_DAUNA"},
            "NUMAR_DAUNE": {"$sum": 1}
        }
    }
]
cursor = collection2.aggregate(pipeline)
df = pd.DataFrame(list(cursor))

nr = df[df['VALOARE_TOTALA'] > 30000].shape[0]
print('Numarul modelelor cu valoarea totala mai mare de 30000 este: ', nr)
df_plot = df[df['NUMAR_DAUNE'] > 100]
df_plot.plot.bar('_id', 'NUMAR_DAUNE', figsize = (12, 8))
plt.title('Modele cu peste 100 de daune')
plt.show()




#Excericitul 4
query = {
    "MARCA": {"$in": ["AUDI", "BMW", "FORD", "FIAT"]}
}

projection = {
    "_id": 0,
    "MARCA": 1,
    "MODEL": 1,
    "AN_FABRICATIE": 1,
    "COMPONENTA": 1,
    "VALOARE_DAUNA": 1,
    "PRET_MANOPERA": 1
}

cursor = collection2.find(query, projection=projection)
df = pd.DataFrame(list(cursor))
cursor.close()

df = df[df['VALOARE_DAUNA'] > 0].copy()
df['PROCENT_MANOPERA'] = (df['PRET_MANOPERA'] / df['VALOARE_DAUNA']) * 100
df_final = df[['MARCA', 'MODEL', 'VALOARE_DAUNA', 'PRET_MANOPERA', 'PROCENT_MANOPERA']]
print(df_final)
df_final.to_csv('daune_masini.csv', index=False)


conn.close()