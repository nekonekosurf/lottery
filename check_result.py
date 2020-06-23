from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import chromedriver_binary
import csv


class ResultBot():

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



    def get_result(self,writer,login,target):

        bsObj = BeautifulSoup(self.driver.page_source, "html.parser")
        table = bsObj.findAll("table", {"class": "log-box"})[0]
        rows = table.findAll("tr")
        # writer = csv.writer(writer)
        for row in rows:
            csvRow = []
            csvRow.append(login)

            for cell in row.findAll(['td', 'th']):
                csvRow.append(cell.get_text())
            # print(csvRow)
            if csvRow[2] == target:
                # print(login)
                writer.writerow(csvRow)
        return  writer

    def complete(self):
        "-----------------------------変更するデータ--------------------------------------"
        read_file_name = "./read.csv"  # 読み込みファイル
        write_file_name = "./result.csv"  # 書き込みファイル
        target = "\n当選"
        "-----------------------------変更するデータ--------------------------------------"
        read_file = open(read_file_name, "r", encoding="utf-8")
        write_file = open(write_file_name, 'wt', newline='', encoding='utf-8')
        line_number = 0
        writer = csv.writer(write_file)

        for line in read_file:
            line_number += 1
            # if line_number == 1 :
            #   continue
            if line_number <= 1:
                continue
            items = line.split(",")
            login = (items[1])
            password = (items[2])
            self.login(login,password)
            writer = self.get_result(writer,login,target)
            print('line_number:',line_number,'id:',login)


        write_file.close()
        read_file.close()

self = ResultBot()
self.complete()