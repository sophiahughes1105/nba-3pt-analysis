"""
Enkidu Bazua​, Pranav Bollineni​, Sal Gagliardo​, Sophia Hughes​, Sebastian Romero​,
    and Dylan Tu​
DS2001 Project - File 2
April 7, 2025
This program analyzes NBA team data to see how often the top 10 teams in 
    3-point field goal percentage make the playoffs each year. It reads 
    "game.csv", processes team FG3% averages, identifies 
    playoff teams, and calculates the percentage of top 3-point shooting 
    teams that reached the playoffs. A function is
    created to plots the data over time, from 1979 onward, in the form of a
    line-chart and returns the standard deviation of these percentages 
    to measure variability.
"""
 
import matplotlib.pyplot as plt
import pandas as pd 

# Read an article published on the python website titled
# "datetime — Basic date and time types" for this library
import datetime
 
def read_data(filename):
   '''
   Read in data from game.csv and extract useful information 
 
   Parameters
   ----------
   filename : String
       String of filename
 
   Returns
   -------
   Dictionary {header: [data]}
 
   '''
   
   # extracting the headers we need
   useful_headers = ['game_date', 'team_name_home', 'fg3_pct_home', 
                     'team_name_away', 'fg3_pct_away', 'season_type']
   
   # opening and reading the file, striping and splitting for headers and
   # all lines
   with open(filename, 'r') as file:
       headers = file.readline().strip().split(',')
       lines = [line.strip().split(',') for line in file]
       
       # setting the indicies that are useful for us (indices correspond
       # match the useful headers)
       useful_indices = [headers.index(i) for i in useful_headers]

    # getting the useful data
   useful_data = [[line[i] for i in useful_indices] for line in lines]
   
   return useful_data
 
def analyze_playoffs_teams(data):
   '''
   Checks if the top 10 3pt shooters are in the playoffs for each year. Returns % of teams from that top 10 that made it to playoffs
 
   Parameters
   ----------
   data : List
       List of lists containing player data [[useful data], [...], ...]
   Returns
   -------
   Dictionary containing {year: % of top 10 fg3% teams that made playoffs}
   '''
   
   # intializing the empty lists
   years = [] 
   team_stats = {}
   playoff_teams = {}
   
   def get_percentage(team):
       # need this for below for a for loop, just returns 2nd item in an 
       # iterable
       return team[1]
   
   for i in data:
       
       # date handling -- watched a tutorial on datetime library for this
       game_date = datetime.datetime.strptime(i[0], "%Y-%m-%d %H:%M:%S")
       game_year = game_date.year
       if game_year not in years: 
           years.append(game_year)
    
       # if the information is not in the dictionaries already, add as key and
       # intialize a value
       if game_year not in team_stats:
           team_stats[game_year] = {}
       if game_year not in playoff_teams:
           playoff_teams[game_year] = []
    
    # converting the home and away stats (if there are)
       home_team, away_team = i[1], i[3]
       home_fg3 = float(i[2]) if i[2] else 0.0
       away_fg3 = float(i[4]) if i[4] else 0.0
       
       # adding teams to dict -- including a count of games as well for average
       if home_team not in team_stats[game_year]:
           team_stats[game_year][home_team] = [home_fg3, 1]
       else:
           team_stats[game_year][home_team][0] += home_fg3
           team_stats[game_year][home_team][1] += 1
           
       if away_team not in team_stats[game_year]:
           team_stats[game_year][away_team] = [away_fg3, 1]
       else:
           team_stats[game_year][away_team][0] += away_fg3
           team_stats[game_year][away_team][1] += 1
           
    # if playoffs, then add the home and away team
       if i[5] == 'Playoffs':
           playoff_teams[game_year].append(home_team)
           playoff_teams[game_year].append(away_team)
   
    # for each year, calculate the 3 field goal average
   for year in team_stats:
       for team in team_stats[year]:
           fg3_avg = team_stats[year][team][0] / team_stats[year][team][1]
           team_stats[year][team] = fg3_avg
   
   results = {}
        
    # for hear year in the team_stats dictionary, sort   
   for year in team_stats:
       # looked up 'how to sort dictionary' on google and
       # read python docs for sorted() 
       sorted_teams = sorted(team_stats[year].items(), key=get_percentage, 
                             reverse=True)
       
       # sorted returns a list, so converting it back to a dictionary
       top_ten = dict(sorted_teams[:10])
       
       # finding number of teams in playoffs
       teams_in_playoffs = len([team for team in top_ten.keys() 
                                if team in playoff_teams[year]])
       
       # calculating the teams in playoff percentage
       teams_in_playoffs_pct = (teams_in_playoffs / len(top_ten)) * 100
       
       # adding to results dictionary
       results[year] = teams_in_playoffs_pct
       
   return results
       
def visualize(data):
   '''
   Create chart of % of teams in top 10 fg3 pct that made it to playoffs
 
   Parameters
   ----------
   data : Dictionary
       Dictionary containing {year: % of teams in playoffs}
   Returns
   -------
   Line chart of % of teams from the top 10 fg3% that made the playoffs
   '''
   
   # making a list of the years and values
   years = list(data.keys())
   values = list(data.values())
   
   # due to missing data/NBA rules change, only want 1979 and forward
   index_1979 = years.index(1979)
   years = years[index_1979:]
   values = values[index_1979:]
   
   # plotting
   plt.plot(years, values, marker='', color='blue', label='% of Top 10 3pt% teams in Playoffs')
   plt.xlabel('Year')
   plt.ylabel('% of Top 10 3pt% teams who made it to the Playoffs')
   plt.show()
   
   return pd.Series(values).std()
   
def main(): 
   data = read_data('game.csv')
   plottable_data = analyze_playoffs_teams(data)
   chart = visualize(plottable_data)
   
   return print(chart)
 
main()