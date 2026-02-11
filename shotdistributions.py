"""
Enkidu Bazua​, Pranav Bollineni​, Sal Gagliardo​, Sophia Hughes​, Sebastian Romero​,
    and Dylan Tu​
DS2001 Project - File 3
April 7, 2025
This program reads a csv file with data from the NBA, and analyzes the 3-point 
    shot attempt distribution across three court zones (Left Corner, 
    Right Corner, and Above the Break). It calculates the average number of 
    3-point attempts from each zone for three time periods, and visualizes the 
    distribution using pie charts. 
"""


# importing matplotlib and csv reader to plot out our data, and read our 
# dataset.
import matplotlib.pyplot as plt
import csv

# creating a function which will allow us to read our database, and extract
# the columns that we need,
# putting all this info into a dictionary with lists within.
def read_file(filename, start_year, end_year):
    game_data = {"Left Corner FGA": [], "Right Corner FGA": [], 
                 "Above the Break FGA": []}
    with open(filename, 'r' ) as infile:
        reader = csv.DictReader(infile)
        
        # for each year, we convert the string from each row 
        # into a float point, where we can use it for a numerical conditional.
        for row in reader:
                year = float(row["\ufeffYear"])
                
                # year conditional, extracting data from the start
                # and end year specified.
                if year >= start_year and year < end_year:
                    game_data["Left Corner FGA"].append(float
                                                (row["Left Corner 3 FGA"]))
                    game_data["Right Corner FGA"].append(float
                                                (row["Right Corner 3 FGA"]))
                    game_data["Above the Break FGA"].append(float
                                                (row["Above the Break 3 FGA"]))
    
    # returns game_data dictionary
    return game_data

# creating functions to count up three point shots from respective position,
# and then divide the total by the legnth of the list to get an average.
def left_count_up(dataset):
    fga_list = dataset["Left Corner FGA"] 
    left_position_avg = sum(fga_list) / len(fga_list)
    return left_position_avg
    
def right_count_up(dataset):
    fga_list = dataset["Right Corner FGA"]
    right_position_avg = sum(fga_list) / len(fga_list)

    return right_position_avg

def above_break_count_up(dataset):
    fga_list = dataset["Above the Break FGA"]
    above_position_avg = sum(fga_list) / len(fga_list)
    return above_position_avg
    
# creating a function to plot out all of our lists into a pie chart, with 
# custom labels and colors.
def plot_pie(dataset, title):
    labels = ["Left Corner", "Right Corner", "Above the Break"]
    sizes = [left_count_up(dataset), right_count_up(dataset), 
             above_break_count_up(dataset)]
    colors = ["tomato", "cadetblue", "lightsteelblue"]

# setting up pie chart and adjusting proportions to make sure it's not hard 
# for viewers to understand
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', 
            startangle=140)
    plt.title(title)
    plt.axis('equal') 
    plt.show()

# main function where we plot everything and execute the functions.  
def main():
    plot_pie(read_file("regular_season_3pt_zones.csv", 2015, 2026), 
             "Average 3PT Attempt Distribution by Zone, 2015-2025")
    
    plot_pie(read_file("regular_season_3pt_zones.csv", 2005, 2015), 
             "Average 3PT Attempt Distribution by Zone, 2005-2015")

    plot_pie(read_file("regular_season_3pt_zones.csv", 1997, 2005), 
             "Average 3PT Attempt Distribution by Zone, 1997-2005")
main()
