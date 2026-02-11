"""
Enkidu Bazua​, Pranav Bollineni​, Sal Gagliardo​, Sophia Hughes​, Sebastian Romero​,
    and Dylan Tu​
DS2001 Project - File 1
April 7, 2025
This program reads the csv file "game.csv" from Kaggle, and returns
    a dictionary of statsitics that are useful for this project.
    Another function is implemented to clean the returned dictionary,
    and then this second dictionary is used as a parameter for two more
    functions that creates a bar-chart and line-chart. The purpose of 
    the bar-chart is to see the change in how three-pointers account for
    the total field goals from the introduction of the three-point line
    to modern day. Additionally, our line chart is used to plot the 
    3-point makes and 3-point attempts, and see how these two measures
    changed over time.
"""

import matplotlib.pyplot as plt


def read_game_data(game_info_file):
    '''
    
    This function reads a csv file of information, converts the data into
    its necessary form, and returns a dictionary of values for each year
    after the establishment of the 3-point line.

    Parameters
    ----------
    game_info_file : string
        name of the file that will be read.

    Returns
    -------
    game_data : dictionary
        a nested dictionary that follows the form:
            {year: {'home3pm': [list of values],         
        'home3pa': [[list of values], 'home3%': [[list of values],          
        'away3pm': [[[list of values], 'away3pa': [[[list of values],      
        'home_fgm': [[list of values], 'home_fga': [list of values],      
        'away_fgm': [list of values], 'away_fga': [list of values],        
        'away3%': [[list of values]}}
    '''
    # empty dictionary and list to hold values
    game_data = {}
    years = []

    # opening and reading file, skipping header, stripping and spliting at 
    # comma
    with open (game_info_file, 'r') as file:
        file.readline()
        for line in file:
            line = line.strip().split(',')
              
            # append years starting from 1979 (when 3-pt line was established)             
            year = int(line[5][:4])
            if year < 1979:
                continue
            years.append(year)
            
            # if year is not in the dictionary aleady, append it and
            # make its value a dictionary to hold information
            if year not in game_data:
                game_data[year] = {'home3pm': [], 'home3pa': [],
                                   'home3%': [], 'away3pm': [],
                                   'away3pa': [], 'away3%': [],
                                   'home_fgm': [], 'home_fga': [],
                                   'away_fgm': [], 'away_fga': [],
                                   'home_result': []}    
            
            # append the result at home to dictionary
            game_data[year]['home_result'].append(line[7])


            # NOTE: documentation for appending to a list in a dictionary
            # came from the website 'GeeksForGeeks'
            
            # for each of the values moving forward, convert to a float
            # if there is a value in the dataset. If not, append 0:
            # Home 3-Pointers made:
            home3 = line[12]
            if len(home3) > 0:
                game_data[year]['home3pm'].append(float(home3))
            else:
                game_data[year]['home3pm'].append(0)
            
            # Home 3-Pointers Attempted:
            home3_attempt = line[13]
            if len(home3_attempt) > 0:
                game_data[year]['home3pa'].append(float(home3_attempt))
            else:
                game_data[year]['home3pa'].append(0)
            
            # Home 3-Point Shooting Percentage:
            home3_percent = line[14]
            if len(home3_percent) > 0:
                game_data[year]['home3%'].append(float(home3_percent))
            else:
                game_data[year]['home3%'].append(0)
            
            # Away 3-Pointer Made:
            away3 = line[37]
            if len(away3) > 0:
                game_data[year]['away3pm'].append(float(away3))
            else:
                game_data[year]['away3pm'].append(0)
            
            # Away 3-Pointers Attempted
            away3_attempt = line[38]
            if len(away3_attempt) > 0:
                game_data[year]['away3pa'].append(float(away3_attempt))
            else:
                game_data[year]['away3pa'].append(0)
            
            # Home Field Goals Made
            home_fgm = line[9]
            if len(home_fgm) > 0:
                game_data[year]['home_fgm'].append(float(home_fgm))
            else:
                game_data[year]['home_fgm'].append(0)
            
            # Home Field Goals Attempted
            home_fga = line[10]
            if len(home_fga) > 0:
                game_data[year]['home_fga'].append(float(home_fga))
            else:
                game_data[year]['home_fgm'].append(0)
             
            # Away Field Goals Made
            away_fgm = line[34]
            if len(away_fgm) > 0:
                 game_data[year]['away_fgm'].append(float(away_fgm))
            else:
                 game_data[year]['home_fgm'].append(0)
            
            # Away Field Goals Attempted
            away_fga = line[35]
            if len(away_fga) > 0:
                 game_data[year]['away_fga'].append(float(away_fga))
            else:
                 game_data[year]['home_fgm'].append(0)
            
            # Away 3-Point Shooting Percentage
            away3_percent = line[39]
            if len(away3_percent) > 0:
                game_data[year]['away3%'].append(float(away3_percent))
            else:
                game_data[year]['away3%'].append(0)
            
    return game_data

            
