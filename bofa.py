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
    se.click('#LOGIN_MEDIUM')
    se.fire('#LOGIN_MEDIUM', 'blur')
    se.evaluate("document.getElementById('onlineId1').value='%s'" % username)
    se.evaluate("document.getElementById('passcode1').value='%s'" % password)
    se.click('#signIn', expect_loading=True)
    se.set_field_value('#tlpvt-challenge-answer', answer)
    try:
        se.click('#no-recognize')
    except:
        pass
    se.click('#verify-cq-submit', expect_loading=True)
    se.click('div.AccountItem.AccountItemDeposit > span.AccountActivity > a.quick-view-show')
    se.click('div.AccountItem.AccountItemCreditCard > span.AccountActivity > a.quick-view-show')

def index():
    url = 'https://secure.bankofamerica.com/myaccounts/signin/signIn.go?returnSiteIndicator=GAIEC&langPref=en-us&request_locale=en-us&capturemode=N&newuser=false&bcIP=F'
    se.open(url)

def get_balance():
    html = se.content
    soup = BeautifulSoup(html, "html.parser")
    #source = soup.select('div.AccountActivityPanel')
    source = soup.select('li.show-quick-view')
    deposit_balance = source[0].select('span.balanceValue').text
    cridit_avaliable = source[1].select('strong.TL_NPI_L1')[0].text
    minimum_payment = source[1].select('strong.TL_NPI_L1')[6].text
    text = '''Bank of America\n
    支票账户余额：%s\n
    信用卡剩余额度：%s\n
    最低账单付款：%s\n
    ''' % (deposit_balance, cridit_avaliable, minimum_payment)
    print(text)
    sms.send(16267318573, text)

login('ztang15', '')
get_balance()


