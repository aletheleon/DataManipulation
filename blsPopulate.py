import pymysql
import sys
import csv
import re

user_password = sys.argv[1]

connection = pymysql.connect(host = "localhost", user = "root", password = user_password,db = "blsQcew",charset = "utf8mb4",cursorclass = pymysql.cursors.Cursor)
cursor = connection.cursor()

c1, c2, c3, c4, c5 = True, True, True, True, True
#Populate table combined_quarters
try:
    infile = open("combined_quarters.txt","r")
    reader = csv.reader(infile)
    next(reader)
    for row in reader:
        quarters_id = int(row[0])
        own_code = str(row[2])
        industry_code = str(row[3])
        agglvl_code = str(row[4])
        year = int(row[6])
        qtr = int(row[7])
        disclosure_code = str(row[8])
        qtrly_estabs = int(row[9])
        month1_emplvl = int(row[10])
        month2_emplvl = int(row[11])
        month3_emplvl = int(row[12])
        total_qtrly_wage = int(float(row[13]))
        avg_wkly_wage = int(row[16])
        cursor.execute("INSERT INTO combined_quarters (id, own_code,industry_code,agglvl_code,year,qtr,disclosure_code,qtrly_estabs,month1_emplvl,month2_emplvl,month3_emplvl,total_qtrly_wages,avg_wkly_wage) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(quarters_id, own_code,industry_code,agglvl_code,year,qtr,disclosure_code,qtrly_estabs,month1_emplvl,month2_emplvl,month3_emplvl,total_qtrly_wage,avg_wkly_wage))
except Exception as e:
    print("\n", e)
    print("Did you download combined_quarters.txt and place it in the current directory?\nPlease rerun blsSchema.sql before running blsPopulate.py again.\n")
    c1 = False

#Populate table combined_annuals
try:
    infile = open("combined_annuals.txt","r")
    reader = csv.reader(infile)
    next(reader)
    for row in reader:
        annuals_id = int(row[0])
        own_code = str(row[2])
        industry_code = str(row[3])
        agglvl_code = str(row[4])
        year = int(row[6])
        disclosure_code = str(row[8])
        annual_avg_estabs = int(row[9])
        annual_avg_emplvl = int(row[10])
        annual_avg_wkly_wage = int(row[14])
        avg_annual_pay = int(row[15])
        cursor.execute("INSERT INTO combined_annuals (id, own_code,industry_code,agglvl_code,year,disclosure_code,annual_avg_estabs,annual_avg_emplvl,annual_avg_wkly_wage,avg_annual_pay) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(annuals_id, own_code,industry_code,agglvl_code,year,disclosure_code,annual_avg_estabs,annual_avg_emplvl,annual_avg_wkly_wage,avg_annual_pay))
except Exception as e:
    print("\n", e)
    print("Did you download combined_annuals.txt and place it in the current directory?\nPlease rerun blsSchema.sql before running blsPopulate.py again.\n")
    c2 = False

#Populate table ownership_titles
try:
    infile = open("ownership_titles.txt","r")
    reader = csv.reader(infile)
    next(reader)
    for row in reader:
        own_code_num = str(row[0])
        own_title_str = str(row[1])
        cursor.execute("INSERT INTO own_titles (own_code,own_title) VALUES (%s,%s)",(own_code_num,own_title_str))
except Exception as e:
    print("\n", e)
    print("Did you download ownership_titles.txt and place it in the current directory?\nPlease rerun blsSchema.sql before running blsPopulate.py again.\n")
    c3 = False

#Populate table industry_titles
try:
    infile = open("industry_titles.txt","r")
    reader = csv.reader(infile)
    next(reader)
    for row in reader:
        industry_code = str(row[0])
        industry_title = str(row[1])
        industry_title_cleaned = industry_title[re.search('(NAICS )?\d{0,}',industry_title).end()+1:]
        cursor.execute("INSERT INTO industry_titles (industry_code,industry_title) VALUES (%s,%s)",(industry_code,industry_title_cleaned))
except Exception as e:
    print("\n", e)
    print("Did you download industry_titles.txt and place it in the current directory?\nPlease rerun blsSchema.sql before running blsPopulate.py again.\n")
    c4 = False

#Populate table agglevel_titles
try:
    infile = open("agglevel_titles.txt","r")
    reader = csv.reader(infile)
    next(reader)
    for row in reader:
        agglvl_code = str(row[0])
        agglevel_title = str(row[1])
        cursor.execute("INSERT INTO agglvl_titles (agglvl_code,agglvl_title) VALUES (%s, %s)", (agglvl_code,agglevel_title))
except Exception as e:
    print("\n", e)
    print("Did you download agglevel_titles.txt and place it in the current directory?\nPlease rerun blsSchema.sql before running blsPopulate.py again.\n")
    c5 = False

connection.commit()
connection.close()

if c1 and c2 and c3 and c4 and c5:
    print("\n##########################################################\n#\n#             Data Inserted Successfully.\n#\n##########################################################\n\n")


