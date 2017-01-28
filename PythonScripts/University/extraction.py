#  Class for extracting data formDatabase.
import pymysql
import math

con = pymysql.connect(host='localhost', port=3306, user='candidwebuser', passwd='pw4candid', db='fittsdb')
curr = con.cursor()


