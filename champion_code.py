"""
Enkidu Bazua​, Pranav Bollineni​, Sal Gagliardo​, Sophia Hughes​, Sebastian Romero​,
    and Dylan Tu​
DS2001 Project - File 4
April 7, 2025
This program analyzes NBA 3-point shooting data to compare regular season 
    performance of championship teams to the league average. It reads 
    a csv file with statistic published by the NBA and cleans the data, 
    identifies champions, normalizes 3-point shooting percentages using 
    z-scores, and plots how champions performed across different 3-point 
    zones over the years.
"""
 
import matplotlib.pyplot as plt
import pandas as pd
 
def read_data(filename):
    '''
    Read in data from CSV. Purposed for 3pt zones csv's. Returns as dictionary 
    with structure {headers: [list of values], ...}
 
    Parameters
    ----------
    filename : String
 
    Returns
    -------
    Dictionary 
    '''
    
    # intializing trhe empty dictionary
    team_dict = {}
    
    # opeining and reading the file, splitting and striping white space
    with open(filename, 'r', encoding='utf-8-sig') as file:
        headers = file.readline().strip().split(',')
        lines = [line.strip().split(',') for line in file]        
    
    # creating a dictionary with key as header, and value as the data
    # corresponding to that header
    data_dict = {headers[i]: [line[i] for line in lines] for i in
                 range(len(headers))}
    
    # clean the data - convert to float if number
    data_dict_cleaned = {k: [str(val) if val[:2].isalpha() else float(val) 
                             for val in v] for k, v in data_dict.items()}
    
    # extracting headers that are not 'Team' or 'Season'
    misc_headers = [i for i in headers if i != 'Team' and i != 'Season']
    
    # adding key/value pairs to the team_dict from the dictionaries cleaned
    # above
    for i in range(len(data_dict_cleaned['Season'])):
        team_dict[(data_dict_cleaned['Season'][i], 
                   data_dict_cleaned['Team'][i])] = [data_dict_cleaned[j][i] 
                    for j in misc_headers]
    
    return team_dict
 
def champions(data):
    '''
    Returns list of tuples of championship winners by year with structure 
    (year, winner)
 
    Parameters
    ----------
    data : Dictionary
 
    Returns
    -------
    Dictionary
    '''
    # intialize empty dictionary 
    champions_dict = {}
    
    # for key, values in the data, if value is 1, then add the value
    # and key to the championship_dict
    for k, v in data.items():
        if v[0] == float(1):
            champions_dict[k] = v
            
    return champions_dict
 
def normalize_data(data):
    '''
    Z-scores FG% for left, right and above break baskets by year and team. 
    To be used on regular season data only
 
    Parameters
    ----------
    data : Dictionary
 
    Returns
    -------
    Dictionary
    '''
    
    # (1) extract useful data from value (which is a list)    
    processed_data = {}
    
    for k in data.keys():
        v = data[k]
        
        if len(v) == 10:
            useful = [3, 6, 9]
            processed_data[k] = [v[i] for i in useful]
        elif len(v) == 9:
            useful = [2, 5, 8]
            processed_data[k] = [v[i] for i in useful]
            
    # (2) group data by year in new dictionary
    year_dict = {}
    
    for (year, team), values in processed_data.items():
        if year not in year_dict: 
            year_dict[year] = {}
        
        year_dict[year][team] = values
        
    # (3) z-score each year 
    zscore_dict = {}
    
    for year, teams in year_dict.items():
        left_values = [v[0] for v in teams.values()]
        right_values = [v[1] for v in teams.values()]
        above_values = [v[2] for v in teams.values()]
        
        left_srs = pd.Series(left_values)
        right_srs = pd.Series(right_values)
        above_srs = pd.Series(above_values)
        
        for team, values in teams.items():
            left_zscore = (values[0] - left_srs.mean()) / left_srs.std()
            right_zscore = (values[1] - right_srs.mean()) / right_srs.std()
            above_zscore = (values[2] - above_srs.mean()) / above_srs.std()
            
            zscore_dict[(year, team)] = [left_zscore, right_zscore,
                                         above_zscore]
            
    return zscore_dict
 
def plot_champions(data, champions):
    '''
    Plots the regular season 3pt performance for champions vs the league 
    average by year
    
    Parameters
    ----------
    data : Dictionary
        Regular season data for all teams in all years
    champions : Dictionary
        Contains champions for each season
 
    Returns
    -------
    Plot
    '''
    # initializing dictionary
    champion_stats = {}
    
    # for each k in data, if it is chamipm, then add the key-value pair to 
    # champion stats
    for k, v in data.items():
        if k in champions.keys():
            champion_stats[k] = v
    
    # making a list of years
    years = [k[0] for k in champion_stats.keys()]
    
    # making a list for different 3-point shots 
    champion_left = [v[0] for v in champion_stats.values()]
    champion_right = [v[1] for v in champion_stats.values()]
    champion_above = [v[2] for v in champion_stats.values()]
    
    # plotting
    plt.plot(years, champion_left, marker='', color='green', 
             label='Left Corner')
    plt.plot(years, champion_right, marker='', color='red', 
             label='Right Corner')
    plt.plot(years, champion_above, marker='', color='blue', 
             label='Above the Break')
    
    plt.legend()
    plt.title('Are champions better at 3pt shots than the rest of the league?')
    plt.xlabel('Year')
    plt.ylabel('Z-score')
    
    plt.show()
 
def main():
    # reading the two data files
    reg_season_data = read_data('regular_season_3pt_zones.csv')
    post_season_data = read_data('postseason_3pt_by_zone.csv')
    
    
    champions_output = champions(post_season_data)
    
    normalize_reg = normalize_data(reg_season_data)
    plot_test = plot_champions(normalize_reg, champions_output)
    return plot_test
 
main()

