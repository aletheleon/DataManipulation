import pymysql
from pprint import pprint


def create_cursor(host_name, user_name, pw, db_name):
    try:
        connection = pymysql.connect(host = host_name, user = user_name, password = pw, db = db_name, charset = "utf8mb4", cursorclass = pymysql.cursors.Cursor)
        cursor = connection.cursor()
        return cursor
    except Exception as e:
        print(e)
        print(f"Couldn't log in to MySQL server using this password: {pw}.\n")

def query0(cursor):
    '''Sample'''
    query = 'SELECT * FROM own_titles;'
    '''DO NOT CHANGE THE CODE BELOW'''
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def query1(cursor):
    '''Fill in the query'''
    query = 'select year, avg(avg_annual_pay) from combined_annuals where year = 2016 or year = 2017 group by year order by year;'
    '''DO NOT CHANGE THE CODE BELOW'''
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def query2(cursor, year, lower_avg_annual_pay, upper_avg_annual_pay):
    '''Fill in the query'''
    query = f'select industry_title from combined_annuals join industry_titles using (industry_code) where avg_annual_pay >= {lower_avg_annual_pay} and avg_annual_pay <= {upper_avg_annual_pay} and year = {year} order by -avg_annual_pay;'
    '''DO NOT CHANGE THE CODE BELOW'''
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def query3(cursor, keyword):
    '''Fill in the query'''
    query = f'select distinct industry_title from industry_titles where industry_title like "%{keyword}%" order by industry_title;'
    '''DO NOT CHANGE THE CODE BELOW'''
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def query4(cursor, year, quarter):
    '''Fill in the query'''
    query = f'select own_title, avg(avg_wkly_wage) from combined_quarters join own_titles using (own_code) where year = {year} and qtr = {quarter} group by own_title order by -avg(avg_wkly_wage);'
    '''DO NOT CHANGE THE CODE BELOW'''
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def query5(cursor, year, quarter):
    '''Fill in the query'''
    query = f'select industry_title, (month1_emplvl + month2_emplvl + month3_emplvl) as total_emplvl from combined_quarters join industry_titles using (industry_code) where industry_code != 10 and year = {year} and qtr = {quarter} order by -total_emplvl limit 1;'
    '''DO NOT CHANGE THE CODE BELOW'''
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def query6(cursor, year, quarter, avg_wkly_wage_lb):
    '''Fill in the query'''
    query = f'select agglvl_title, min(avg_wkly_wage) from agglvl_titles join combined_quarters using (agglvl_code) where year = {year} and qtr = {quarter} group by agglvl_title having min(avg_wkly_wage) > {avg_wkly_wage_lb};'
    '''DO NOT CHANGE THE CODE BELOW'''
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def query7(cursor):
    '''Fill in the query'''
    query = 'select own_title, agglvl_title from own_titles, agglvl_titles where own_title = "Federal Government" limit 10;'
    '''DO NOT CHANGE THE CODE BELOW'''
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def query8(cursor):
    '''Fill in the query'''
    query = 'select own_code, own_title, length(own_title) as title_length from own_titles order by title_length;'
    '''DO NOT CHANGE THE CODE BELOW'''
    cursor.execute(query)
    result = cursor.fetchall()
    return result

