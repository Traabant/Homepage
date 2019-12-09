from myLog import MyLog as log
from compare import Compare
from DbOperations import DbOperations
from myEmail import Email

import requests
from bs4 import BeautifulSoup
import unicodedata
import os
import datetime


class CheckEents():
    """
        downloads two HTML sites, than parse them.
        Parsed data gets compared to the data in DB,
        new data is stored in DB and snd throw the mail
        Script should be run periodically once a day
        method check_events is called automaticly on init
    """
    def __init__(self):
        pass
        self.check_events()
    
    def check_events(self):
        url = 'http://www.msmartinov.cz/stranka71'
        ulr_gallery = "http://www.msmartinov.cz/galerie"
        url_ifno = 'http://www.msmartinov.cz/pro-rodice'

        user = 'siba.robot@seznam.cz'
        password = 'lplojiju321'
        subject = "Nove udalosti MS"
        recipient = [
            "david.siba@gmail.com",
        ]

        # recipient = [
        #     "david.siba@gmail.com",
        # ]


        if os.path.exists('D:/SIBA/'):
            fileDir = 'D:/SIBA/Scripty/Homepage/homepage'
        else:
            fileDir = '/home/Traabant/Homepage/Homepage/homepage'
        db_file_name = fileDir + '/db.sqlite3'

        print("downloading data")
        events = self.find_envents_in_url(url)
        galery_list = self.find_new_galery_in_url(ulr_gallery)
        info = self.find_envents_in_url(url_ifno)

        print("deleting special characters")
        events = self.odstraneni_diakritiky(events)
        galery_list = self.odstraneni_diakritiky(galery_list)
        info = self.odstraneni_diakritiky(info)

        print("comparing")
        compare = Compare(events, db_file_name)
        compare.compare('events')
        events = compare.new_events

        galery_compare = Compare(galery_list, db_file_name)
        galery_compare.compare('gallery')
        galery_list = galery_compare.new_events

        info = Compare(info, db_file_name)
        info.compare('info')
        info_list = info.new_events

        # print(info_list)

        # write_events_to_file(events, eventsFile)
        # write_events_to_file(galery_list, galeryFile)

        if (compare.status is True) or (galery_compare.status is True) or (info.status is True):
            

            body = "Nove udoalosti ve skolce jsou : \n"
            for line in events:
                body += line + '\n'

            body += "\nNove galerie jsou : \n"
            for line in galery_list:
                body += line + '\n'
            
            body += "\nNove Informace pro rodice jsou : \n"
            for line in info_list:
                body += line + '\n'

            db = DbOperations(db_file_name)
            print("writing Events to DB")
            for item in events:
                db.dump_data_to_events_table(item, datetime.datetime.today().strftime("%Y-%m-%d"))
            print("Writing galerry to DB")
            for item in galery_list:
                db.dump_data_to_galerry_table(item, datetime.datetime.today().strftime("%Y-%m-%d"))
            for item in info_list:
                db.dump_data_to_info_table(item, datetime.datetime.today().strftime("%Y-%m-%d"))
            print('Done')

            Email.send_email(user, password, recipient, subject, body)
            print('I would send an email')
            print(body)
            log(body)
            compare.status = False
        else:
            log('No new Events')
            print('No new Events')
    
    def find_envents_in_url(self, url):
        """
        downloads HTML, parse it and returns list with only parsed paragraps
        :param url:
        :return: correct_list
        """
        try:
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, 'html.parser')
            output = soup.find_all('p')
            correct_list = []
            for item in output:
                correct_list.append(item.text)
            return correct_list
        except:
            log("Error while downloading Data from Web")


    def find_new_galery_in_url(self, url):
        try:
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, 'html.parser')
            output = soup.find_all('li')
            list_to_return = []
            for item in output:
                if item.attrs.get("data-cat") == "1":
                    list_to_return.append(item.text[4:-3])
            return list_to_return
        except:
            log("Error while downloading Data from Web")
        


    def odstraneni_diakritiky(self, list):
        """
        delets special characters from Czech language and converts them to ASCI
        :param list:
        :return: list
        """
        list_to_return = []
        for item in list:
            item = unicodedata.normalize('NFKD', item)
            output = ''
            for c in item:
                if not unicodedata.combining(c):
                    output += c
            list_to_return.append(output)
        return list_to_return


if __name__ == "__main__":
    e = CheckEents()