from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import calendar

chrome_driver_path = "/usr/local/bin/chromedriver-linux64/chromedriver"  # 크롬 드라이버의 경로를 지정
chrome_options = Options()
chrome_options.add_argument("--headless")  # 헤드리스 모드 (브라우저 UI 없이 실행)
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# 방문할 웹 페이지 URL
url = "https://at.agromarket.kr/domeinfo/smallTrade.do"
driver.get(url)
wait = WebDriverWait(driver, 10)

# 설정할 연도 범위
start_year = 2019
end_year = 2023

for year in range(start_year, end_year + 1):
    for month in range(1, 13):
        # 페이지를 새로 고침하여 각 루프의 시작 상태를 초기화
        driver.refresh()
        time.sleep(2)

        start_date = datetime.date(year, month, 1)
        
        # 각 달의 마지막 날짜를 계산
        if month == 12:
            end_date = datetime.date(year, month, 31)
        else:
            last_day = calendar.monthrange(year, month)[1]
            end_date = datetime.date(year, month, last_day)

        # JavaScript를 사용하여 값 설정
        driver.execute_script(f"document.querySelector('#startDate').value = '{start_date}';")
        driver.execute_script(f"document.querySelector('#endDate').value = '{end_date}';")
        time.sleep(1)

        # 값이 설정되었는지 확인
        start_date_value = driver.execute_script("return document.querySelector('#startDate').value;")
        end_date_value = driver.execute_script("return document.querySelector('#endDate').value;")
        print(f"Year: {year}, Month: {month}, Start Date: {start_date_value}, End Date: {end_date_value}")

        # 도매시장 설정 (whsalCd)
        whsal_cd_select = Select(wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#whsalCd'))))
        whsal_cd_select.select_by_index(17)
        time.sleep(1)

        # 부류 설정 (divLarge) <과일과채류>
        driver.execute_script("""
            var largeItems = document.querySelectorAll("#divLarge a");
            for (var i = 0; i < largeItems.length; i++) {
                if (largeItems[i].innerText.includes('과일과채류')) {
                    largeItems[i].click();
                    break;
                }
            }
        """)
        time.sleep(1)

        # 검색 버튼 클릭
        search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#btnSearch')))
        driver.execute_script("arguments[0].click();", search_button)

        # 검색 결과가 로드될 시간을 주기 위해 잠시 대기
        time.sleep(3)

        # 엑셀 다운로드 버튼 클릭
        download_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.wrap > div.sub_wrap > div.sub_conts_wrap > div.sub_content > div.btn_search_box > div > button.btn_down')))
        driver.execute_script("arguments[0].click();", download_button)

        # 잠시 대기 (다운로드가 시작될 시간을 위해)
        time.sleep(5)

# 웹 드라이버 종료
driver.quit()
