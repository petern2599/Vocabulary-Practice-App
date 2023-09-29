import matplotlib.pyplot as plt
import os
from datetime import date,timedelta
import json
import numpy as np

class ProgressionChart:
    def __init__(self,main_app):
        self.main_app = main_app
        current_dir = os.getcwd()
        self.log_path = current_dir + "\log"
        
    def generate_today_stats(self):
        stats,labels,success = self.grab_stats_from_date(date.today())
        if success:
            colors = ['limegreen','red']
            fig = plt.figure(num="Today's Stats Progression Chart")
            plt.pie(stats[0:2], labels = labels[0:2], wedgeprops=dict(width=0.5),startangle=90,colors=colors)
            plt.title("Today's Stats",fontweight="bold")
            plt.text(-0.3,-0.1,"{}%".format(stats[0]/(stats[0]+stats[1])*100),fontsize=24)
            plt.show()
        else:
            self.main_app.generate_msg("Today's log entry does not exist...",1)

    def generate_week_stats(self, as_percent):
        correct_stats_array = [0]*7
        incorrect_stats_array = [0]*7
        practice_amount_stats_array = [0]*7
        date_array = [0]*7

        day_number = date.today().weekday()
        current_date = date.today()
        #Subtract days to get to date on a Monday
        current_date -= timedelta(days=day_number)
            
        for weekday_index in range(len(correct_stats_array)):
            stats,labels,success = self.grab_stats_from_date(current_date)
            if success:
                correct_stats_array[weekday_index] = stats[0]
                incorrect_stats_array[weekday_index] = stats[1]
                practice_amount_stats_array[weekday_index] = stats[2]
                date_array[weekday_index] = current_date.strftime("%m/%d/%y")
                
            else:
                correct_stats_array[weekday_index] = 0
                incorrect_stats_array[weekday_index] = 0
                practice_amount_stats_array[weekday_index] = 0
                date_array[weekday_index] = current_date.strftime("%m/%d/%y")
            
            current_date += timedelta(days=1)

        if as_percent:
            plt.figure(num="Week's Stats Progression Chart")
            percent_array = [0]*7
            for weekday_index in range(len(correct_stats_array)):
                total = correct_stats_array[weekday_index]+incorrect_stats_array[weekday_index]
                if total == 0:
                    percent_array[weekday_index] = 0.00
                else:
                    percent_array[weekday_index] = round((correct_stats_array[weekday_index]/total)*100,2)

            plt.plot(range(len(percent_array)),percent_array)
            plt.plot(range(len(percent_array)),percent_array,'o',color="blue")

            plt.xlabel("Weekday",fontweight ='bold')
            plt.ylabel('Percentage',fontweight ='bold')
            plt.xticks([r for r in range(len(correct_stats_array))],
                    date_array,fontsize=8)
            max_val = max(percent_array)
            plt.ylim(0, max_val+10)

            for weekday_index in range(len(correct_stats_array)):
                plt.text(weekday_index+.1,percent_array[weekday_index]+2,"PA: {} \n {}%"
                         .format(practice_amount_stats_array[weekday_index],percent_array[weekday_index]),
                         horizontalalignment='center')
                
            plt.plot([], [], ' ', label="PA -> Practice Amount")
            plt.legend()
            plt.title("Current Week's Stats",fontweight="bold")
            plt.show()
        else:
            bar_width = 0.40
            plt.figure(num="Week's Stats Progression Chart")
            bar_correct = np.arange(len(correct_stats_array))
            bar_incorrect = [x + bar_width for x in bar_correct]

            plt.bar(bar_correct, correct_stats_array, color ='g', width = bar_width,
                edgecolor ='grey', label ='Correct')
            plt.bar(bar_incorrect, incorrect_stats_array, color ='r', width = bar_width,
                edgecolor ='grey', label ='Incorrect')
            
            plt.xlabel("Weekday",fontweight ='bold')
            plt.ylabel('Count',fontweight ='bold')
            plt.xticks([r + bar_width/2 for r in range(len(correct_stats_array))],
                    date_array,fontsize=8)
            
            max_val_correct = max(correct_stats_array)
            max_val_incorrect = max(incorrect_stats_array)
            max_val = max(max_val_correct,max_val_incorrect)
            plt.ylim(0, max_val+10)
            
            for weekday_index in range(len(correct_stats_array)):
                max_value = max(correct_stats_array[weekday_index],incorrect_stats_array[weekday_index])
                plt.text(weekday_index+.1,max_value+5,"PA: {}".format(practice_amount_stats_array[weekday_index])
                        ,horizontalalignment='center')
                
                plt.text(weekday_index-0.12,correct_stats_array[weekday_index]+0.1,"{}".format(correct_stats_array[weekday_index]),fontsize=10)
                plt.text(weekday_index+0.27,incorrect_stats_array[weekday_index]+0.1,"{}".format(incorrect_stats_array[weekday_index]),fontsize=10)
                
            plt.plot([], [], ' ', label="PA -> Practice Amount")
            plt.legend()
            plt.title("Current Week's Stats",fontweight="bold")
            plt.show()
            
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
    pc.generate_week_stats(False)
