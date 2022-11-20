import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nHello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs


    while True:
      city = input("Please Enter City Name: new york city, chicago, washington\n ").lower()
      if city not in ('new york city', 'chicago', 'washington'):
        city = input("Pick one among new york city, chicago, washington: ").lower()
        continue
      else:
        break

    # TO DO: get user input for month (all, january, february, ... , june)

    while True:
      month = input('Enter a month among: january, february, march, april, may, june, or choose all  \n ').lower()
      if month not in ("january", "february", "march", "april", "may", "june", "all"):
        month = input("Please Enter a Correct Month: \n ").lower()
        continue
      else:
        break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
      day = input('Please Enter a Day of week: saturday, sunday, monday, tuesday, wednesday, thursday, friday, or choose all  \n ').lower()
      if day not in ("saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "all"):
        day = input("Please Enter Correct Day of Week: ").lower()
        continue
      else:
        break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):

    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    df = pd.read_csv(CITY_DATA[city])

    
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    
    if month != 'all':
   
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

    
        df = df[df['month'] == month]

        
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month

    Common_month = df['month'].mode()[0]
    print('Most Common Month:', Common_month)


    # TO DO: display the most common day of week

    Common_Weekday = df['day_of_week'].mode()[0]
    print('Most Common day:', Common_Weekday)



    # TO DO: display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most Common Hour:', common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station

    Common_Start_Station = df['Start Station'].value_counts().idxmax()
    print('\nThe Most Commonly Used Start Station:', Common_Start_Station)


    # TO DO: display most commonly used end station

    Common_End_Station = df['End Station'].value_counts().idxmax()
    print('\nThe Most Commonly Used End Station:', Common_End_Station)


    # TO DO: display most frequent combination of start station and end station trip

    Combination_Station = df.groupby(['Start Station', 'End Station']).count()
    print('\nThe Most Commonly Used Combination of Start and End Stations Trip:', Common_Start_Station, " & ", Common_End_Station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time

    Total_Travel_Time = sum(df['Trip Duration'])
    print('Total Travel Time:', Total_Travel_Time/86400, " Days")


    # TO DO: display mean travel time

    Mean_Travel_Time = df['Trip Duration'].mean()
    print('Mean Travel Time:', Mean_Travel_Time/60, " Minutes")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types

    user_types = df['User Type'].value_counts()
    #print(user_types)
    print('User Types:\n', user_types)

    # TO DO: Display counts of gender

    try:
      gender_types = df['Gender'].value_counts()
      print('\nGender Types:\n', gender_types)
    except KeyError:
      print("\nGender Types:\nNo Available Data.")

    # TO DO: Display earliest, most recent, and most common year of birth

    try:
      Earliest_Year = df['Birth Year'].min()
      print('\nEarliest Year:', Earliest_Year)
    except KeyError:
      print("\nEarliest Year:\nNo Avaiable Data.")

    try:
      Most_Recent_Year = df['Birth Year'].max()
      print('\nMost Recent Year:', Most_Recent_Year)
    except KeyError:
      print("\nMost Recent Year:\nNo data available for this month.")

    try:
      Most_Common_Year = df['Birth Year'].value_counts().idxmax()
      print('\nMost Common Year:', Most_Common_Year)
    except KeyError:
      print("\nMost Common Year:\nNo Available Data.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def display_data(df):
    print("Data Required is Ready to Check\n")
    
    index=0
    user_reply = input("Do You Need to See 5 Rows of Data?, Please Enter yes or no ").lower()
    if user_reply not in ['yes' or 'no']:
        print("Check Your Answer, Please Enter yes or no")
        user_reply = input("Do You Need to See 5 Rows of Data?, Please Enter yes or no ").lower()
    elif user_reply != "yes" :
        print("You Are Welcome")
        
    else:
        while index+5 < df.shape[0]:
            print(df.iloc[index:index+5])
            index +=5
            user_reply = input("Do You Need to See 5 Rows of Data?, Please Enter yes or no ").lower()
            if user_reply != "yes" :
                print("You Are Welcome")
                break




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("You are Welcome")
            break


if __name__ == "__main__":
	main()