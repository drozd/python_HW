
import pymysql, csv
cnx = pymysql.connect(host ='localhost', user='guest1', passwd='n76Je4=wx6H')

with open('metatable.csv', encoding='utf-8') as vk_table:
    reader = csv.reader(vk_table, delimiter='\t')
    cursor = cnx.cursor()
    database = """create database guest1_olgadrozd"""
    cursor.execute(database)
    change_db = """use guest1_olgadrozd"""
    cursor.execute(change_db)
    table = """create table vk_data (
               Name varchar(30),
               Sex char(1),
               Id varchar(15),
               Birth_date varchar(10),
               Relation char(1),
               Languages varchar(100))"""
    cursor.execute(table)
    insert_query = ("insert into vk_data (Name, Sex, Id, Birth_date, Relation, Languages) "
                   "VALUES (%s, %s, %s, %s, %s, %s)")
    for row in reader:
        data = tuple(row)
        cursor.execute(insert_query, data)
        cnx.commit()
    cnx.close()
