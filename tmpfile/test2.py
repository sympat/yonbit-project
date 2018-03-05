# 검색하고 그에 맞는 수강편람 표 내용이 채워진 이후에 총 레코드의 개수와 페이지당 레코드 수가 제대로 표시가 되므로
# 수강편람 표 내용이 채워졌는지를 몇 초 기다리면서 확인해야만 한다. (WebDriver 에게 #row0jqxgrid > div가 생길 때 까지 명시적으로 delayTime 만큼 기다리라고 알린다)
# 채워진 기준을 다시 한번 생각해봐도 괜찮을듯
delayTime = 5
WebDriverWait(browser, delayTime).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#row0jqxgrid > div")))

# 검색된 총 레코드의 개수와 페이지당 레코드 수를 담은 텍스트를 찾는다
# 이 두 수를 찾는 이유는 수강편람 페이지 설계가 개같아서 '원하는' 수강편람 리스트를 가져올 때 필요하다.
# 뽑혀나온 텍스트에서 총 레코드의 개수와 페이지당 레코드 수를 찾아 변수로 저장해놓는다
# 그 외 크롤링을 위한 변수도 저장해놓는다
# limitRecord는 페이지당 레코드 수, totalRecord는 총 레코드의 개수
pageText = browser.find_element_by_xpath('//*[@id="pager"]/div/div/div[3]').text
limitRecord = int(pageText.split()[0][2:])
totalRecord = int(pageText.split()[2])
lastPage = (totalRecord // limitRecord) + 1
lastRow = (totalRecord % limitRecord) - 1

print('페이지당 레코드 수는', limitRecord)
print('총 레코드 수는', totalRecord)
print('마지막 페이지는', lastPage)
print('마지막 행은', lastRow)

countPage = 1
countRow = 0

# 첫 시도는 다음과 같았다. 하지만 문제점이 생겼는데, 데이터가 아예 없는 cell에 대한 처리가 불가능하다.
# for row in rows:
#    output = list()
#    dummy = row.stripped_strings
#    for data in dummy:
#        output.append(data)
#    print(output)
# 수강편람 데이터 테이블의 첫 페이지 부터 마지막 페이지 까지 반복한다.
while(countPage <= lastPage):
    # BeautifulSoup 객체를 만든다.
    html = BeautifulSoup(browser.page_source, 'html.parser')
    print(countPage, '페이지')

    # 일반적인 페이지이면 첫행부터 limitRecord 수 만큼 행을 가져온다.
    # 그러나 마지막 페이지는 첫행부터 마지막 행까지(포함) 가져온다. 왜냐하면 마지막 페이지에서도 limitRecord 만큼의 행이 빈칸으로 존재하기 때문에 불필요한 행을 조사하는 경우가 있다.
    if(countPage == lastPage):
        rows = html.find_all(id=re.compile('^(row)[0-9]+jqxgrid$'), limit=lastRow+1)
    else:
        rows = html.find_all(id=re.compile('^(row)[0-9]+jqxgrid$'))
        nextPage = browser.find_element_by_xpath('//*[@id="pager"]/div/div/div[2]')
        nextPage.click()

    # 현재 페이지의 첫행부터 가져온 행까지 반복한다.
    for row in rows:
        # 각 행에 대해 출력 리스트를 만든다.
        output = list()

        # 현재 행의 첫 데이터 셀부터 마지막 데이터 셀까지 반복한다.
        # 이 때 데이터에 해당되는 적절한 셀을 뽑기 위해 조건을 설정한다.
        for cell in row.find_all(is_gridcell_and_visible):
            # 데이터 셀 중에서 값이 아예 없는 (텍스트가 존재하지 않는) 셀의 경우, 인위적으로 공백 문자를 삽입하여 셀의 갯수를 유지한다.
            # 또한, html에서 &nbsp; 는 유니코드상으로 \xa0 라는 값으로 인코딩 되는듯하다. &nbsp;는 우리게에 불필요한 공백이므로 이를 제거하고 그 다음 출력 리스트에 저장한다.
            if(cell.text == None):
                cell.text = " "
            output.append(cell.text.replace('\xa0', ''))

        # 리스트를 출력한다.
        print(output)

    # 다음 페이지로 이동한다.
    countPage += 1


