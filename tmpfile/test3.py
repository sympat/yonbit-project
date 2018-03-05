from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
from pandas import Series, DataFrame


def isSameTable(aTable, bTable):
    if len(aTable) != len(bTable):
        return False
    else:
        for aKey, aValue in aTable.items():
            for bKey, bValue in bTable.items():

def mergeTable(aTable, bTable):
    resultTable = dict()

    for aKey, aValue in aTable.items():
        for bKey, bValue in bTable.items():
            if aKey == bKey:
                resultTable[aKey] = aValue+bValue
                continue

    return resultTable

def addDatabase(aDatabase, bDatabase):
    resultDatabase = list()

    for a, b in zip(aDatabase, bDatabase):
        resultDatabase.append(mergeTable(a, b))

    return resultDatabase

c = { 'college_code' : [6,7], 'college_name': ['c', 'd']}
d = { 'college_code' : [1,2], 'college_name': ['e', 'f']}
a = [{ 'college_code' : [6,7], 'college_name': ['c', 'd']} , { 'dept_code' : [8,9], 'dept_name': ['a', 'b']}]
b = [{ 'college_code' : [1,2,3], 'college_name': ['e', 'f', 'g']} , { 'dept_code' : [3,4], 'dept_name': ['가', '나']}]
g = []

print(len(g))