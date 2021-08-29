import xlrd
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sys
import zipfile
import os
import time
import logging
import requests
import sqlite3
import random
import string
import json
import platform
import re
import names
from contextlib import closing
from datetime import datetime
from fake_headers import Headers, browsers
from random import choice, choices, randint, uniform

os.system("color")
WEBRTC = os.path.join('extension', 'webrtc_control.zip')
ACTIVE = os.path.join('extension', 'always_active.zip')
FINGERPRINT = os.path.join('extension', 'fingerprint_defender.zip')
TIMEZONE = os.path.join('extension', 'spoof_timezone.zip')
counter = 0

############################# Database ####################################
DB_Log = True
DB_File = 'database.db'

############################# Logging ##################################### 
#Not implimented yet
log = logging.getLogger('werkzeug')
log.disabled = True

############################# SMS API ##################################### 
api_key = ''
country = '0' #0=Russia, 1=Ukraine, 12=USA, , 43=Germany, 32=Romania, 36=Canada : MORE -> https://sms-activate.ru/en/price

######################## Proxy settings ###################################  
#Start with proxy number
num = 0
category = "rp" #f=free / r=residential / rp=residential pool - If you use residential pool proxies we will always use the first proxy from file
background = False
auth_required = False
proxyfile = 'proxy.txt'
proxy_type = 'socks4' # -> https://github.com/TheSpeedX/PROXY-List -> proxy.txt


VIEWPORT = ['2560,1440', '1920,1080', '1440,900',
            '1536,864', '1366,768', '1280,1024', '1024,768']

CHROME = ['{8A69D345-D564-463c-AFF1-A69D9E530F96}',
          '{8237E44A-0054-442C-B6B6-EA0509993955}',
          '{401C381F-E0DE-4B85-8BD8-3F3F14FBDA57}',
          '{4ea16ac7-fd5a-47c3-875b-dbf4a2008c20}']

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

################################## Send key with a delay #########################  
def send_delayed_keys(element, text, delay=0.2):
    for c in text:
        endtime = time.time() + delay
        element.send_keys(c)
        time.sleep(endtime - time.time())

################################## Create Random Informations #########################  
def randomize(_option_,_length_):

    mon = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    gen = ["Male", "Female"]
    
    if _length_ > 0 :

        # Options:
        #       -p      for letters, numbers and symbols
        #       -l      for letters only
        #       -n      for numbers only
        #       -m      for month selection
        #       -d      for day selection
        #       -y      for year selection

        if _option_ == '-p':
            string._characters_='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+'
        elif _option_ == '-l':
            string._characters_='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        elif _option_ == '-n':
            string._characters_='1234567890'

        if _option_ == '-d':
            _generated_info_=random.randint(1,28)
        elif _option_ == '-y':
            _generated_info_=random.randint(1950,2000)
        elif _option_ == '-m':
            _generated_info_=mon[random.randint(0,11)]
        elif _option_ == '-g':
            _generated_info_=gen[random.randint(0,1)]
        else:
            _generated_info_=''
            for _counter_ in range(0,_length_) :
                _generated_info_= _generated_info_ + random.choice(string._characters_)
           
        return _generated_info_

    else:
        print('randomize: No valid length specified...')
        ext()

################################## Check if proxy is working #########################  
def check_proxy(agent, proxy, proxy_type):
    try:
        if category == 'f' and proxy_enable == True:
            headers = {
                'User-Agent': f'{agent}',
            }

            proxy_dict = {
                "http": f"{proxy_type}://{proxy}",
                "https": f"{proxy_type}://{proxy}",
            }
            response = requests.get(
                'https://www.youtube.com/', headers=headers, proxies=proxy_dict, timeout=30)
            status = response.status_code

        else:
            status = 200
    except:
        print(bcolors.FAIL + f"Error while checking proxy" + bcolors.ENDC)
        status = "error"

    return status

################################## Load Proxy from file #########################  
def load_proxy(filename):
    proxies = []

    load = open(filename)
    loaded = [items.rstrip().strip() for items in load]
    load.close()

    for lines in loaded:
        if lines.count(':') == 3:
            split = lines.split(':')
            lines = f'{split[2]}:{split[-1]}@{split[0]}:{split[1]}'
        proxies.append(lines)

    return proxies
 
