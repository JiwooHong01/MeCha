import time
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# 1. 웹 드라이버 설정 (Chrome 드라이버 사용 예)
driver = webdriver.Chrome()  # ChromeDriver의 경로를 지정해줄 수 있습니다.
driver.maximize_window()

# 2. 리스트 페이지로 이동 (여기에 실제 URL 입력)
list_page_url = "https://www.cdc.gov/health-topics.html#cdc-atozlist"  # 변경 필요


# 3. li 요소들이 포함된 ul 요소 선택 (제공해주신 XPath 사용)
# ul_xpath = "/html/body/div[4]/main/div[3]/div/div[4]/div[2]/div/div/div/div[2]/div/div/div/div[3]/div/ul"
# ul_xpath = "/html/body/div[4]/main/div[3]/div/div[4]/div[2]/div/div/div/div[2]/div/div/div/div[4]/div/ul"
name = ["C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
for i in range(7, 29):
    driver.get(list_page_url)
    time.sleep(3)  # 페이지 로드 대기
    ul_xpath = "/html/body/div[4]/main/div[3]/div/div[4]/div[2]/div/div/div/div[2]/div/div/div/div[" + str(i) + "]/div/ul"
    ul_element = driver.find_element(By.XPATH, ul_xpath)

    # 4. ul 내부의 모든 li 요소들 가져오기
    li_elements = ul_element.find_elements(By.TAG_NAME, "li")
    # print("Lis")
    # print(li_elements)
    href_list = []

    # 5. 각 li 요소에 대해 처리
    for index, li in enumerate(li_elements, start=1):
        try:
            # 각 li 내부에 있는 첫번째 a 태그의 href 추출 (XPath 예시: li[1]/a)
            # 만약 li 내부에 여러 a 태그가 있다면, 원하는 a 태그를 정확히 선택하세요.
            a_element = li.find_element(By.XPATH, ".//a")
            href = a_element.get_attribute("href")
            href_list.append(href)
        except NoSuchElementException:
            print(f"li 요소 {index}에서 링크를 찾지 못했습니다.")
            continue
    results = []
    for href in href_list:
        # 대상 페이지로 이동
        driver.get(href)
        time.sleep(2)  # 페이지 로드 대기

        page_text = driver.find_element(By.XPATH, '/html/body').text
        results.append(page_text)

    
    

    # 6. 결과를 CSV 파일로 저장
    df = pd.DataFrame(results)
    csv_filename = "crawled_results" + name[i-5] + ".csv"
    df.to_csv(csv_filename, index=False, encoding="utf-8-sig")
    print(f"크롤링 결과가 {csv_filename} 파일로 저장되었습니다.")

# 5. driver 종료
driver.quit()