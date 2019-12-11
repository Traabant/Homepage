import datetime
import requests
import json
import os

from credentials import Credentials

class radarData:
    def __init__(self):
        self.today = self.get_today_timestamp()
        self.working_date_stamp = ''


    def get_radar_data(self, given_time, path):
        """
        :param given_time: datetime
        :param path: string, place to save files
        :return: bool if the file was downloaded
        saves individual png files to separate files in path var
        """
        url = self.create_url(given_time)
        
        resp = requests.get(url)
        if resp.status_code == 200:
            downloaded_status = True
            file_path = path + '/' + self.working_date_stamp + '.png'
            # writes picture data from response object into the file
            with open(file_path, 'wb') as fd:
                for chunk in resp.iter_content(chunk_size=128):
                    fd.write(chunk)
        return downloaded_status

    def yesterdays_radar_data(self):
        """
        Downloads and saveves PNG files from CHMI.
        CHmi has png file for every ten minutes
        :return:
        """
        print('downlaoding radar data')
        time = self.get_today_timestamp()
        timedelta_days_to_add = datetime.timedelta(days=-1)    
        timedelta_minutes_to_add = datetime.timedelta(minutes=10)
        time = time + timedelta_days_to_add
        working_date = time

        todays_dir = Credentials().fileDir + '/radar_pictures/' + working_date.strftime('%Y%m%d')
        try:
            os.mkdir(todays_dir)
        except OSError:
            print("Creation of the directory %s failed" % todays_dir)
        else:
            print("Successfully created the directory %s " % todays_dir)
        #todays_dir = '/home/Traabant/Homepage/Homepage/homepage/weather/scripts/radar_pictures'
        index = 0
        while time.date() == working_date.date():
            if self.get_radar_data(time, todays_dir):
                index += 1
            time = time + timedelta_minutes_to_add

        print(f"downloaded {index} files")


    def get_today_timestamp(self):

        today_sting = datetime.datetime.today().strftime('%Y-%m-%d')
        today_sting = today_sting + ' 00:01'
        self.today = datetime.datetime.strptime(today_sting, '%Y-%m-%d %H:%M')   
        return datetime.datetime.strptime(today_sting, '%Y-%m-%d %H:%M') 
        pass 
    

    def create_url(self, given_time):
        # url_example = 'http://portal.chmi.cz/files/portal/docs/meteo/rad/inca-cz/data/czrad-z_max3d/pacz2gmaps3.z_max3d.20190627.0630.0.png'
        url = ''
        downloaded_status = False
        given_curent_minutes = int(given_time.strftime('%M'))
        if given_curent_minutes <= 10:
            given_curent_minutes = '00'
        elif given_curent_minutes <= 20:
            given_curent_minutes = '10'
        elif given_curent_minutes <= 30:
            given_curent_minutes = '20'
        elif given_curent_minutes <= 40:
            given_curent_minutes = '30'
        elif given_curent_minutes <= 50:
            given_curent_minutes = '40'
        elif given_curent_minutes <= 60:
            given_curent_minutes = '50'
        self.working_date_stamp = given_time.strftime('%Y%m%d.%H') + given_curent_minutes
        url = 'http://portal.chmi.cz/files/portal/docs/meteo/rad/inca-cz/data/czrad-z_max3d/pacz2gmaps3.z_max3d.' + \
            self.working_date_stamp + '.0.png'
        
        return url
    
    def get_last_x_images(self):
        ulr_list = []
        num_of_imgs = 5
        timedelta_minutes_to_sub = datetime.timedelta(minutes=10)
        now = datetime.datetime.utcnow()
        working_time = now - timedelta_minutes_to_sub
        num_cur_img = 0
        while (num_cur_img < num_of_imgs):
            ulr_list.append(self.create_url(working_time))
            working_time = working_time - timedelta_minutes_to_sub
            num_cur_img += 1
        
        ulr_dict = {
            "0": ulr_list[0],
            "1": ulr_list[1],
            "2": ulr_list[2],
            "3": ulr_list[3],
            "4": ulr_list[4],
        }

        json.dumps(ulr_dict)
        # print(ulr_list)
        data_to_return ={
            'time': datetime.datetime.strftime(now, "%Y%m%d %H:%M"),
            'data': ulr_dict
        }            
        return data_to_return

if __name__ == "__main__":
    r = radarData()
    r.get_last_x_images()
    pass

    
        
