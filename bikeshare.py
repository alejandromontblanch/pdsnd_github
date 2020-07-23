#This code was written from scratch, with no template.

#Import the required packages
import numpy as np
import pandas as pd
import time
import textwrap

#Define the options for cities, months, filter period options and days.
#Define dictionaries for months and days that assigns a day or a month
#with its corresponding number in a calendar. This will be useful later.
cities = ('chicago','new_york_city','washington')
filter_period_opts = ('month','day','both','none')
possible_months = ('january','february','march','april','may','june')
dict_months = dict(zip(possible_months,np.arange(1,7,1)))
inv_dict_months = dict(zip(np.arange(1,7,1),possible_months))
possible_days = ('monday','tuesday','wednesday','thursday','friday',\
                 'saturday','sunday')
dict_days = dict(zip(possible_days,np.arange(1,8,1)))
inv_dict_days = dict(zip(np.arange(1,8,1),possible_days))


#Define a function which asks for a city as an input. This city must be in the
#list cities above, otherwise it will just keep asking for a city.
def select_city():
    while True:
        try:
            city = input(textwrap.dedent('''
            Please type a city: either Chicago, New York or Washington: 
            ''')).lower()
            if city in cities:
                break
            elif city == 'new york':
                city = 'new_york_city'
                break
            else:
                print('This is not a valid input! Please type a valid city')
        finally:
            print('Your choice: {}'.format(city))
    return city

#Define a function asking for the type of filtering.
def select_filter_period():
    while True:
        try:
            filter_period = input(textwrap.dedent('''
            Please type whether you want to filter by month, day, 
            both, or none: ''')).lower()
            if filter_period in filter_period_opts:
                break
            else:
               print('This is not a valid input! Please type a valid filter')
        finally:
            print('Your choice: {}'.format(filter_period))
    return filter_period

#Define a function asking for the month.
def select_month():
    while True:
        try:
            month = input(textwrap.dedent('''
            Please type which month: January, February, March, April, 
            May or June: ''')).lower()
            if month in possible_months:
                break
            else:
               print('This is not a valid input! Please type a valid month')
        finally:
            print('Your choice: {}'.format(month))
    return dict_months.get(month)

#Define a function asking for the day of the week.
def select_day():
    while True:
        try:
            day = input(textwrap.dedent('''
            Please type which day of the week: Monday, Tuesday, 
            Wednesday, Thursday, Friday, Saturday or Sunday: ''')).lower()
            if day in possible_days:
                break
            else:
               print('This is not a valid input! Please type a valid day')
        finally:
            print('Your choice: {}'.format(day))
    return dict_days.get(day)   

#Loads city data into a dataframe depending on the choice above. Additionally,
#it performs some preliminary operations depending on the options above. The
#returned df is just the df containing those elements depending on the
#choices.
def load_data(city,month,day):
    filename = '{}.csv'.format(city.lower())
    df = pd.read_csv(filename)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    df['day'] = df['Start Time'].dt.day_name()
    df['hour'] = pd.DatetimeIndex(df['Start Time']).hour

    if month != 'all' and day == 'all':
        df = df.loc[df['month'] == month]
    elif day != 'all' and month =='all':
        df = df.loc[df['day'] == inv_dict_days.get(day).title()]
    elif month != 'all' and day != 'all':
        df = df.loc[df['day'] == inv_dict_days.get(day).title()].\
            loc[df['month'] == month]
    
    return df

#Calculates the popular times to travel, based on the choices.
def pop_time_travel(df):
    popular_month = df['month'].mode()[0]
    popular_day = df['day'].mode()[0]
    popular_hour = df['hour'].mode()[0]
    return popular_month, popular_day, popular_hour

#Returns most popular stations.
def pop_stations(df):
    popular_start_station = df['Start Station'].mode()[0]
    popular_end_station = df['End Station'].mode()[0]
    popular_combo = df.groupby(['Start Station','End Station']).size().idxmax()
    return popular_start_station, popular_end_station, popular_combo

#Returns total times and average travel times.
def trip_duration(df):
    total_time = df['Trip Duration'].sum()
    average_time = df['Trip Duration'].mean()
    return total_time, average_time

