"""
Enkidu Bazua​, Pranav Bollineni​, Sal Gagliardo​, Sophia Hughes​, Sebastian Romero​,
    and Dylan Tu​
DS2001 Project - File 5
April 7, 2025
This program reads csv files with data from the NBA for both the 
    regular season and postseason 3-point shot statistics from different zones. 
    It processes and averages the data, then creates bar charts to visualize 
    team 3-point shooting performance during the regular season and the 
    difference in 3-point makes between champions and runner-ups 
    during the postseason.

"""
import matplotlib.pyplot as plt

def read_file_regularseason(regularseason_filename):
    '''
    The function reads a csv file on regular season statistics, converts
    any data to its necessary form, and returns a dictionary with the
    data being sums of all the averages

    Parameters
    ----------
    regularseason_filename : string
        the name of the csv file that will be read.

    Returns
    -------
    team_numbers : dictionary
        a dictionary with team names as key, and its value being another
        dictionary with keys being the name of the statistic and value
        being the numbers.

    '''
    # intializing the empty list
    team_numbers = {}
    
    # opeining and reading the file, skipping header
    with open(regularseason_filename, "r") as file:
        file.readline()
        
        # for each line in the file, stip at whitespace, split, and
        # convert to necessary data
        for line in file:
            line = line.strip().split(",")
            name = line[1]
            l_corner_3m = float(line[2])
            l_corner_3a = float(line[3])
            r_corner_3m = float(line[5])
            r_corner_3a = float(line[6])
            above_break_3m = float(line[8])
            above_break_3a = float(line[9])
            
            # calculating the totals for made and attempted 3 pointers
            made3_total = l_corner_3m + r_corner_3m + above_break_3m
            attempt3_total = l_corner_3a + r_corner_3a + above_break_3a
            
            # if team is not in dictionary, add it and add the dictionary
            # model for its value
            if name not in team_numbers:
                team_numbers[name] = {
                    "3-Pointers Made": made3_total,
                    "3-Pointers Attempted": attempt3_total,
                    "Number of Seasons": 1}
                
            # if in the dictionary, add the already existing value
            # by the value of the line
            else:
                team_numbers[name]["3-Pointers Made"] += made3_total
                team_numbers[name]["3-Pointers Attempted"] += attempt3_total
                team_numbers[name]["Number of Seasons"] += 1

    return team_numbers

def season_averages(regularseason_data):
    '''
    This function takes a dictionary of the averages summed, and computes
    the per game averages from this time period.

    Parameters
    ----------
    regularseason_data : dictionary
        dictionary returned from reading the file.

    Returns
    -------
    team_averages : dictionary
        cleaned verion of regularseason_data.

    '''
    
    # empty dictionary that will hold values
    team_averages = {}
    
    # for each team in the data, calculate their per game avg for makes,
    # attempts, and shooting
    for team in regularseason_data:
        makes = (regularseason_data[team]["3-Pointers Made"] /
                              regularseason_data[team]["Number of Seasons"])
        attempts = (regularseason_data[team]["3-Pointers Attempted"] /
                            regularseason_data[team]["Number of Seasons"])
        shooting = (makes / attempts)
        
        # add the keys and values into a dictionary (for values), that 
        # corresponds to the team key
        team_averages[team] = {}
        team_averages[team]["Avg 3PM"] = round(makes, 2)
        team_averages[team]["Avg 3PA"] =  round(attempts, 2)
        team_averages[team]["Avg 3PT-Shooting"] = round(shooting, 2)
        
        
    return team_averages


def visualize_regularseason(clean_data, figure_name):
    '''
    This function renders a bar-chart visualization with each bar's
    height corresponding to the avg number of made 3-point shots per team,
    and lists the efficieny above the bar

    Parameters
    ----------
    clean_data : dictionary
        a dictionary of the cleaned data.
    figure_name : string
        the name that the png will be saved as.

    Returns
    -------
    Renders a bar-chart.

    '''
    
    # Setting the title and axii
    plt.figure(figsize=(20, 10))
    plt.title("Game Average 3-Pointers Made During Regular Season: 1997-2025",
              fontsize = 36)
    plt.xlabel("Team", fontsize = 24)
    plt.ylabel("Average 3-Pointers Made\nEfficieny Above Bar", fontsize = 24)

    # Lists to store team names, their corresponding 3-pointer averages, and shooting efficiencies
    teams = []
    avg_3pm_values = []
    efficiencies = []

    # Loop through each team in the regular season data
    for team in clean_data:
        
        # Extract the average 3-pointers made for that team
        avg_3pm = clean_data[team]["Avg 3PM"] 
        avg_shooting = clean_data[team]["Avg 3PT-Shooting"] 
        
        # Calculate shooting efficiency as a percentage 
        efficiency = round(avg_shooting * 100, 2)  
        
        # Append values to the lists
        teams.append(team)
        avg_3pm_values.append(avg_3pm)
        efficiencies.append(efficiency)
    
    # Create a bar chart with teams on the x-axis and average 3-pointers 
    # made on the y-axis
    plt.bar(teams, avg_3pm_values, color='peru', alpha = 0.6, width = 0.8)
    plt.xticks(rotation = 45, ha="right", fontsize = 16)
    plt.yticks(fontsize = 16)

    # Add shooting efficiency text above each bar
    for i in range(len(teams)):
        plt.text(i, avg_3pm_values[i] + 0.1, f'{efficiencies[i]}%', 
                 ha ='center', verticalalignment ='bottom', color = 'black', 
                 fontsize = 12)

    # Display the plot
    plt.savefig(figure_name, dpi = 500)
    plt.show()
    
