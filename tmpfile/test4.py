from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re, copy

def is_gridcell_and_visible(tag):
    if( not tag.has_attr('role')):
        return False
    if( tag.has_attr('style') and ('display: none' in tag.attrs['style'] or 'display:none' in tag.attrs['style'])):
        return False
    else:
        return True


def collectAllRecord():
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

    if limitRecord == 0 or totalRecord == 0:
        return
    elif limitRecord >= totalRecord:
        lastPage = 1
        lastRow = totalRecord - 1
    else:
        lastPage = (totalRecord // limitRecord) + 1
        lastRow = (totalRecord % limitRecord) - 1

    print('페이지당 레코드 수는', limitRecord)
    print('총 레코드 수는', totalRecord)
    print('마지막 페이지는', lastPage)
    print('마지막 행은', lastRow)

    countPage = 1

    # 수강편람 데이터 테이블의 첫 페이지 부터 마지막 페이지 까지 반복한다.
    while (countPage <= lastPage):
        # BeautifulSoup 객체를 만든다.
        html = BeautifulSoup(browser.page_source, 'html.parser')
        print(countPage, '페이지')

        # 일반적인 페이지이면 첫행부터 limitRecord 수 만큼 행을 가져온다.
        # 그러나 마지막 페이지는 첫행부터 마지막 행까지(포함) 가져온다. 왜냐하면 마지막 페이지에서도 limitRecord 만큼의 행이 빈칸으로 존재하기 때문에 불필요한 행을 조사하는 경우가 있다.
        if (countPage == lastPage):
            rows = html.find_all(id=re.compile('^(row)[0-9]+jqxgrid$'), limit=lastRow + 1)
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
                if (cell.text == None):
                    cell.text = " "
                output.append(cell.text.replace('\xa0', ''))

            # 리스트를 출력한다.
            print(output)

        # 다음 페이지로 이동한다.
        countPage += 1

# 검색 버튼을 누르는 함수
def clickSearchButton():
    browser.find_element_by_xpath('//a[@href="javascript:searchGb(\'search\',1);"]').click()

def searchByCategory(category):
    if not category:
        # 기저 사례
        # 모든 category를 정했으면 검색 버튼을 누른다.
        clickSearchButton()
        # 버튼을 누른 뒤에 검색된 강의 목록을 모두 모은다.
        collectAllRecord()
    else:
        # 파이썬에서는 mutable 변수에 대해 call by reference를 취하므로 원래 값의 변경을 막기 위해 입력받은 categoryID를 복사한다.
        category = copy.deepcopy(category)
        categoryInfo = category.pop(0)
        # 입력받은 categoryID에서 맨 앞의 값을 선택하여 검색에 필요한 category들 중에 하나를 선택한다.
        selectedCategory = Select(browser.find_element_by_id(categoryID))

        # 선택된 category에는 드롭다운 메뉴처럼 여러 Item들이 존재하므로 item들 중에 하나를 선택한 뒤에 재귀 호출한다.
        categoryItems = selectedCategory.options
        for categoryItem in categoryItems:
            # 전체는 검색하는 의미가 없으므로 예외 처리
            if not categoryItem.text == '전체':
                selectedCategory.select_by_visible_text(categoryItem.text)
                searchByCategory(categoryInfos)

# Chrome 브라우저를 통해 연세 수강편람 페이지를 방문
# (수강편람 페이지가 JS로 로드되어 페이지가 변하기 때문에 requests 모듈 대신 selenium 모듈을 사용)
browser = webdriver.Firefox()
browser.get('http://ysweb.yonsei.ac.kr:8888/curri120601/curri_new.jsp#top')

# 년도 메뉴에서 2018년을 선택
# 2018년 value = '2018'
year = Select(browser.find_element_by_id('HY'))
year.select_by_value('2018')

# 학기 메뉴에서 1학기를 선택
# 1학기 value = '1'
semester = Select(browser.find_element_by_id('HG'))
semester.select_by_value('1')

# 대학 메뉴에서 신촌 캠퍼스를 선택
# 신촌 캠퍼스 value = 's1'
university = Select(browser.find_element_by_id('OCODE0'))
university.select_by_value('s1')

# 단과 메뉴에서 공과대학을 선택
# 공과대학 value = 's1104000H1'
# college = Select(browser.find_element_by_id('OCODE1'))
# college.select_by_value('s1104000H1')

# 강의 목록을 검색하는데 필요한 category의 ID들을 가져온다.
# 년도 - HY, 학기 - HG, 대학 - OCODE0, 단과 - OCODE1, 학과 - S2 이다.
# categoryID = ['OCODE1','S2']
category= [{'name':'university','id':'OCODE0'},{'name':'college','id':'OCODE1'}]

# 정의된 category들을 차례대로 모두 선택한다.
# 다시 그 안에 있는 모든 item(예를 들면 학과라는 category에는 컴과라는 item이 있다)들을 차례대로 선택하여 강의 목록을 검색한다.
searchByCategory(category)
