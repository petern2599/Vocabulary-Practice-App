import json
import os
from datetime import date,timedelta

class JSONLogger():
    def __init__(self):
        current_dir = os.getcwd()
        self.log_path = current_dir + "\log"
        self.check_log_directory_exists()
        year_path = self.check_current_year_log_folder_exists()
        json_path = self.check_current_month_log_file_exists(year_path)
        self.is_streak_changed = False
    
    def check_log_directory_exists(self):
        if os.path.exists(self.log_path):
            pass
        else:
            print("Creating Log directory at {}...".format(self.log_path))
            os.mkdir(self.log_path)

    def check_current_year_log_folder_exists(self):
        year = date.today().strftime("%Y")
        new_path = self.log_path + "\{}".format(year)
        if os.path.exists(new_path):
            return new_path
        else:
            print("Creating Log folder for this year ({})...".format(year))
            os.mkdir(new_path)
            return new_path

    def check_current_month_log_file_exists(self,path):
        month_year = date.today().strftime("%m-%y")
        new_path = path + "\{}.json".format(month_year)
        if os.path.exists(new_path):
            return new_path
        else:
            print("Creating Log file for this month ({})...".format(month_year))
            day = date.today()
            day -= timedelta(days=1)
            streak = self.check_streak(day)
            data = {"{}".format(date.today().strftime("%m-%d-%y")):{"correct":0, "incorrect":0, "practice amount":0, "streak":streak}}
            with open(new_path, 'w') as file:
                json.dump(data,file,indent=4)
            
            return new_path
        
    def check_streak(self,date_to_check):
        self.check_log_directory_exists()
        year_path = self.check_current_year_log_folder_exists()
        month_year = date_to_check.strftime("%m-%y")
        json_path = year_path + "\{}.json".format(month_year)

        with open(json_path,'r+') as file:
            file_data = json.load(file)
            day = date_to_check.strftime("%m-%d-%y")
            if day in file_data:
                streak = file_data[day]["streak"]
                return streak
            else:
                #If log entry for previous day doesn't exists, set streak to 0
                return 0
            
    def append_daily_stats(self,correct,incorrect):
        day = date.today().strftime("%m-%d-%y")
        self.check_log_directory_exists()
        year_path = self.check_current_year_log_folder_exists()
        json_path = self.check_current_month_log_file_exists(year_path)

        with open(json_path,'r+') as file:
            file_data = json.load(file)
            if day in file_data:
                correct_stat = file_data[day]["correct"]
                incorrect_stat = file_data[day]["incorrect"]
                practice_amount_stat = file_data[day]["practice amount"]
                streak_stat = file_data[day]["streak"]
                streak_change_check = self.check_streak_changed_before()
                if streak_change_check:
                    file_data[day]= {"correct":correct_stat + correct, "incorrect":incorrect_stat+incorrect, "practice amount": practice_amount_stat+1,"streak":streak_stat}
                else:
                    file_data[day]= {"correct":correct_stat + correct, "incorrect":incorrect_stat+incorrect, "practice amount": practice_amount_stat+1,"streak":streak_stat+1}
                file.seek(0)
                json.dump(file_data,file,indent=4)
            else:
                print("Adding new entry in log file...")
                file_data[day] = {"correct":correct, "incorrect":incorrect,"practice amount":1}
                file.seek(0)
                json.dump(file_data,file,indent=4)

    def check_streak_changed_before(self):
        day = date.today()
        today_streak = self.check_streak(day)
        #If today_streak = 0, then new streak have started 
        if today_streak == 0:
            return False
        day -= timedelta(days=1)
        yesterday_streak = self.check_streak(day)
        #If today and yesterday streak are not equal then streak has changed
        if today_streak != yesterday_streak:
            return True
        else:
            return False
        