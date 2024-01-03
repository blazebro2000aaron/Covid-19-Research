import csv
import pyautogui
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates

def ask_questions(data=[]):
    raw_data = pyautogui.prompt("Please enter the provinces for covid data(separated by comma)")
    if raw_data != None:
        for item in raw_data.split(","):
            if item.title() == "Newfoundland And Labrador":
                data.append("Newfoundland and Labrador")
            else:
                data.append(item.title())
        return(data)
    else:
        return([])

def filter_data_from_province(province,file_path):
    with open(file_path) as data_file:
        filtered_plot_x_data = []
        filtered_plot_y_data = []
        data_reader = csv.DictReader(data_file)
        notfounderror = False
        for row in data_reader:
            if row["prname"] == province:
                date = row["date"].split("-")
                filtered_plot_x_data.append(datetime(int(date[0]),int(date[1]),int(date[2])))
                filtered_plot_y_data.append(int(row["totalcases"]))
        if filtered_plot_x_data == []:
            pyautogui.alert("The province you asked for was not found, Province: "+province)
            notfounderror = True
        data_file.close()
    if notfounderror:
        return([False])
    else:
        return([filtered_plot_x_data,filtered_plot_y_data])
    
def plot_data(data,provinces):
    for item in provinces:
        current_data = filter_data_from_province(item,data)
        if current_data != [False]:
            plt.plot(time,current_data[1],label=item)

time = filter_data_from_province("Ontario","Covid-19 Research/covid19 records.csv")[0]

plot_data("Covid-19 Research/covid19 records.csv",ask_questions())

date_format = mpl_dates.DateFormatter("%y-%m-%d")

plt.gca().xaxis.set_major_formatter(date_format)

plt.xlabel("Date")

plt.ylabel("Total Cases")

plt.legend()

plt.tick_params(axis='y',which="major",labelsize=7)

plt.show()