def yearly_totals(data):
    '''
    This function calculates the yearly totals from the dictionary returned
    in the first function. Essentially, instead of a list of values for
    each game played per year, we are returning a dictionary with the key
    being the year, and the value being a dictionary where the values here
    are the averages for the year.

    Parameters
    ----------
    data : dictionary
        the dictionary returned from the read_game_data function .

    Returns
    -------
    year_numbers : dictionary
        a dictionary that has the key as the year, and the value as
        another dictionary that totals the numbers for each sub-key
        (one value for the list rather than a list).

    '''
    # intializing empty dictionary to hold key, values
    year_numbers = {}
    
    # for each year in the data, set an accumulator variable to hold the
    # value of interest
    for year in data:
        home3s_made = 0
        away3s_made = 0
        home_attempts = 0
        away_attempts = 0
        total_attempts_home = 0
        total_attempts_away = 0
        total_makes_home = 0
        total_makes_away = 0
        total_attempts = 0
        total_makes = 0
        total_fg_made = 0
        total_fg_attempts = 0
        fg3_percent_of_shots = 0
        home_percentages = []
        away_percentages = []
        total_percentage = 0
        home_wins = 0
        away_wins = 0
        
        # for each value in the year and subkey of interest,
        # add the value to the corresponding accumulator to get total
        for value in data[year]['home3pm']:
            home3s_made += value
        for value in data[year]['away3pm']:
            away3s_made += value
        for value in data[year]['home3pa']:
            home_attempts += value
        for value in data[year]['away3pa']:
            away_attempts += value
        for value in data[year]['home_fgm']:
            total_makes_home += value
        for value in data[year]['away_fgm']:
            total_makes_away += value
        for value in data[year]['home_fga']:
            total_attempts_home += value
        for value in data[year]['away_fga']:
            total_attempts_away += value
              
        
        # calculationg the total 3-point makes and attempts by adding home and
        # away team results
        total_makes = home3s_made + away3s_made
        total_attempts = home_attempts + away_attempts
        
        # calculating the total field goal makes and attempts by adding
        # home and away team results
        total_fg_made = total_makes_home + total_makes_away
        total_fg_attempts = total_attempts_home + total_attempts_away
        
        # to calculate the shooting percentages, append the values for
        # home and away 3% if its greater than 0
        for value in data[year]['home3%']:
            if value > 0:
                home_percentages.append(value)
        for value in data[year]['away3%']:
            if value > 0:
                away_percentages.append(value)
        
        # if the sum of home_percentages is greater than 0, then
        # caculate the overall shooting percentage at home. if not, 
        # the percentage is equal to 0
        # Do same for away
        if sum(home_percentages) > 0:
            home_percentage = sum(home_percentages) / len(home_percentages)
        else:
            home_percentage = 0
        if sum(away_percentages) > 0:
            away_percentage = sum(away_percentages) / len(away_percentages)
        else:
            away_percentage = 0
        
        # calculating the total percent of field goals taken that are
        # 3-pointers
        fg3_percent_of_shots = round(total_makes / total_fg_made, 2)
        
        # calulating the total percent of field goals taken that are not
        # 3-pointers
        other_shots_proportion = 1 - fg3_percent_of_shots
        
        # for each value in the home_result values of that year, add one
        # when the win is at home to home_wins, or add 1 if the win is away
        # to away_wins
        for value in data[year]['home_result']:
            if value == 'W':
                home_wins += 1
            else:
                away_wins += 1
        
        # calulcate the home vs away winning percentages
        home_win_percentage = home_wins / len(data[year]['home_result'])
        away_win_percentage = away_wins / len(data[year]['home_result'])
        
        # if the value in the accumulator variable is above 0, calculate
        # the total 3-pt shooting percentage
        if total_makes > 0 and total_attempts > 0:
            total_percentage = total_makes / total_attempts
        
        # add keys and values to the dictionary that is the value for 
        # the year
        year_numbers[year] = {'total_home3pm': home3s_made,
                              'total_away3pm': away3s_made,
                              'total_home3a': home_attempts,
                              'total_away3a': away_attempts,
                              'total_home3%': round(home_percentage, 2),
                              'total_away3%': round(away_percentage, 2),
                              'total_makes3': total_makes,
                              'total_attempts3': total_attempts,
                              'total_fgm': total_fg_made,
                              'total_fga': total_fg_attempts,
                              'total_3%': round(total_percentage, 2),
                              '3pt_fg_proportion': 
                                  round(fg3_percent_of_shots, 2),
                              'other_shots_proprtion': other_shots_proportion,
                              'home_win%': round(home_win_percentage, 2),
                              'away_win%': round(away_win_percentage, 2)}
    return year_numbers

