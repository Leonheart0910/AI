from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup
import sys
import re

keyword = str(input())
# 브라우저 생성
browser = webdriver.Chrome('C:/chromedriver.exe')

# 해당 웹사이트 열기
browser.get('https://www.naver.com')
browser.implicitly_wait(10)  # 로딩 완료까지 10초 기다림

# 쇼핑 메뉴 클릭
browser.find_element(By.CSS_SELECTOR, "a.nav.shop").click()
time.sleep(2)  # 로딩 완료까지 10초 기다림

search = browser.find_element(By.CSS_SELECTOR, "input._searchInput_search_text_3CUDs")
search.click()

# 검색어 입력
search.send_keys(keyword)
search.send_keys(Keys.ENTER)

# 스크롤 전 높이
before_h = browser.execute_script("return window.scrollY")
for i in range(0,10):
    # 무한 스크롤
    while True:
        # 맨아래로 스크롤 내리기
        browser.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)

        # 스크롤 페이지 로딩 시간
        time.sleep(1)

        # 스크롤 후 높이
        after_h = browser.execute_script("return window.scrollY")

        if after_h == before_h:
            break
        before_h = after_h

        # 상품정보 div
        items = browser.find_elements(By.CSS_SELECTOR, ".basicList_mall_title__FDXX5")

        # 링크를 저장할 배열
        links = []

        for item in items:
            link = item.find_element(By.CSS_SELECTOR, ".basicList_mall_title__FDXX5 > a").get_attribute('href')
            
            # 'https://smartstore.naver.com/'으로 시작하는 URL만 배열에 추가
            if link.startswith('https://smartstore'):
                links.append(link)

    # 배열에 저장된 링크 출력
    #for link_store in links:
    #    print(link_store)

    list_number = len(links)

    #print((links))

    extracted_links = []

    for link in links:
        # 링크에서 원하는 부분을 추출합니다.
        # 예: https://smartstore.naver.com/inflow/outlink/url?url=https%3A%2F%2Fsmartstore.naver.com%2Floneque&channelNo=100126531&tr=slsl
        # 추출된 부분: loneque
        match = re.search(r'https%3A%2F%2Fsmartstore\.naver\.com%2F(.+?)&', link)
        if match:
            extracted_links.append(match.group(1))

    # 새로운 배열에 저장된 링크 출력
    #for extracted_link in extracted_links:
    #    print(extracted_link)

    # 추출된 문자와 'https://smartstore.naver.com/'을 합쳐 저장할 배열
    combined_links = []

    for extracted_link in extracted_links:
        # 'https://smartstore.naver.com/'와 추출된 문자를 합칩니다.
        combined_link = f'https://smartstore.naver.com/{extracted_link}'
        combined_links.append(combined_link)


    

    # 새로운 배열에 저장된 링크 출력
    #for combined_link in combined_links:
    #    print(combined_link)

    for i in range(0, len(combined_links)-1):
        # 네이버 쇼핑 사이트에서 검색어를 사용하여 검색
        url = f"{combined_links[int(i)]}"
        response = requests.get(url)

        # 웹 페이지 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 'BEST' 또는 'number1' 텍스트를 포함하는 모든 요소 찾기
        best_elements = soup(text=['BEST', '베스트'])
        # 찾은 요소들의 직전 a 태그에서 href 속성 값 출력
        for element in best_elements:
            previous_link = element.find_previous('a', href=True)
            if previous_link:
                print("https://smartstore.naver.com" + previous_link['href'])
        print("베스트 상품 출력 완료  " + "다음 스토어")
    
    
    combined_links.clear()  
    links.clear()
    extracted_links.clear() 

    print(links)

    browser.find_element(By.CSS_SELECTOR, "a.pagination_next__pZuC6").click()
    time.sleep(2)  # 로딩 완료까지 10초 기다림