################################## Download driver if not exists #########################   
def download_driver():
    OSNAME = 'win'

    return OSNAME
 
################################## Create Driver settings #########################   
def get_driver(agent, proxy, proxy_type, pluginfile):
    options = webdriver.ChromeOptions()
    options.headless = background
    options.add_argument(f"--window-size={choice(VIEWPORT)}")
    options.add_argument("--log-level=3")
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--lang=en-US")
    options.add_argument(f"user-agent={agent}")
    options.add_argument("--mute-audio")
    options.add_argument('--disable-features=UserAgentClientHint')
    webdriver.DesiredCapabilities.CHROME['loggingPrefs'] = {
        'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}

    if not background:
        options.add_extension(WEBRTC)
        options.add_extension(FINGERPRINT)
        options.add_extension(TIMEZONE)
        options.add_extension(ACTIVE)

    if auth_required:
        proxy = proxy.replace('@', ':')
        proxy = proxy.split(':')
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (proxy[2], proxy[-1], proxy[0], proxy[1])

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        options.add_extension(pluginfile)

    else:
        options.add_argument(f'--proxy-server={proxy_type}://{proxy}')

    dc = DesiredCapabilities.CHROME
    dc['goog:loggingPrefs'] = { 'browser':'ALL' }
    driver = webdriver.Chrome(options=options,desired_capabilities=dc)

    return driver

################################## Exit driver #########################  
def quit_driver(driver, pluginfile):
    try:
        os.remove(pluginfile)
    except:
        pass

    driver.quit()
    status = 400
    return status   

################################## Click trough the personalization #########################  
def click_whatever(driver):
    try:
        driver.find_element_by_xpath("//span[contains(text(), 'I agree')]").click()
    except:
        pass
        
    try:
        driver.find_element_by_xpath("//span[contains(text(), 'Confirm')]").click()
    except:
        pass
        
    try:
        driver.find_element_by_xpath("//span[contains(text(), 'Next')]").click()
    except:
        pass
        
    try:
        driver.find_element_by_xpath("//div[contains(text(), 'Express personalization (1 step)')]").click()
    except:
        pass
        
    try:
        driver.find_elements_by_class_name('VfPpkd-vQzf8d').click()
    except:
        pass
        
    return

################################## Check if username is already taken #########################  
def check_username_taken(driver, uName, rand_name):
    fName, lName = rand_name.split(" ")
    print(bcolors.OKCYAN + f"Check if username is available!!" + bcolors.ENDC)
    try:
        time.sleep(1)
        driver.find_element_by_xpath("//div[contains(text(), 'That username is taken')]").click()
        print(bcolors.FAIL + f"That username is taken. Try another!" + bcolors.ENDC)
        time.sleep(1)
        username = driver.find_element_by_id('username')
        time.sleep(1)
        username.clear()
        uName = fName + randomize('-n',4) + lName
        time.sleep(1)
        send_delayed_keys(username, uName)
        time.sleep(1)
        driver.find_element_by_name("ConfirmPasswd").send_keys(Keys.RETURN)
        time.sleep(1)
        check_username_taken(uName, rand_name)
    except:
        pass
        
    try:
        time.sleep(1)
        driver.find_element_by_xpath("//div[contains(text(), 'username must be between')]").click()
        print(bcolors.FAIL + f"Sorry, your username must be between 6 and 30 characters long." + bcolors.ENDC)
        time.sleep(1)
        username = driver.find_element_by_id('username')
        time.sleep(1)
        username.clear()
        uName = randomize('-l',10)
        time.sleep(1)
        send_delayed_keys(username, uName)
        time.sleep(1)
        driver.find_element_by_name("ConfirmPasswd").send_keys(Keys.RETURN)
        time.sleep(1)
        check_username_taken(uName, rand_name)
    except:
        pass
        
    return uName

################################ Create Database if not exists #########################
def create_database():
    global DB_Log
    global DB_File
    with closing(sqlite3.connect(DB_File)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS
            accounts (username TEXT, password TEXT, phone TEXT, status TEXT,  date TEXT)""")

            connection.commit()

################################ Insert into Database #########################
def update_database(username, password, phone, status):
    global DB_Log
    global DB_File
    if DB_Log == True:
        today = str(datetime.today().date())
        with closing(sqlite3.connect(DB_File, timeout=10)) as connection:
            with closing(connection.cursor()) as cursor:
                try:
                    cursor.execute(
                        "INSERT INTO accounts VALUES (?, ?, ?, ?, ?)", (username, password, phone, status, today),)
                except:
                    print(bcolors.FAIL + f"DB ERROR...insert won't work" + bcolors.ENDC)

                connection.commit()
                
################################## Starting Account Creation #########################
def start(proxy):
    global num
    global proxy_type
    global api_key
    global country
    global DB_Log
    global category
    global counter
    counter += 1
    oldnum = num
    num = num + 1
    
    if category == "rp":
        num = 0
        oldnum = 0
    print(f'################################## START ID:{counter} #########################')
    print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    ################################## Download Driver #########################
    OSNAME = download_driver()
    ################################## Generate Info #########################
    header = Headers(browser="chrome",os=OSNAME,headers=False).generate()
    userAgent = header['User-Agent']
    print(f'Checking Proxy:{proxy}')
    status = check_proxy(userAgent, proxy, proxy_type)

    if status == 200:
        try:
        
            ################################## Form Informations ##############################
            url = 'https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp&hl=en'
            gender = randomize('-g',1)
            rand_name = names.get_full_name(gender=gender)
            fName, lName = rand_name.split(" ")
            uName = fName + randomize('-n',4) + lName
            password = randomize('-p',16)
            confpassword = password
            recoverymail = ''
            month = randomize('-m',1)
            day = randomize('-d',1)
            year = randomize('-y',1)
            symbol = '+'
            pluginfile = os.path.join('extension', f'proxy_auth_plugin{oldnum}.zip')
            ##################################################################################
            
            print("proxy: ", proxy)
            print("Username: ", uName)
            print("Password:", password + '\n')
        
            ################################## Browser Driver ######################### #######           
            driver = get_driver(userAgent, proxy, proxy_type, pluginfile)        
            driver.delete_all_cookies()
            driver.get(url)
            time.sleep(2)
            
            ############################## CHECK CHROME CONSOLE LOG ########################### 
            #This is to prevent money lose on sms activation because the site is not loaded the correct way
            errconclose0 = "ERR_CONNECTION_RESET"
            errconclose1 = "ERR_PROXY_CONNECTION_FAILED"
            for e in driver.get_log('browser'):
                if re.search(errconclose0, str(e)):
                    print(bcolors.FAIL + errconclose0 + bcolors.ENDC)
                    driver.quit()
                    start(proxy_list[num])   
                elif re.search(errconclose1, str(e)):
                    print(bcolors.FAIL + errconclose1 + bcolors.ENDC)
                    driver.quit()
                    start(proxy_list[num])  
            ##################################################################################
        
            ############################# Check if webiste is loaded ######################### 
            current_Url = driver.current_url
            du_Url = 'https://accounts.google.com/signup'
            if not du_Url in current_Url:
                print(bcolors.FAIL + f"Restarting...redirected to wrong site" + bcolors.ENDC)
                driver.quit()
                start(proxy_list[num])
            ##################################################################################
            
            time.sleep(2)
            
            ############################# Robot check? ######################### 
            current_Url = driver.current_url
            du_Url = 'https://www.google.com/sorry/index'
            if du_Url in current_Url:
                print(bcolors.FAIL + f"Restarting...robot check active" + bcolors.ENDC)
                driver.quit()
                start(proxy_list[num])
            ##################################################################################
        
            ############################# Filling out Signup form ############################
            firstName = driver.find_element_by_id('firstName')
            send_delayed_keys(firstName, fName)
        
            lastName = driver.find_element_by_id('lastName')
            send_delayed_keys(lastName, lName)
        
            username = driver.find_element_by_id('username')
            send_delayed_keys(username, uName)
        
            time.sleep(1)
            Passwd = driver.find_element_by_name('Passwd')
            send_delayed_keys(Passwd, password)
        
            time.sleep(1)
            ConfirmPasswd = driver.find_element_by_name('ConfirmPasswd')
            send_delayed_keys(ConfirmPasswd, confpassword)

            time.sleep(1)
            driver.find_element_by_name("ConfirmPasswd").send_keys(Keys.RETURN)
            ##################################################################################
            
            ############################# Check if username exists ###########################
            time.sleep(5)
            NewuName = check_username_taken(driver, uName, rand_name)
            if not uName == NewuName:
                uName = NewuName
                print("New Username: ", uName)
            ##################################################################################
        
            ################################## API ###########################################
            time.sleep(5)
            current_Url = driver.current_url
            du_Url = 'https://accounts.google.com/signup/v2/webgradsidvphone'
            if not du_Url in current_Url:
                uName = check_username_taken(driver, uName, rand_name)
                print("New Username: ", uName)
            
            try:
                driver.find_element_by_id('phoneNumberId')
            except NoSuchElementException:
                print(bcolors.FAIL + f"Site not correct loaded..." + bcolors.ENDC)
                print("\n")
                driver.quit()
                start(proxy_list[num])
                
            print(bcolors.OKGREEN + f"Verify Your Phone number!!" + bcolors.ENDC)
            time.sleep(1)
        
            country = str(country)
            operator = 'any'
            service = 'go'
            ref = '613879'
            forward = '0'
        
            status_ready = '1'
            status_complete = '6'
            status_ban = '8'
        
            ######## Change of activation status
            access_ready = 'ACCESS_READY'  # number readiness confirmed
            access_ready_get = 'ACCESS_RETRY_GET'  # waiting for a new sms
            access_activation = 'ACCESS_ACTIVATION'  # service successfully activated
            access_cancel = 'ACCESS_CANCEL'  # activation canceled
        
            ######## Get activation status:
            status_wait = 'STATUS_WAIT_CODE'  # waiting for sms
            status_wait_retry = "STATUS_WAIT_RETRY"  # waiting for code clarification
            status_wait_resend = 'STATUS_WAIT_RESEND'  # waiting for re-sending SMS *
            status_cancel = 'STATUS_CANCEL'  # activation canceled
            status_ok = "STATUS_OK"  # code received
        
            # POSSIBLE MISTAKES: (ERROR)
            error_sql = 'ERROR_SQL'  # SQL-server error
            no_activation = 'NO_ACTIVATION'  # activation id does not exist
            bad_service = 'BAD_SERVICE'  # incorrect service name
            bad_status = 'BAD_STATUS'  # incorrect status
            bad_key = 'BAD_KEY'  # Invalid API key
            bad_action = 'BAD_ACTION'  # incorrect action
        
            # Balance
            balance = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=getBalance')
            info = balance.text
            b1, b2 = info.split(":")
            print("Balance: ", b2)
        
            # number of available phones
            find_numbers = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=getNumbersStatus&country=' + country + '&operator=' + operator)
            num_numbers = json.loads(find_numbers.text)
        
            a = num_numbers['go_0']
            if a == '0':
                print(bcolors.FAIL + f"No Numbers available" + bcolors.ENDC)
                driver.quit()
                start(proxy_list[num])
            else:
                print('Available phone numbers: ', a)
        
                # Order Number
                order_number = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=getNumber&service=' + service + '&forward=' + forward + '&operator=' + operator + '&ref=' + ref + '&country=' + country)
                print('buy TEXT: ', order_number.text)
                
                if order_number.text == "NO_NUMBERS":
                    print(bcolors.FAIL + f"No Numbers available" + bcolors.ENDC)
                    driver.quit()
                    start(proxy_list[num])
                elif order_number.text == "NO_BALANCE":
                    print(bcolors.FAIL + f"No Balance...Please TopUp" + bcolors.ENDC)
                    driver.quit()
                    sys.exit()
                
                info = order_number.text
                a, id, phone_number = info.split(":")
                print('Id: ', id)
                print('Phone Number: ', phone_number)
        
                time.sleep(5)
                phonenumber = driver.find_element_by_id('phoneNumberId')
                send_delayed_keys(phonenumber, symbol + phone_number)
                time.sleep(1)
                driver.find_element_by_id("phoneNumberId").send_keys(Keys.RETURN)
                time.sleep(5) 
                try:
                    driver.find_element_by_id('code')
                except NoSuchElementException:
                    ch_activation_status = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=setStatus&status=' + status_ban + '&id=' + id + '&forward=' + forward)
                    print(bcolors.FAIL + f"sorry this number has some issues" + bcolors.ENDC)
                    driver.quit()
                    start(proxy_list[num])
        
                # Activation status
                time.sleep(5)
                ch_activation_status = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=setStatus&status=' + status_ready + '&id=' + id + '&forward=' + forward)
                if ch_activation_status.text in access_ready:
                    print("number readiness confirmed\n")
        
                    # SMS status
                    time.sleep(3)
                    get_sms = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=getStatus&id=' + id)
                    code = get_sms.text
        
                    waitcounter = 0
                    while status_wait in code or status_ok in code or status_cancel in code or status_wait_resend in code or status_wait_retry in code:
                        if waitcounter == 6:
                            ch_activation_status = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=setStatus&status=' + status_ban + '&id=' + id + '&forward=' + forward)
                            print("Cancel the activation")
                            print(bcolors.FAIL + f"sorry this number has some issues" + bcolors.ENDC)
                            driver.quit()
                            start(proxy_list[num])
                    
                        if code in status_wait:
                            print("wait sometime for SMS")
                            waitcounter += 1
                            time.sleep(20)
                            get_sms = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=getStatus&id=' + id)
                            code = get_sms.text
                        elif status_ok in code:
                            tex, m_code = code.split(':')
                            print("Your SMS code: ", m_code)
                            time.sleep(2)
                            codenumber = driver.find_element_by_id('code')
                            send_delayed_keys(codenumber, m_code)
                            time.sleep(2)
                            
                            driver.find_element_by_id("code").send_keys(Keys.RETURN)
                            # print("PVA complete")
                            break
                        else:
                            ch_activation_status = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=setStatus&status=' + status_ban + '&id=' + id + '&forward=' + forward)
                            print("Cancel the activation")
                            print(bcolors.FAIL + f"sorry this number has some issues" + bcolors.ENDC)
                            driver.quit()
                            start(proxy_list[num])
        
                else:
                    ch_activation_status = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=setStatus&status=' + status_ban + '&id=' + id + '&forward=' + forward)
                    print("Cancel the activation")
                    print(bcolors.FAIL + f"sorry this number has some issues" + bcolors.ENDC)
                    driver.quit()
                    start(proxy_list[num])
        
            time.sleep(3)
            phone_url = "https://accounts.google.com/signup/v2/webgradsidvphone"
            veryfi_url = "https://accounts.google.com/signup/v2/webgradsidvverify"
            main_url = "https://accounts.google.com/signup/v2/webpersonaldetails"
            a = driver.current_url
            while veryfi_url in a or phone_url in a or main_url in a:
                if main_url in a:
                    break
                else:
                    time.sleep(2)
                    print("This is not correct page\nplz wait some time")
                    a = driver.current_url
        
            ############################### Enter Person Informations #########################  
            driver.find_element_by_id('phoneNumberId').clear()
        
            time.sleep(1)
            RecoveryEmail = driver.find_element_by_xpath('//*[@spellcheck="false"]')
            send_delayed_keys(RecoveryEmail, recoverymail)
        
            time.sleep(1)
            driver.find_element_by_xpath('//*[@aria-label="Day"]').send_keys(int(day))
        
            time.sleep(1)
            element = driver.find_element_by_id('month')
            drp = Select(element)
            drp.select_by_visible_text(month)
        
            time.sleep(1)
            driver.find_element_by_xpath('//*[@aria-label="Year"]').send_keys(int(year))
        
            time.sleep(1)
            element = driver.find_element_by_id('gender')
            drp = Select(element)
            drp.select_by_visible_text(gender)
        
            time.sleep(2)
            driver.find_element_by_xpath("//span[contains(text(), 'Next')]").click()
            ##################################################################################
            
            ######################### Click trough personal settings #########################  
            time.sleep(10)
            click_whatever(driver)
            time.sleep(5)
            click_whatever(driver)
            time.sleep(5)
            click_whatever(driver)
            time.sleep(2)
            click_whatever(driver)
            time.sleep(2)
            click_whatever(driver)
            time.sleep(2)
            click_whatever(driver)
            time.sleep(2)
            click_whatever(driver)
            ##################################################################################
            
            ############################ Check Database ######################################
            if DB_Log == True:
                if os.path.exists(DB_File) == False:
                    create_database()
            ##################################################################################
            
            time.sleep(10)
            current_Url = driver.current_url
            du_Url = 'https://accounts.google.com/signup/v2/webtermsofservice'
            if du_Url in current_Url:
                time.sleep(5)
                
                click_whatever(driver)
                    
                time.sleep(10)
                cur_url = driver.current_url
                fail_url = 'https://accounts.google.com/'
                if fail_url in cur_url:
                    print("This account take some time")
                    print("Plz Cut this browser yourself\n")
                    time.sleep(10)
                    click_whatever(driver)
                    time.sleep(5)
                    click_whatever(driver)
                    time.sleep(5)
                    click_whatever(driver)
                    time.sleep(5)
                    click_whatever(driver)
                    
                    with open("accounts.txt", "a") as myfile:
                        update_database(uName, password, phone_number, "Bad")
                        myfile.write("\n")
                        myfile.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
                        myfile.write("\n")
                        myfile.write("Username: " + uName)
                        myfile.write("\n")
                        myfile.write("Password: " + password)
                        myfile.write("\n")
                        myfile.write("Phone Number: +" + phone_number)
                        myfile.write("\n")
                        myfile.write("Status: Bad")
                        myfile.write("\n")
                        myfile.write("______________________________________")
                        myfile.write("\n")
                    driver.quit()
        
                else:
                    time.sleep(3)
                    with open("accounts.txt", "a") as myfile:
                        update_database(uName, password, phone_number, "OK")
                        myfile.write("\n")
                        myfile.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
                        myfile.write("\n")
                        myfile.write("Username: " + uName)
                        myfile.write("\n")
                        myfile.write("Password: " + password)
                        myfile.write("\n")
                        myfile.write("Phone Number: +" + phone_number)
                        myfile.write("\n")
                        myfile.write("Status: OK")
                        myfile.write("\n")
                        myfile.write("______________________________________")
                        myfile.write("\n")
                    driver.quit()
            else:
                time.sleep(10)
                cur_url = driver.current_url
                fail_url = 'https://accounts.google.com/'
                if fail_url in cur_url:
                    print("This account take some time")
                    time.sleep(10)
                    click_whatever(driver)
                    time.sleep(5)
                    click_whatever(driver)
                    time.sleep(5)
                    click_whatever(driver)
                    time.sleep(5)
                    click_whatever(driver)
        
                    with open("accounts.txt", "a") as myfile:
                        update_database(uName, password, phone_number, "Bad")
                        myfile.write("\n")
                        myfile.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
                        myfile.write("\n")
                        myfile.write("Username: " + uName)
                        myfile.write("\n")
                        myfile.write("Password: " + password)
                        myfile.write("\n")
                        myfile.write("Phone Number: +" + phone_number)
                        myfile.write("\n")
                        myfile.write("Status: Bad")
                        myfile.write("\n")
                        myfile.write("______________________________________")
                        myfile.write("\n")
                    time.sleep(100000)
                    driver.quit()
                else:
                    time.sleep(3)
        
                    with open("accounts.txt", "a") as myfile:
                        update_database(uName, password, phone_number, "OK")
                        myfile.write("\n")
                        myfile.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
                        myfile.write("\n")
                        myfile.write("Username: " + uName)
                        myfile.write("\n")
                        myfile.write("Password: " + password)
                        myfile.write("\n")
                        myfile.write("Phone Number: +" + phone_number)
                        myfile.write("\n")
                        myfile.write("Status: OK")
                        myfile.write("\n")
                        myfile.write("______________________________________")
                        myfile.write("\n")
                        
            complete = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key='+api_key+'&action=setStatus&status='+ status_complete +'&id='+id+'&forward='+forward)
            print(bcolors.OKGREEN + f'Now, this account is completed.\n' + bcolors.ENDC)
            driver.quit()
        except:
            driver.quit()
            print(bcolors.FAIL + f"Proxie not working ID:" + str(oldnum) + bcolors.ENDC)
            print("\n")
            start(proxy_list[num])
    else:
        print(bcolors.FAIL + f"Proxie not working ID:" + str(oldnum) + bcolors.ENDC)
        print("\n")
        
    print("\n")
    start(proxy_list[num])
    return

################################## Bot start #########################  
proxy_list = load_proxy(proxyfile)
proxy_list = list(filter(None, proxy_list))
total_proxies = len(proxy_list)
print(bcolors.OKGREEN + f'Total proxies : {total_proxies}' + bcolors.ENDC)

start(proxy_list[num])