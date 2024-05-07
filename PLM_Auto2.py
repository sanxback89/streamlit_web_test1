from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import time

# ChromeOptions 객체 생성
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--ignore-certificate-errors")  # SSL 인증서 검사 비활성화 옵션 추가
options.accept_insecure_certs = True  # 보안 인증서 오류 무시

# 옵션을 포함하여 웹 드라이버 실행
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

# https://intranet.gap.com/en_us/vendor.html 웹사이트 접속
driver.get("https://intranet.gap.com/en_us/vendor.html")

# 로그인 정보
username = "Vptd325"
password = "Entks1457419!"
# 보안 질문 답변
favorite_sport_answer = "running"
first_car_make_answer = "tesla"

# 로그인 및 보안 질문 처리
try:
    # 로그인 페이지가 로드될 때까지 대기
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "pf.username"))
    )

    # 아이디와 비밀번호 입력
    driver.find_element(By.NAME, "pf.username").send_keys(username)
    driver.find_element(By.NAME, "pf.pass").send_keys(password)

    # 로그인 실행
    driver.execute_script("postOk();")

    # 보안 질문 페이지 로드 대기
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//input[contains(@name, 'pf.challengeanswer')]"))
    )

    # 보안 질문 필드 확인
    challenge_fields = driver.find_elements(By.XPATH, "//input[contains(@name, 'pf.challengeanswer')]")
    challenge_labels = driver.find_elements(By.CLASS_NAME, "gapinc-input-label")

    for i in range(len(challenge_labels)):
        if "first car" in challenge_labels[i].text.lower():
            challenge_fields[i].send_keys(first_car_make_answer)
        elif "favorite sport" in challenge_labels[i].text.lower():
            challenge_fields[i].send_keys(favorite_sport_answer)

    # 보안 질문 제출
    driver.execute_script("postSubmit();")
    WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))
except Exception as e:
    print(f"로그인 또는 보안 질문 처리 중 에러 발생: {str(e)}")

def wait_and_click(xpath, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        actions = ActionChains(driver)
        actions.move_to_element(element).click().perform()
    except (TimeoutException, StaleElementReferenceException):
        print(f"요소를 클릭하는 중 에러 발생: {xpath}")
        # 에러 발생 시 10초 대기 후 재시도
        time.sleep(10)
        wait_and_click(xpath, timeout)

def wait_for_page_load(timeout=10):
    try:
        WebDriverWait(driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
    except TimeoutException:
        print("페이지 로드 대기 중 타임아웃 발생")

# Applications 드롭다운 클릭
try:
    wait_and_click("//a[@title='Applications']")

    # PLM Centric 링크가 나타날 때까지 대기
    wait_and_click("//a[@title='PLM Centric']")

    # PLM Centric 페이지가 로드될 때까지 대기
    wait_for_page_load()

    print("PLM Centric 페이지로 이동했습니다.")

    # PLM Centric 링크 클릭
    wait_and_click("//a[@href='https://plmprod.gapinc.com/csi-requesthandler/sso/idp-redirect']")

    # 새 창으로 전환
    driver.switch_to.window(driver.window_handles[-1])

    print("PLM Centric 사이트로 이동했습니다.")

    # PLM Centric 페이지가 완전히 로드될 때까지 대기
    wait_for_page_load(timeout=30)

    print("PLM Centric 페이지가 로드되었습니다.")

    # Design 링크 클릭
    wait_and_click("//span[@class='MuiTab-wrapper' and @data-csi-tab-name='Design']")

    print("Design 링크를 클릭했습니다.")

    # OLD NAVY - WOMENS 링크 클릭
    wait_and_click("//a[@class='browse' and @href='/WebAccess/home.html#URL=C54444590']")

    print("OLD NAVY - WOMENS 링크를 클릭했습니다.")
    
    # BOMs 링크 클릭
    
    wait_and_click("//span[@class='MuiTab-wrapper' and @data-csi-tab-name='BOMs']", timeout=100)
    print("BOMs 링크를 클릭했습니다.")

    # BOMs 페이지가 완전히 로드될 때까지 대기
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='uniqName_4_61']/span[1]"))
    )
    print("BOMs 페이지가 완전히 로드되었습니다.")

    # "csi-wait" 요소의 존재 여부 확인
    try:
        csi_wait = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "csi-wait"))
        )
        print("csi-wait 요소가 화면에 표시되어 있습니다.")
        
        # "csi-wait" 요소가 사라질 때까지 대기
        WebDriverWait(driver, 100).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "csi-wait"))
        )
        print("csi-wait 요소가 사라졌습니다.")
    except TimeoutException:
        print("csi-wait 요소가 화면에 표시되어 있지 않습니다.")

    # JavaScript를 사용하여 "csi-wait" 요소 제거
    driver.execute_script("""
        var elements = document.getElementsByClassName("csi-wait");
        while (elements.length > 0) {
            elements[0].parentNode.removeChild(elements[0]);
        }
    """)
    print("JavaScript를 사용하여 csi-wait 요소를 제거했습니다.")

    # Export 드롭다운 메뉴 클릭
    export_dropdown_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='uniqName_4_61']/span[1]"))
    )
    export_dropdown_menu.click()
    print("Export 드롭다운 메뉴를 클릭했습니다.")

    # 클릭할 요소가 나타날 때까지 최대 10초 동안 대기
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//td[@class='dijitReset dijitMenuItemLabel' and @id='uniqName_4_58_text']"))
    )

    # 요소 클릭
    element.click()
    print("클릭할 요소를 클릭했습니다.")

except TimeoutException:
    print("특정 요소를 찾을 수 없거나 작업 수행 중 에러가 발생했습니다.")

# 사용자의 입력을 기다리기 위해 대기
input("Press Enter to close the browser…")

# 웹 브라우저 종료
driver.quit()