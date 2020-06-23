from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import chromedriver_binary
import csv
from selenium.webdriver.support.ui import Select


class BookBot():
    def __init__(self):
        self.driver = webdriver.Chrome()
    def login(self,login,password):

        try:
            self.driver.get('https://yoyaku.harp.lg.jp/resident/Login.aspx')
            self.driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtRiyoushaID"]').send_keys(login)
            self.driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtPassword"]').send_keys(password)
            sleep(0.5)
            self.driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_btnLogin"]').click()

            try:
                self.driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_btnReset"]').click()
                self.driver.find_element_by_xpath('// *[ @ id = "ctl00_ContentPlaceHolder1_btnYoyakuService"]').click()
                self.login(login,password)
            except Exception:
                pass
        except Exception:
            self.login(login,password)


    def book(self,school,day,court_no):
        self.driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_btnMenuShinseiSrch"]').click()
        sleep(0.5)
        bunri_element = self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$ShinseiKumiawaseInp1$drpPurposeBunrui")
        bunri_select_element = Select(bunri_element)
        bunri_select_element.select_by_value("01") #学校開放屋外
        mokuteki_element = self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$ShinseiKumiawaseInp1$drpPurpose")
        mokuteki_select_element = Select(mokuteki_element)
        mokuteki_select_element.select_by_value("011") #屋外テニス（硬式）
        self.driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_ShinseiKumiawaseInp1_btnSearch"]').click()
        #ページをスキップ
        page_skip = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_SelectSstList1_drplstKensu")
        page_skip_select = Select(page_skip)
        page_skip_select.select_by_value("50")
        if school > 50:
            self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_SelectSstList1_imgbtnNxtPageTop").click()
            if school >100:
                self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_SelectSstList1_imgbtnNxtPageTop").click()
        # 学校を選択する
        self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_SelectSstList1_SelectSstRow{}_lnkSelect".format(school)).click()
        self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lnkBtnNxtMonth").click()
        self.driver.find_element_by_xpath("//a[@title='{}']".format(day)).click()
        #ｺｺaharfｼｶﾅｲﾉﾃﾞ注意

        self.driver.execute_script("javascript:__doPostBack('ctl00$ContentPlaceHolder1$grdStbNaiyoList','{}')".format(court_no))
        # 時間をラジオボタンで選択(18時から２０時まで)
        self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_JikantaiSel11").click()
        self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_JikantaiSel12").click()
        self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnShinseiCnf").click()
    def terminate_apply(self):
        #確定
        self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnShinsei").click()
        #ログアウト
        self.driver.find_element_by_id("ctl00_btnLogout").click()





    def complete(self,school,date,start=1,court_no='Select$0'):
        "-----------------------------変更するデータ--------------------------------------"
        read_file_name = "./read.csv"  # 読み込みファイル
        write_file_name = "result.csv"  # 書き込みファイル
        "-----------------------------変更するデータ--------------------------------------"
        read_file = open(read_file_name, "r", encoding="utf-8")
        line_number = 0
        print('学校:',school,'日付:',date,'start：',start)
        for line in read_file:
            # if line_number==2: break      #テスト用
            line_number += 1
            # if line_number == 1 :
            #   continue
            if line_number <= start:
                continue
            items = line.split(",")
            login = (items[1])
            password = (items[2])
            self.login(login,password)
            self.book(school,date,court_no)
            # sleep(20)
            self.terminate_apply()

            print('line_number:',items[0],'id:',login)

self = BookBot()

self.complete(16,
              '7月28日',
              start=1,
              court_no='Select$0'
              )
# Cコートなら'Select$0'
# Dコートなら'Select$1'


#学校開放の夕方練習夏バージョン　ボットを使用している。
#１０みかほ公園
#１６月寒
#２５農試公園
#２７手稲稲積公園
#12　山鼻中学校
# 新琴似中
#19　新川中学校
# 八軒小学校
#103 八軒中学校　
#92　琴似小
#5 ﾄﾝﾃﾞﾝ西公園