import matplotlib.pyplot as plt
import os
from datetime import date,timedelta
import json
import numpy as np

class ProgressionChart:
    def __init__(self,main_app):
        self.main_app = main_app
        self.json_logger = self.main_app.json_logger
        current_dir = os.getcwd()
        self.log_path = current_dir + "\log"
        
    def generate_today_stats(self):
        stats,labels,success = self.json_logger.grab_stats_from_date(date.today())
        if success:
            colors = ['limegreen','red']
            fig = plt.figure(num="Today's Stats Progression Chart")
            plt.pie(stats[0:2], labels = labels[0:2], wedgeprops=dict(width=0.5),startangle=90,colors=colors)
            plt.title("Today's Stats",fontweight="bold")
            plt.text(-0.35,-0.1,"{:.1f}%".format(round(stats[0]/(stats[0]+stats[1])*100),2),fontsize=24)
            plt.legend()
            plt.show()
            return success
        else:
            self.main_app.generate_msg("Today's log entry does not exist...",1)
            return success

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
            stats,labels,success = self.json_logger.grab_stats_from_date(current_date)
            if success:
                correct_stats_array[weekday_index] = stats[0]
                incorrect_stats_array[weekday_index] = stats[1]
                practice_amount_stats_array[weekday_index] = stats[2]
                date_array[weekday_index] = current_date.strftime("%m/%d/%y") + " (PA: {})".format(practice_amount_stats_array[weekday_index])
                
            else:
                correct_stats_array[weekday_index] = 0
                incorrect_stats_array[weekday_index] = 0
                practice_amount_stats_array[weekday_index] = 0
                date_array[weekday_index] = current_date.strftime("%m/%d/%y") + " (PA: 0)"
            
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
                    date_array,fontsize=6,rotation=30,horizontalalignment='right')
            max_val = max(percent_array)
            plt.ylim(0, max_val+10)

            for weekday_index in range(len(correct_stats_array)):
                plt.text(weekday_index+.1,percent_array[weekday_index]+2,"{}%"
                         .format(percent_array[weekday_index]),
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
                    date_array,fontsize=6,rotation=30,horizontalalignment='right')
            
            max_val_correct = max(correct_stats_array)
            max_val_incorrect = max(incorrect_stats_array)
            max_val = max(max_val_correct,max_val_incorrect)
            plt.ylim(0, max_val+10)
            
            for weekday_index in range(len(correct_stats_array)):
                
                plt.text(weekday_index-0.12,correct_stats_array[weekday_index]+0.1,"{}".format(correct_stats_array[weekday_index]),fontsize=10)
                plt.text(weekday_index+0.27,incorrect_stats_array[weekday_index]+0.1,"{}".format(incorrect_stats_array[weekday_index]),fontsize=10)
                
            plt.plot([], [], ' ', label="PA -> Practice Amount")
            plt.legend()
            plt.title("Current Week's Stats",fontweight="bold")
            plt.show()
            
    def generate_weekly_stats(self,as_percent):
        weekly_stats = self.get_weekly_stats()
        accumulate_weekly_stats = self.get_accumulate_weekly_stats(weekly_stats)
        
        week_array = []
        if as_percent:
            plt.figure(num="Weekly Stats Progression Chart")
            percent_array = [0]*len(accumulate_weekly_stats)
            for week_index in range(len(accumulate_weekly_stats)):
                total = accumulate_weekly_stats[week_index][0]+accumulate_weekly_stats[week_index][1]
                if total == 0:
                    percent_array[week_index] = 0.00
                else:
                    percent_array[week_index] = round((accumulate_weekly_stats[week_index][0]/total)*100,2)
                week_array.append("Week {} (PA:{})".format(week_index+1,accumulate_weekly_stats[week_index][2]))
                
            
            plt.plot(range(len(percent_array)),percent_array)
            plt.plot(range(len(percent_array)),percent_array,'o',color="blue")

            plt.xlabel("Week Number",fontweight ='bold')
            plt.ylabel('Percentage',fontweight ='bold')
            plt.xticks([r for r in range(len(accumulate_weekly_stats))],
                    week_array,fontsize=6,rotation=30,horizontalalignment='right')
            max_val = max(percent_array)
            plt.ylim(0, max_val+10)

            for week_index in range(len(accumulate_weekly_stats)):
                plt.text(week_index+.1,percent_array[week_index]+2,"{}%"
                         .format(percent_array[week_index]),
                         horizontalalignment='center')
                
            plt.plot([], [], ' ', label="PA -> Practice Amount")
            plt.legend()
            plt.title("Weekly Stats in Current Month",fontweight="bold")
            plt.show()
        else:
            bar_width = 0.40
            plt.figure(num="Weekly Stats Progression Chart")
            bar_correct = np.arange(len(accumulate_weekly_stats))
            bar_incorrect = [x + bar_width for x in bar_correct]

            correct_stats_array = []
            incorrect_stats_array = []
            practice_amount_stats_array = []
            for week_index in range(len(accumulate_weekly_stats)):
                correct_stats_array.append(accumulate_weekly_stats[week_index][0])
                incorrect_stats_array.append(accumulate_weekly_stats[week_index][1])
                practice_amount_stats_array.append(accumulate_weekly_stats[week_index][2])
                week_array.append("Week {} (PA:{})".format(week_index+1,accumulate_weekly_stats[week_index][2]))
                

            plt.bar(bar_correct, correct_stats_array, color ='g', width = bar_width,
                edgecolor ='grey', label ='Correct')
            plt.bar(bar_incorrect, incorrect_stats_array, color ='r', width = bar_width,
                edgecolor ='grey', label ='Incorrect')
            
            plt.xlabel("Week Number",fontweight ='bold')
            plt.ylabel('Count',fontweight ='bold')
            plt.xticks([r + bar_width/2 for r in range(len(accumulate_weekly_stats))],
                    week_array,fontsize=6,rotation=30,horizontalalignment='right')
            
            max_val_correct = max(correct_stats_array)
            max_val_incorrect = max(incorrect_stats_array)
            max_val = max(max_val_correct,max_val_incorrect)
            plt.ylim(0, max_val+30)
            
            for week_index in range(len(correct_stats_array)):
                plt.text(week_index-0.12,correct_stats_array[week_index]+0.1,"{}".format(correct_stats_array[week_index]),fontsize=10)
                plt.text(week_index+0.3,incorrect_stats_array[week_index]+0.1,"{}".format(incorrect_stats_array[week_index]),fontsize=10)
                
            plt.plot([], [], ' ', label="PA -> Practice Amount")
            plt.legend()
            plt.title("Weekly Stats in Current Month",fontweight="bold")
            plt.show()

    def get_weekly_stats(self):
        current_month = int(self.get_current_month())
        next_month = current_month + 1
        if next_month == 13:
            next_month = 1
        if current_month == 12 and next_month == 1:
            current_year = int(self.get_current_year())
            other_year = current_year + 1
        else:
            current_year = int(self.get_current_year())
            other_year = current_year

        number_of_days = (date(other_year, next_month, 1) - date(current_year, current_month, 1)).days
        
        weekly_stats = []
        week_stats = []
        week_index = 0
        for day in range(1,number_of_days+1):
            current_date = date(current_year,current_month,day)
            day_number = current_date.weekday()
            stats,labels,success = self.json_logger.grab_stats_from_date(current_date)
            if success:
                week_stats.append((stats[0],stats[1],stats[2]))
            else:
                week_stats.append((0,0,0))
            if day_number == 6 or current_date.day == number_of_days:
                #Used copy to avoid changes in week_stats affecting the appended array in weekly_stats
                weekly_stats.append(week_stats.copy())
                week_stats.clear()
                week_index +=1
        return weekly_stats
    
    def get_accumulate_weekly_stats(self,weekly_stats):
        correct_stats = 0
        incorrect_stats = 0
        practice_amount_stats = 0

        accumulate_weekly_stats = []
        #Okay to do nested for loop because worst case is 35 iterations (5 weeks per month * 7 days per week)
        for week_number in range(len(weekly_stats)):
            for day in range(len(weekly_stats[week_number])):
                correct_stats += weekly_stats[week_number][day][0]
                incorrect_stats += weekly_stats[week_number][day][1]
                practice_amount_stats += weekly_stats[week_number][day][2]
            accumulate_weekly_stats.append((correct_stats,incorrect_stats,practice_amount_stats))
            correct_stats = 0
            incorrect_stats = 0
            practice_amount_stats = 0
        return accumulate_weekly_stats
    
    def get_current_year(self):
        return date.today().strftime("%Y")
    
    def get_current_month(self):
        return date.today().strftime("%m")
    
    def get_month_year(self):
        return date.today().strftime("%m-%y")

    def get_today_date(self):
        return date.today().strftime("%m-%d-%y")
    

if __name__ == "__main__":
    pc = ProgressionChart("hi")
    pc.generate_weekly_stats(True)
