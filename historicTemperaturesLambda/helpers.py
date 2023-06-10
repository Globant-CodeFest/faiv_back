from math import radians, cos, sin, sqrt, atan2
from logger_config import logger
import datetime

# Haversine formula to calculate the distance between two lat/long points on a sphere
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # radius of Earth in kilometers. Use 3956 for miles

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c  # returns distance in kilometers

def find_nearest_n_locations(lat, lon, locations, n):
    distances = []
    for loc in locations:
        dist = haversine_distance(lat, lon, loc[2], loc[3])
        distances.append((dist, loc)) 
    distances.sort()  # sort based on distance
    nearest_n_locations = [loc for dist, loc in distances[:n]]  # take first n locations
    logger.info(nearest_n_locations)
    return nearest_n_locations

def timestamp_to_month_year(timestamp):
    # convert timestamp to datetime object
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    # extract month and year
    month = dt_object.month
    year = dt_object.year
    logger.info(f'Month: {month}, Year: {year}')
    return {
        'month': month,
        'year': year
    }

def get_historic_temps_in_range(start_month_year, end_month_year, temp_data_table_tuples):
    historic_temps = []
    for record in temp_data_table_tuples.get('records'):
        for i in range(4, 16):
            month = i - 3
            year = record[2]
            if year >= start_month_year.get('year') and year <= end_month_year.get('year'):
                if year == start_month_year.get('year') and month < start_month_year.get('month'):
                    continue
                if year == end_month_year.get('year') and month > end_month_year.get('month'):
                    continue
                historic_temps.append({
                    'month': month,
                    'year': year,
                    'temperature': record[i]
                })
    return historic_temps

def get_average_temp(temp_data_table_tuples):
    average_temp = 0
    months_count = 0
    for record in temp_data_table_tuples.get('records'):
        for i in range(4, 16):
            average_temp += record[i]
            months_count += 1
    average_temp = average_temp / months_count
    return round(average_temp, 2)