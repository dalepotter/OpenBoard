from datetime import datetime, timedelta
from io import StringIO
from os import system
from lxml import etree

def generate_rtt_url(start_time=datetime.now()):
    """Create a Realtime Trains detailed listing URL from a specified start time.  The generated URL will look for movements that are expected for 24 hours following the input start time.

    Args:
        start_time (datetime): The start time. Defaults to when the script is run.

    Returns:
        str: A URL for a Realtime Trains detailed departure board page.
    """
    URL_REAL_TIME_TRAINS = "http://www.realtimetrains.co.uk/search/advanced/STPLNAR/{yyyy}/{mm}/{dd}/{hhhh1}-{hhhh2}?stp=WVS&show=all&order=actual"

    year = start_time.year
    time = "{hh}{mm}".format(hh=start_time.strftime('%H'), mm=start_time.strftime('%M'))
    time_tomorrow = start_time + timedelta(hours=23, minutes=59)
    time_tomorrow = "{hh}{mm}".format(hh=time_tomorrow.strftime('%H'), mm=time_tomorrow.strftime('%M'))

    url = URL_REAL_TIME_TRAINS.format(yyyy=start_time.year,mm=start_time.strftime('%m'),dd=start_time.strftime('%d'),hhhh1=time,hhhh2=time_tomorrow)
    return url


def load_rtt_trains(html_str):
    """Return train information from a Realtime Trains detailed listing HTML page.

    Args:
        html_str (str): HTML string representing a RTT detailed departure board page.

    Returns:
        list of dict: Containing data about each train on the input page.
    """
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html_str), parser)

    output = list()
    for train in tree.xpath('//table/tr'):
        train_dict = {
            'destination': train.xpath('td[@class="location"]/span')[1].text
        }
        output.append(train_dict)
    return output


# Define test connection to Realtime Trains function
def test_rtt_connection():

    """Returns True if connection to Realtime Trains can be made, otherwise returns False."""

    # Define realtime trains address
    address = 'realtimetrains.co.uk'

    # Save result of pinging address once
    result = system('ping -c 1 {}'.format(address))

    # If realtime trains pinged successfully
    if result == 0:
        # Return True
        return True

    # Otherwise
    else:
        # Return False
        return False

def is_cancelled(input_string):

    '''Returns True if input_string is 'Cancel', otherwise, returns False'''

    # If input_string is 'Cancel' as a string
    if input_string == 'Cancel':

        # Return True
        return True

    # If input_string is not'Cancel' as a string
    else:

        # Return False
        return False

# Sort for half minutes using round() from math

def mins_left_calc(event_time, comparison_time=datetime.now()):

    '''
    Returns integer of minutes to event_time from comparison_time.

    Args:
        event_time (datetime): The time of the event.
        comparison_time (datetime): The time to compare the time of the event to.

    Returns:
        (Integer) Number of minutes to event_time from comparison_time.

    Illustrative example:

        Args:
            event_time: Time in exactly two minutes as datetime
            comparison_time: Time now as datetime

        Returns:
            2
    '''

    # Save difference between event_time and comparison_time as datetime.timedelta object
    difference = event_time - comparison_time

    # Save difference as minutes
    difference = (difference.total_seconds()/60)

    # Round difference to 0 decimal places
    difference = int(difference)

    # Return difference
    return difference


def convert_time(time_string, time_accessed):

    '''Converts input time_string to datetime using input time_accessed as reference.'''

    # Save hour as integer
    hour = int(time_string[0:2])

    # Save minute as integer
    minute = int(time_string[2:4])

    # Default second to be 0
    second = 0

    # If fifth character is a fraction
    if time_string[4:5] in ['¼', '½', '¾']:

        # Save fraction as second
        second = time_string[4:5]

        # Save and convert fractions to relevant seconds as string
        second = second.replace('¼', '15')
        second = second.replace('½', '30')
        second = second.replace('¾', '45')

        # Save second as integer
        second = int(second)

    # Save converted_time by overwriting time_accessed datetime as relevant
    converted_time = time_accessed.replace(hour=hour, minute=minute, second=second, microsecond=0)

    # If time_string meant to be tomorrow
    if (converted_time - time_accessed).days < 0:

        # Add a day to converted_time
        converted_time = converted_time + timedelta(days=1)

    return converted_time
