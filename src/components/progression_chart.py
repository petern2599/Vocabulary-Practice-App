import matplotlib.pyplot as plt
import os
from datetime import date,timedelta
import json

class ProgressionChart:
    def __init__(self,main_app):
        self.main_app = main_app
        current_dir = os.getcwd()
        self.log_path = current_dir + "\log"
        
    def generate_today_stats(self):
        stats,labels,success = self.grab_stats_from_date(date.today())
        if success:
            colors = ['limegreen','red']
            fig = plt.figure(1000)
            plt.pie(stats[0:2], labels = labels[0:2], wedgeprops=dict(width=0.5),startangle=90,colors=colors)
            plt.title("Today's Stats",)
            plt.text(-0.3,-0.1,"{}%".format(stats[0]/(stats[0]+stats[1])*100),fontsize=24)
            plt.show()
        else:
            self.main_app.generate_msg("Today's log entry does not exist...",1)

    def generate_week_stats(self):
        stats_array = [0]*7
        day_number = date.today().weekday()
        print(day_number)
        
        current_date = date.today()

        #Subtract days to get to date on a Monday
        current_date -= timedelta(days=day_number)
        print(current_date)
            
        for weekday_index in range(len(stats_array)):
            stats,labels,success = self.grab_stats_from_date(current_date)
            if success:
                stats_array[weekday_index] = stats
            else:
                stats_array[weekday_index] = stats
            
            current_date += timedelta(days=1)

        
            

    def get_current_year(self):
        return date.today().strftime("%Y")
    
    def get_month_year(self):
        return date.today().strftime("%m-%y")

    def get_today_date(self):
        return date.today().strftime("%m-%d-%y")
    
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
            
                    stats = [correct_stat,incorrect_stat,practice_amount_stat]
                    labels = ['Correct','Incorrect','practice_amount_stat']
                else:
                    return [],[],False
            return stats,labels,True
        else:
            return [],[],False

if __name__ == "__main__":
    pc = ProgressionChart("hi")
    pc.generate_week_stats()
