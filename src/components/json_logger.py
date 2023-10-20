import json
import os
from datetime import date,timedelta

class JSONLogger():
    def __init__(self):
        self.incorrect_dictionary = {}
        current_dir = os.getcwd()
        self.log_path = current_dir + "\log"
        self.check_log_directory_exists()
        year_path = self.check_current_year_log_folder_exists()
        json_path = self.check_current_month_log_file_exists(year_path)
        self.is_streak_changed = False
        
        self.initialize_incorrect_dictionary(json_path)
    
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
            data = {"{}".format(date.today().strftime("%m-%d-%y")):{"correct":0, "incorrect":0, "practice amount":0, "streak":streak, "incorrect terms": self.incorrect_dictionary}}
            with open(new_path, 'w') as file:
                json.dump(data,file,indent=4)
            
            return new_path
        
    def check_streak(self,date_to_check):
        self.check_log_directory_exists()
        year_path = self.check_current_year_log_folder_exists()
        month_year = date_to_check.strftime("%m-%y")
        json_path = year_path + "\{}.json".format(month_year)
        if os.path.exists(json_path):
            with open(json_path,'r+') as file:
                file_data = json.load(file)
                day = date_to_check.strftime("%m-%d-%y")
                if day in file_data:
                    streak = file_data[day]["streak"]
                    return streak
                else:
                    #If log entry for previous day doesn't exists, set streak to 0
                    return 0
        else:
            return 0
          
    def check_last_practice_date_log(self,date_to_check):
        self.check_log_directory_exists()
        year_path = self.check_current_year_log_folder_exists()
        month_year = date_to_check.strftime("%m-%y")
        json_path = year_path + "\{}.json".format(month_year)
        if os.path.exists(json_path):
            with open(json_path,'r+') as file:
                file_data = json.load(file)
                day = date_to_check.strftime("%m-%d-%y")
                practice_amount_stat = self.check_practice_on_date(date_to_check,file_data)
                if day in file_data and len(file_data) >= 1 and practice_amount_stat > 0:
                    return True
                return False
        else:
            return False
    
    def check_practice_on_date(self,date_to_check,file_data):
        day = date_to_check.strftime("%m-%d-%y")
        if day in file_data:
            practice_amount_stat = file_data[day]["practice amount"]
            return practice_amount_stat
        else:
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
                    file_data[day]= {"correct":correct_stat + correct, 
                                     "incorrect":incorrect_stat+incorrect, 
                                     "practice amount": practice_amount_stat+1,
                                     "streak":streak_stat,
                                     "incorrect terms":self.incorrect_dictionary}
                else:
                    file_data[day]= {"correct":correct_stat + correct, 
                                     "incorrect":incorrect_stat+incorrect, 
                                     "practice amount": practice_amount_stat+1,
                                     "streak":streak_stat+1,
                                     "incorrect terms":self.incorrect_dictionary}
                file.seek(0)
                json.dump(file_data,file,indent=4)
            else:
                yesterday = date.today()
                yesterday -= timedelta(days=1)
                streak_stat = self.check_streak(yesterday)
                print("Adding new entry in log file...")
                file_data[day] = {"correct":correct, 
                                  "incorrect":incorrect,
                                  "practice amount":1,
                                  "streak":streak_stat + 1, 
                                  "incorrect terms": self.incorrect_dictionary}
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
        
    def add_index_to_dictionary(self,index):
        if str(index) in self.incorrect_dictionary.keys():
            self.incorrect_dictionary[str(index)] += 1
        else:
            self.incorrect_dictionary[str(index)] = 1
    
    def initialize_incorrect_dictionary(self,json_path):
        day = date.today().strftime("%m-%d-%y")
        if os.path.exists(json_path):
            with open(json_path,"r+") as file:
                file_data = json.load(file)
                if day in file_data:
                    self.incorrect_dictionary = file_data[day]["incorrect terms"]
                else:
                    self.incorrect_dictionary = {}
        else:
            self.incorrect_dictionary = {}
    
    def remove_index_in_dictionary(self,index):
        if str(index) in self.incorrect_dictionary.keys():
            if self.incorrect_dictionary[str(index)] == 1:
                del self.incorrect_dictionary[str(index)]
            else:
                self.incorrect_dictionary[str(index)] -= 1
                
    def grab_today_incorrect_indexes(self):
        year_path = self.check_current_year_log_folder_exists()
        today = date.today()
        month_year = today.strftime("%m-%y")
        json_path = year_path + "\{}.json".format(month_year)
        if os.path.exists(json_path):
            with open(json_path,'r+') as file:
                file_data = json.load(file)
                day = today.strftime("%m-%d-%y")
                if day in file_data:
                    indexes = file_data[day]["incorrect terms"]
                    return indexes
                
    def grab_week_incorrect_indexes(self):
        date_array = [0]*7
        day_number = date.today().weekday()
        current_date = date.today()
        #Subtract days to get to date on a Monday
        current_date -= timedelta(days=day_number)
        accumulate_incorrect_dictionary = {}
        for weekday_index in range(7):
            stats,labels,success = self.grab_stats_from_date(current_date)
            if success:
                for index,frequency in stats[4].items():
                    if index in accumulate_incorrect_dictionary.keys():
                        accumulate_incorrect_dictionary[index] += frequency
                    else:
                        accumulate_incorrect_dictionary[index] = frequency
            current_date += timedelta(days=1)

        return accumulate_incorrect_dictionary
        
    def get_current_year(self):
        return date.today().strftime("%Y")
    
    def get_current_month(self):
        return date.today().strftime("%m")
        
    def grab_stats_from_date(self,check_date):
        month_year = check_date.strftime("%m-%y")
        log_dir = self.log_path + "\{}".format(check_date.year) + '\{}.json'.format(month_year)
        if os.path.exists(log_dir):
            with open(log_dir,'r+') as file:
                file_data = json.load(file)
                date_str = check_date.strftime("%m-%d-%y")
                if date_str in file_data:
                    correct_stat = file_data[date_str]['correct']
                    incorrect_stat = file_data[date_str]['incorrect']
                    practice_amount_stat = file_data[date_str]['practice amount']
                    streak_stat = file_data[date_str]['streak']
                    incorrect_terms_stat = file_data[date_str]['incorrect terms']
            
                    stats = [correct_stat,incorrect_stat,practice_amount_stat, streak_stat,incorrect_terms_stat]
                    labels = ['Correct','Incorrect','Practice Amount','Streak','Incorrect Terms']
                else:
                    return [],[],False
            return stats,labels,True
        else:
            return [],[],False
        
        