def read_file_postseason(postseason_filename):
    '''
    This function takes a filename as an argument, opens and reads the file,
    converts data when neccessary, and returns a dictionary.

    Parameters
    ----------
    postseason_filename : string
        name of the file that will be opened.

    Returns
    -------
    post_numbers : dictionary
        a dictionary that lists the statistics for the champion and 
        runner-up during the posts season for each year.

    '''
    # intialize the empty dictionary
    post_numbers = {}
    
    # open the file, read header, and split/strip 
    with open(postseason_filename, "r") as file:
        file.readline()  
        for line in file:
            line = line.strip().split(",")
            
            # Convert years to integers
            year = int(line[0])
            
            # Initialize the year in the dictionary if not already present
            if year not in post_numbers:
                post_numbers[year] = {}

            # if 1 is listed (Champion), add the following information
            # to the following keys (calculating the total 3PM, 3PA, 3P%)
            if line[1] == '1':  
                champion_name = line[2]
                post_numbers[year]["Champion"] = champion_name
                post_numbers[year]["Champion 3PM"] = round(float(line[3]) + 
                                        float(line[6]) + float(line[9]), 2)
                post_numbers[year]["Champion 3PA"] = round(float(line[4]) + 
                                        float(line[7]) + float(line[10]), 2)
          
            # if 0 (runner-up) add the following information to the following
           # keys (calculation the total 3PM, 3PA, 3P%)
            else:  # Runner-Up
                runner_up_name = line[2]
                post_numbers[year]["Runner-Up"] = runner_up_name
                post_numbers[year]["Runner-Up 3PM"] = round(float(line[3]) + 
                                        float(line[6]) + float(line[9]), 2)
                post_numbers[year]["Runner-Up 3PA"] = round(float(line[4]) + 
                                        float(line[7]) + float(line[10]), 2)
    return post_numbers


def visualize_postseason(postseason_data, figure_name):
    '''
    This function makes a bar chart of the difference of three pointers 
    by the Championship winning team vs the runner-up team. The champion
    is green, and the runner-up is red

    Parameters
    ----------
    postseason_data : dictionary
        a dictionary returned from reading the postseason data.
    figure_name : string
        the name that the figure will be saved as.

    Returns
    -------
    Renders a bar-chart visualization.

    '''
    # Intialize empty lists
    years = []  
    champion_3pm = []  
    runnerup_3pm = [] 
    champ_diff = []
    
    # for each year in the data, convert year to string, and append
    # the chamipon 3PM with the Runner-Up 3PM
    for year in postseason_data:
        years.append(str(year))  
        champion_3pm.append(postseason_data[year]["Champion 3PM"])
        runnerup_3pm.append(postseason_data[year]["Runner-Up 3PM"])
    
    # for each value at a specific index, calculate the Champion 3PM mins
    # the Runner-Up 3PM
    for i in range(len(champion_3pm)):
        diff = abs(champion_3pm[i] - runnerup_3pm[i])  
        champ_diff.append(diff)
    
    # Reverse the lists so the bars go from 1979 to 2024
    years = years[::-1]
    champ_diff = champ_diff[::-1]
    
    # intialize the colors we want
    colors = ['green' if champion_3pm[i] >= runnerup_3pm[i] else 
              'red' for i in range(len(champion_3pm))]
    
    # make the figure zie
    plt.figure(figsize=(15, 10))

    # Track if we've already added each label
    green_label_added = False
    red_label_added = False
    
    # adding the labels to the graph, so views understand what each
    # bar means
    for i in range(len(years)):
        color = colors[i]
        
        if color == 'green' and not green_label_added:
            label = "Champion made more 3PMs"
            green_label_added = True
        elif color == 'red' and not red_label_added:
            label = "Runner-Up made more 3PMs"
            red_label_added = True
        else:
            label = None
        
        # plotting the bars
        plt.bar(years[i], champ_diff[i], color=color, label=label)
    
    # making the axii and title, saving figure
    plt.xticks(rotation = 45, fontsize = 12)
    plt.ylabel("3PM Difference (Absolute Value)", fontsize = 24)
    plt.xlabel("Championship Year", fontsize=24)
    plt.title("3-Point Makes Difference in NBA Finals (Champion vs Runner-Up)", 
              fontsize=30)
    plt.legend()
    plt.savefig(figure_name)
    plt.show()


def main():
    regfile = "regular_season_3pt_zones.csv"
    regular_data = read_file_regularseason(regfile)
    reggame_averages = season_averages(regular_data)
    
    postfile = "postseason_3pt_by_zone.csv"
    post_data = read_file_postseason(postfile)
    visualize_regularseason(reggame_averages, "avg_regularseason.png")
    
    visualize_postseason(post_data, "avg_postseason.png")

main()
