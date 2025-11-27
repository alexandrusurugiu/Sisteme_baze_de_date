import oracledb
import pandas as pd
import oracledb

# Pandas:
# - are drept scop analiza si manipularea datelor, facilitand interactiunea cu baza de date prin incarcarea rezultatelor
# direct in DataFrame-uri
# - pentru a putea utiliza pachetul in cadrul lucrului cu baza de date, putem folosit instructiunea PANDAS.READ_DQL
# - pachetul gestioneaza automat procesul de preluare a datelor, eliminand necesitatea folosirii cursorului
# - se utilizeaza in general pentru operatiuni ce tin de analiza, calcule statistice, rapoarte si procesari rapide ale
# seturilor de date in memorie

# SQL Alchemy
# - este o biblioteca folosita pentru accesul la baze de date relationale ce implementeaza modelul ORM
# - mapeaza tabelele bazei de date pe clase Python, permitand manipularea inregistrarilor sub forma de obiecte
# - este o biblioteca independenta de SGBD, oferind flexibilitate si posibilitatea de a lucra cu diverse baze de date, nu
# doar cele Orace
# - se bazeaza pe crearea unei sesiuni, definirea claselor model si gestionarea tranzactiilor prin metode specifice

# Diferente intre cele 2:
# - Pandas lucreaza cu rezultatul interogarilor SQL, in timp ce SQL Alchemy permite definirea si controlul structurii bazei
# de date direct din codul Python
# - SQL Alchemy ofera atat capacitati ORM, cat si de executie SQL, fiind un insturment complet pentru dezvoltare BE (back-end)
# spre deosebire de Pandas care este un insturment de analiza

connection = oracledb.connect(user="MS_DBA1", password="oracle", dsn="193.226.34.57:1521/orclpdb.docker.internal")


#Exercitiul 4
# lista_clienti_noi = [
#     (100, "Popa Marcel", "Inginer", "m", 34, "C", 230),
#     (101, "Popa Vasilica", "Coafeza", "f", 32, "C", 200),
#     (102, "Popa Ion", "Instalator", "m", 64, "C", 120)
# ]
#
# cursor = connection.cursor()
# cursor.bindarraysize = 3
# cursor.setinputsizes(int, 150, 150, 3, int, 1, float)
# sql_insert = "insert into clienti_noi(id_client, nume_client, profesia, sex, varsta, stare_civila, suma_solicitata) values (:1, :2, :3, :4, :5, :6, :7)"
# cursor.executemany(sql_insert, lista_clienti_noi)
# connection.commit()
#
# sql_select = "select * from clienti_noi"
# cursor.execute(sql_select)
# for row in cursor:
#     print(row)
#
# cursor.close()
# connection.close()




#Exercitiul 5
# cursor = connection.cursor()
#
# v_nume = input("Introduceti numele clientilor pentru majorare: ")
# sql_update = "update clienti_noi set suma_solicitata=suma_solicitata*1.10 where lower(nume_client) like :p_nume"
# cursor.execute(sql_update, p_nume='%' + v_nume.lower() + '%')
# connection.commit()
#
# print(f"Actualizare realizata pentru clientii cu numele {v_nume.upper()}.")
#
# cursor.execute("SELECT nume_client, suma_solicitata from clienti_noi where lower(nume_client) like :p_nume", p_nume='%' + v_nume.lower() + '%')
# for row in cursor:
#     print(f"Nume client: {row[0]}, suma solicitata: {row[1]}")
# cursor.close()
# connection.close()




#Exercitiul 9
# cursor = connection.cursor()
# sql_select = "SELECT id_client, nume_client FROM t_clienti_leasing"
# cursor.execute(sql_select)
# for row in cursor:
#     print(row)

# sql_select = "SELECT id_client, nume_client FROM t_clienti_leasing WHERE nume_client = 'Hodorogea Prisacaru Neculai'"
# cursor.execute(sql_select)
# result = cursor.fetchone()
#
# if result:
#     v_id = result[0]
#     v_nume = result[1]
#     scor = cursor.callfunc("f_calcul_prescoring", int, [v_id])
#     print(f"Clientul cu ID {v_id} si NUME {v_nume} are prescoringul: {scor}")
# else:
#     print("Clientul nu exista.")
#
# cursor.close()
# connection.close()




#Exercitiul 11
# prag = 2010
# sql_Select = "SELECT marca, model, an_fabricatie, componenta, pret_manopera, valoare_dauna FROM t_clienti_daune WHERE an_fabricatie > :an"
#
# df = pd.read_sql(sql_Select, con=connection, params={'an': prag})
# print("DataFrame Autoturisme noi:")
# print(df)
#
# connection.close()




#Exercitiul 12
# sql_select = "SELECT marca, model, an_fabricatie, componenta, pret_manopera, valoare_dauna FROM t_clienti_daune"
# df = pd.read_sql(sql_select, con=connection)
# df["PROCENT_MANOPERA"] = (df["VALOARE_DAUNA"] / df["PRET_MANOPERA"]) * 100
# df_filtrat = df.loc[df["PROCENT_MANOPERA"] > 30, ["MARCA", "COMPONENTA", "PROCENT_MANOPERA"]]
#
# print("Componente cu manopera scumpa:")
# print(df_filtrat)
#
# connection.close()




#Exercitiul 14
# sql_select = "SELECT nume_client, varsta, profesia, venit_anual_ron, suma_solicitata FROM t_clienti_leasing"
# df = pd.read_sql(sql_select, con=connection)
#
# criterii = (
#     (df['VARSTA'] < 40) &
#     (df['VENIT_ANUAL_RON'] > 10000) &
#     (df['PROFESIA'].isin(['Inginer', 'Profesor']))
# )
#
# rezultat = df.loc[criterii, ['NUME_CLIENT', 'SUMA_SOLICITATA', 'PROFESIA']]
# print("Clienti Tineri, Bogati, Ingineri/Profesori:")
# print(rezultat)
#
# connection.close()