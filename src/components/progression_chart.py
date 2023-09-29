import matplotlib.pyplot as plt
import os
from datetime import date,timedelta
import json

class ProgressionChart:
    def __init__(self):
        current_dir = os.getcwd()
        self.log_path = current_dir + "\log"
        
    def generate_today_stats(self):
        log_dir = self.log_path + "\{}".format(self.get_current_year()) + '\{}.json'.format(self.get_month_year())
        with open(log_dir,'r+') as file:
            file_data = json.load(file)
            day = date.today().strftime("%m-%d-%y")
            if day in file_data:
                correct_stat = file_data[day]['correct']
                incorrect_stat = file_data[day]['incorrect']
        
                stats = [correct_stat,incorrect_stat]
                labels = ['Correct','Incorrect']
                colors = ['limegreen','red']
                plt.pie(stats, labels = labels, wedgeprops=dict(width=0.5),startangle=90,colors=colors)
                plt.title("Today's Stats",)
                plt.text(-0.3,-0.1,"{}%".format(correct_stat/(correct_stat+incorrect_stat)*100),fontsize=24)
                plt.show()

    def get_current_year(self):
        return date.today().strftime("%Y")
    
    def get_month_year(self):
        return date.today().strftime("%m-%y")

    def get_today_date(self):
        return date.today().strftime("%m-%d-%y")

    
