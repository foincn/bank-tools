#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: bofa.py

from ghost import Ghost, Session
from bs4 import BeautifulSoup
import sms

gh = Ghost()
se = Session(gh, wait_timeout=30, display=True, viewport_size=(800, 553), download_images=True)

def login(username, password, answer='philos'):
    #url = 'https://bankofamerica.com'
    #se.open(url)
    index()
    #se.click('#LOGIN_MEDIUM')
    #se.fire('#LOGIN_MEDIUM', 'blur')
    #se.evaluate("document.getElementById('onlineId1').value='%s'" % username)
    #se.evaluate("document.getElementById('passcode1').value='%s'" % password)
    se.set_field_value('#enterID-input', username)
    se.set_field_value('#tlpvt-passcode-input', password)
    se.evaluate("enterOnlineIDFormSubmit();")
    se.wait_for_selector('#tlpvt-challenge-answer')
    #se.click('#signIn', expect_loading=True)
    #se.fire('#signIn', 'click')
    se.set_field_value('#tlpvt-challenge-answer', answer)
    try:
        se.click('#no-recognize')
    except:
        pass
    se.click('#verify-cq-submit', expect_loading=True)
    se.click('div.AccountItem.AccountItemDeposit > span.AccountActivity > a.quick-view-show')
    se.click('div.AccountItem.AccountItemCreditCard > span.AccountActivity > a.quick-view-show')
    se.sleep(3)
    #se.wait_for_selector('div.AccountActivityPanel')

def index():
    url = 'https://secure.bankofamerica.com/login/sign-in/signOnV2Screen.go'
    se.open(url)

def get_balance():
    html = se.content
    soup = BeautifulSoup(html, "html.parser")
    #source = soup.select('div.AccountActivityPanel')
    source = soup.select('li.show-quick-view')
    deposit_balance = source[0].select('span.balanceValue')[0].text
    cridit_avaliable = source[1].select('strong.TL_NPI_L1')[0].text
    minimum_payment = source[1].select('strong.TL_NPI_L1')[6].text
    text = '''Bank of America\r
支票账户余额：%s\r
信用卡剩余额度：%s\r
最低账单付款：%s\r
    ''' % (deposit_balance, cridit_avaliable, minimum_payment)
    print(text)
    sms.send_sms(16267318573, text)

login('ztang15', 'Tz')
get_balance()