'''BONUS'''
"""
Question: Write a query that finds the average employment level for each level of government for a set yearly interval.

This query can help find the trend in employment for every level of government as a function of time.

Test Case: query9(cursor, 2016, 2017)

(('Total Covered', 2016, Decimal('141870066.0000')),
 ('Federal Government', 2016, Decimal('36038.5903')),
 ('State Government', 2016, Decimal('54915.2519')),
 ('Local Government', 2016, Decimal('98914.6537')),
 ('Private', 2016, Decimal('444656.6873')),
 ('Total Government', 2016, Decimal('21365445.0000')),
 ('Total U.I. Covered (Excludes Federal Government)',
  2016,
  Decimal('139077079.0000')),
 ('Total Covered', 2017, Decimal('143859855.0000')),
 ('Federal Government', 2017, Decimal('36936.8534')),
 ('State Government', 2017, Decimal('56234.1210')),
 ('Local Government', 2017, Decimal('99111.8619')),
 ('Private', 2017, Decimal('454335.3063')),
 ('Total Government', 2017, Decimal('21473291.0000')),
 ('Total U.I. Covered (Excludes Federal Government)',
  2017,
  Decimal('141057273.0000')))

+--------------------------------------------------+------+------------------------+
| own_title                                        | year | avg(annual_avg_emplvl) |
+--------------------------------------------------+------+------------------------+
| Total Covered                                    | 2016 |         141870066.0000 |
| Federal Government                               | 2016 |             36038.5903 |
| State Government                                 | 2016 |             54915.2519 |
| Local Government                                 | 2016 |             98914.6537 |
| Private                                          | 2016 |            444656.6873 |
| Total Government                                 | 2016 |          21365445.0000 |
| Total U.I. Covered (Excludes Federal Government) | 2016 |         139077079.0000 |
| Total Covered                                    | 2017 |         143859855.0000 |
| Federal Government                               | 2017 |             36936.8534 |
| State Government                                 | 2017 |             56234.1210 |
| Local Government                                 | 2017 |             99111.8619 |
| Private                                          | 2017 |            454335.3063 |
| Total Government                                 | 2017 |          21473291.0000 |
| Total U.I. Covered (Excludes Federal Government) | 2017 |         141057273.0000 |
+--------------------------------------------------+------+------------------------+
14 rows in set (0.02 sec)
"""
def query9(cursor, year_lb, year_ub): #Add any addditional parameters
    '''Fill in the query'''
    query = f'select own_title, year, avg(annual_avg_emplvl) from combined_annuals join own_titles using (own_code) where year >= {year_lb} and year <= {year_ub} group by own_title, year;'
    '''DO NOT CHANGE THE CODE BELOW'''
    cursor.execute(query)
    result = cursor.fetchall()
    return result


"""
Question: Write a query that finds the year, quarter, and average weekly wages of the quarter with the three highest
quarterly wages of the specified industry and government level.

This query can be used to find quarters that had excessive spending on employee wage specific to industry and government
level. Relating the year and quarter back to events happening in the world or within the country could give good insight
into how to better adjust wages if presented with a similar situation again.

Test Case: query10(cursor, "Private", "Service-providing")

((2017, 4, 1076, 1433290000000),
 (2017, 1, 1090, 1407670000000),
 (2016, 4, 1033, 1354750000000))

+------+------+---------------+-------------------+
| year | qtr  | avg_wkly_wage | total_qtrly_wages |
+------+------+---------------+-------------------+
| 2017 |    4 |          1076 |     1433290000000 |
| 2017 |    1 |          1090 |     1407670000000 |
| 2016 |    4 |          1033 |     1354750000000 |
+------+------+---------------+-------------------+
3 rows in set (0.05 sec)
"""
def query10(cursor, own_title, industry_title): #Add any addditional parameters
    '''Fill in the query'''
    query = f'select year, qtr, avg_wkly_wage, total_qtrly_wages from combined_quarters join own_titles using (own_code) join industry_titles using (industry_code) where own_title = "{own_title}" and industry_title = "{industry_title}" group by year, qtr order by -total_qtrly_wages limit 3;'
    '''DO NOT CHANGE THE CODE BELOW'''
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def main():
    #create a cursor object. Fill in the pw parameter if you have a password to MySQL server
    cursor = create_cursor('localhost', 'root', 'password@', 'blsQcew')

    #query0() - cursor.fetchall() output
    pprint(query0(cursor))

    #query1() - cursor.fetchall() output
    pprint(query1(cursor))

    #query2() - cursor.fetchall() output
    pprint(query2(cursor, 2016, 10000, 15000))

    #query3() - cursor.fetchall() output
    pprint(query3(cursor, 'engineering'))

    #query4() - cursor.fetchall() output
    pprint(query4(cursor, 2017, 2))

    #query5() - cursor.fetchall() output
    pprint(query5(cursor, 2017, 1))

    #query6() - cursor.fetchall() output
    pprint(query6(cursor, 2017, 1, 1000))

    #query7() - cursor.fetchall() output
    pprint(query7(cursor))

    #query8() - cursor.fetchall() output
    pprint(query8(cursor))

    #query8() - cursor.fetchall() output
    pprint(query9(cursor, 2016, 2017))

    #query8() - cursor.fetchall() output
    pprint(query10(cursor, "Private", "Service-providing"))

if __name__ == '__main__':
    main()
