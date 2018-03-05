from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from pandas import Series, DataFrame
import re, copy

def optionFiltering(option):
    return option.text != '전체'

def makeDatabase(categories, foreignTableName, foreignKey, indexing):
    if not categories:
        return
    else:
        categories = copy.deepcopy(categories)
        category = categories.pop(0)
        select = Select(browser.find_element_by_id(category['selector']))
        data = list()
        primaryKey = list()
        test = list()

        filteredOption = filter(optionFiltering, select.options)
        for id, option in enumerate(filteredOption, 1):
                data.append(option.text)
                primaryKey.append(id)

                select.select_by_visible_text(option.text)
                test = makeDatabase(tables, category['name'], id)

        if not foreignTableName:
            tableData = { category['name'] + '_code': primaryKey, category['name'] + '_name': data }
        elif not foreignKey:
            tableData = { category['name'] + '_code': primaryKey, category['name'] + '_name': data, foreignTableName + '_code' : ''}
        else:
            tableData = { category['name'] + '_code': primaryKey, category['name'] + '_name': data, foreignTableName + '_code': foreignKey}

        return tableData

def getForeignTable(name, id):
    return dict(name=name,id=id)

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

def makeDatabase(categories, foreignTable, index):
    if not categories:
        return
    categories = copy.deepcopy(categories)
    category = categories.pop(0)

    data = list()
    primaryKey = list()
    resultDatabase = list()

    select = Select(browser.find_element_by_id(category['selector']))
    filteredOption = filter(optionFiltering, select.options)
    for id, option in enumerate(filteredOption, index):
        data.append(option.text)
        primaryKey.append(id)
        foreignTable = getForeignTable(category['name'], id)

        select.select_by_visible_text(option.text)
        addTableList()
        resultDatabase += makeDatabase(categories, foreignTable)

    if not foreignTable['name']:
        tableData = {category['name'] + '_code': primaryKey, category['name'] + '_name': data}
    elif not foreignTable['id']:
        tableData = {category['name'] + '_code': primaryKey, category['name'] + '_name': data,
                     foreignTable['name'] + '_code': ''}
    else:
        tableData = {category['name'] + '_code': primaryKey, category['name'] + '_name': data,
                     foreignTable['name'] + '_code': foreignTable['id']}

    resultDatabase.append(tableData)
    return resultDatabase

# Chrome 브라우저를 통해 연세 수강편람 페이지를 방문
# (수강편람 페이지가 JS로 로드되어 페이지가 변하기 때문에 requests 모듈 대신 selenium 모듈을 사용)
browser = webdriver.Firefox()
browser.get('http://ysweb.yonsei.ac.kr:8888/curri120601/curri_new.jsp#top')

# categoryID = ['OCODE0']
# categoryID = {'university' : 'OCODE0', 'college' : 'OCODE1', 'department' : 'S2'}
categories = [{'name':'college','selector':'OCODE1'},{'name':'department','selector':'S2'}]

myDB = makeDatabase(categories, foreignTable=None, index=1)
print(myDB)