#Returns some properties of the users.
def user_type(df):
    series_user_type = pd.Series(df['User Type']).value_counts()
    number_subscriber = series_user_type['Subscriber']
    number_customer = series_user_type['Customer']    
    return number_subscriber, number_customer

#Returns some additional personal data from the users.
def user_personal(df):
        series_user_gender = pd.Series(df['Gender']).value_counts()
        number_female = series_user_gender['Female']
        number_male = series_user_gender['Male']
        latest_year = int(df['Birth Year'].max())
        earliest_year = int(df['Birth Year'].min())
        common_year = int(df['Birth Year'].mode()[0])
        return number_female, number_male, latest_year, earliest_year,\
            common_year


#Main function.
def main():
    while True:
        #City and filter selection functions
        city = select_city()
        filter_period = select_filter_period()
        
        #Depending on the filter, so are the variables and functions called.
        if filter_period == 'month':
            month = select_month()
            day = 'all'
        elif filter_period == 'day':
            month = 'all'
            day = select_day()
        elif filter_period == 'both':
            month = select_month()
            day = select_day()
        else:
            month = 'all'
            day = 'all'
        
        #To time the remaining of the script (main operations happen here)
        start_time = time.time()
        
        #Loading of the data depending on the choices
        df = load_data(city,month,day)
        
        #Calling the functions that will give us the quantities we need.
        popular_month, popular_day, popular_hour = \
            pop_time_travel(df)
        popular_start_station, popular_end_station, popular_combo = \
            pop_stations(df)
        total_time, average_time = trip_duration(df)
        number_subscriber, number_customer = user_type(df)
        
        if city == 'new_york_city':
            city = 'New York' #Reformat city name to make it nicer.
        
        #Collection of messages that will be printed
        popularity_message_times = '''
        The most popular time to travel in {}, given your choices, is during 
        the month of {}, on {}s, at {}.'''.\
        format(city.title(),inv_dict_months.get(popular_month).title(),\
        popular_day,popular_hour)
        
        popularity_message_stations = '''
        People like departing from {}, arriving in {}, and the most popular 
        combination is starting in {} and ending in {}'''.\
        format(popular_start_station, popular_end_station, \
        popular_combo[0], popular_combo[1])
        
        travel_time_message = '''
        People travelled in total for {} seconds, with an average of {} 
        seconds per trip, in the city and your timeframe of choice.'''.\
        format(total_time,average_time)
            
        user_type_message = '''
        Within the timeframe you have selected, the number of subscribers 
        is {} and the number of customers is {}'''.\
        format(number_subscriber,number_customer)
        
        #Printing the above messages
        print(textwrap.dedent(popularity_message_times))
        print(textwrap.dedent(popularity_message_stations))
        print(textwrap.dedent(travel_time_message))
        print(textwrap.dedent(user_type_message))
        
        #Special case: we can retrieve additional data from two of the cities.
        if city in ('New York','chicago'):
            number_female, number_male, latest_year, earliest_year,\
                    common_year = user_personal(df)
            message_gender_birth = '''
            Because you chose {}, there is additional data. There were {} 
            male and {} female users. The earliest year of birth was {} and 
            the latest year of birth was {}. The most common year of birth 
            was {}. All of this within your timeframe of choice.'''.\
            format(city.title(), number_female, number_male, earliest_year,\
            latest_year, common_year)
            print(textwrap.dedent(message_gender_birth))
        
        #Showing how long running the script took
        print('-'*20)
        print("It took %s seconds to calculate." % (time.time() - start_time))
        print('-'*20)
        
        #Showing the raw data
        counter = 0        
        while True:
            try:
                selection = input(textwrap.dedent('''
                Would you like to see 5 (additional) rows of raw data, 
                given your choices? Type yes or no: '''))
                if selection == 'yes':
                    print(df[5*counter:5*(counter+1)])
                    counter += 1
                elif selection == 'no':
                    break
                else:
                    print('Please type yes or no. no will break the loop.')
            finally:
                print('Your choice: {}'.format(selection))
                
        
        #We want to decide whether we want to run the script again
        new_beginning = input('\nWould you like to restart? Enter yes or no: ')
        if new_beginning.lower() != 'yes':
            break

#Running the main function     
if __name__ == "__main__":
	main()