def stacked_barchart(data, title, name, x_label, y_label, input1, input2):

    # intialize the empty lists that will hold values
    years = []
    rate1 = []
    rate2 = []
    
    # for each year in the list, append value to correponding list
    for year in data:
        years.append(year)
        rate1.append(data[year][input1])
        rate2.append(data[year][input2])
    
    # convert years to string
    years = [str(year) for year in years]
    
    # NOTE: Format for this function was influenced by the "Stacked Bar Chart"
    # article published by matplotlib website 
   
    # making the graph
    plt.figure(figsize=(10, 6))
    plt.bar(years, rate1, label=input1, color='seagreen')
    plt.bar(years, rate2, label=input2, color='darkorange', bottom = rate1) 
    
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    
    plt.ylim(0, 1)
    plt.xticks(rotation=45)
    plt.legend()
    
    plt.savefig(name, dpi=300)
    plt.show()


# Documentation for the optional parameter information was obtained from the 
    # website: RealPython: 
def linechart(data, title, name, x_label, y_label, input1, input2 = None, 
              input3 = None):  
    '''
    TThe function takes a dictionary as data, and with the given parameters
    for the input1 (and input2 and input3 if given), that
    should match key names in the dictionary, a linechart graph is rendered.

    Parameters
    ----------
    data : dictionary
        dictionary that holds data.
    title : string
        the title of the graph.
    name : string
        the name the visualization will be saved as.
    x_label : string
        the name of the x-axis.
    y_label : string
        the name of the y-axis.
    input1 : string
        the name of the data that will be plotted - should match a key
        in the dictionary.
    input2 : string, optional
        the name of the data that will be plotted - should match a key
        in the dictionary. The default is None.
    input3 : string, optional
        the name of the data that will be plotted - should match a key
        in the dictionary. The default is None.

    Returns
    -------
    Renders a linechart visualization.

    '''
    # empty lists that will hold values
    years = []  
    aspect1 = []  
    aspect2 = [] 
    aspect3 = []
    
    # for each year in the dictionary, append the year to year list, 
    # and append the value for input 1 into aspect 1's list.
    for year in data:
        years.append(year)  
        aspect1.append(data[year][input1])
        
        
        # if input 2 and input 3 were given, append them to the 
        # corresponding lists
        # We read an artical on RealPython that demonstrated what to do
        # with an optional parameter:
        if input2:
            aspect2.append(data[year][input2])
            
        if input3:
            aspect3.append(input3)
    
    # make the title and axii with the information given 
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    
    # plot the line with aspect1
    plt.plot(years, aspect1, label = input1, color = 'black', marker='o')
    
    # if input 2 and 3 were given, plot the lines for them as well
    if input2:
        plt.plot(years, aspect2, label = input2, color = 'dimgray',
                 marker = 'o')
    if input3:
        plt.plot(years, aspect3, label = input3, color = 'darkorange',
                 marker = 'o')
    
    # show the legend
    plt.legend()
    
    # save and show graph
    plt.savefig(name, dpi = 300)
    plt.show()
    
    
def main():
    # set variable to game file
    game_file = 'game.csv'
    
    # run the file through read_game_data function
    game_data = read_game_data(game_file) 
    
    # calculate the year totals, using the game_data return as the parameter
    year_totals = yearly_totals(game_data)
    
    # use the functions to make the graphs
    linechart(year_totals, '3-Point Shots Made and Attempted',
              'linechart_ma','Year', 'Number of Shots', 'total_makes3', 
              'total_attempts3')
    stacked_barchart(year_totals, "Proportion Breakdown of Field Goals", 
                     "stackedbar_fgproportion", "Year", 
                     "Proportion of Field Goals Made", 
                      "3pt_fg_proportion", "other_shots_proprtion",)
main()
        
        