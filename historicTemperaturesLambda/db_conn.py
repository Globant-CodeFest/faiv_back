from logger_config import logger
import psycopg2
import os
from helpers import find_nearest_n_locations
import datetime

class Psycopg():
    def __init__(self):
        self.db_name=os.environ.get('DB_NAME')
        self.user=os.environ.get('DB_USER')
        self.password=os.environ.get('DB_PASS')
        self.host=os.environ.get('DB_HOST')
        self.port=os.environ.get('DB_PORT')
        self.conn = psycopg2.connect(
            database=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cur = self.conn.cursor() 

    def query(self, query):
        records = []
        db_statusCode = 200
        try:
            self.conn.cursor()
            self.cur.execute(query) # SELECT * FROM test;
            records = self.cur.fetchall()
            db_statusCode = 200
        
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(error)
            db_statusCode = 500

        finally:
            self.cur.close()
            self.conn.close()

        return_dict = {
            'records': records,
            'statusCode': db_statusCode
        }
        # print('RETURN DICT')
        # print(return_dict)
        logger.info(return_dict)
        return return_dict

"""
station_data

Unnamed: (int) ID
id: (string) Station ID
latitud: (float) Latitude
longitude: (float) Longitude
stenlev: (float) Elevation
name: (string) Station name

temperature_data

unnamed: (int) ID
id: (string) Station ID
year: (int) Year
measurement_type: (string) Measurement type
jan: (float) Temperature
feb: (float) Temperature
mar: (float) Temperature
april: (float) Temperature
may: (float) Temperature
june: (float) Temperature
july: (float) Temperature
august: (float) Temperature
september: (float) Temperature
october: (float) Temperature 
november: (float) Temperature
december: (float) Temperature


example
-33.40868832820811, -70.5685887810097
"""

# psgs_db = Psycopg()
# stations_query = "SELECT * FROM station_data;"
# stations_table_tuples = psgs_db.query(stations_query)
# locations = stations_table_tuples.get('records')

# nearest_station = find_nearest_n_locations(-33.42880235568389, -70.6053026540827, locations, 1)
# print(nearest_station)

# psgs_db = Psycopg()
# temp_data_query = f"SELECT * FROM temperature_data WHERE id='{nearest_station[0][1]}';"
# temp_data_table_tuples = psgs_db.query(temp_data_query)
# print(temp_data_table_tuples)

# def get_average_temp(temp_data_table_tuples):
#     average_temp = 0
#     months_count = 0
#     for record in temp_data_table_tuples.get('records'):
#         for i in range(4, 16):
#             print(record[i])
#             average_temp += record[i]
#             months_count += 1
#     average_temp = average_temp / months_count
#     return round(average_temp, 2)

# # Calculate average temp
# average_temp = get_average_temp(temp_data_table_tuples)
# print(average_temp)

# def timestamp_to_month_year(timestamp):
#     # convert timestamp to datetime object
#     dt_object = datetime.datetime.fromtimestamp(timestamp)
#     # extract month and year
#     month = dt_object.month
#     year = dt_object.year
#     print(f'Month: {month}, Year: {year}')
#     logger.info(f'Month: {month}, Year: {year}')
#     return {
#         'month': month,
#         'year': year
#     }

# def get_historic_temps_in_range(start_month_year, end_month_year, temp_data_table_tuples):
#     historic_temps = []
#     for record in temp_data_table_tuples.get('records'):
#         for i in range(4, 16):
#             month = i - 3
#             year = record[2]
#             if year >= start_month_year.get('year') and year <= end_month_year.get('year'):
#                 if year == start_month_year.get('year') and month < start_month_year.get('month'):
#                     continue
#                 if year == end_month_year.get('year') and month > end_month_year.get('month'):
#                     continue
#                 historic_temps.append({
#                     'month': month,
#                     'year': year,
#                     'temperature': record[i]
#                 })
#     return historic_temps

# # 645069496 Junio 1990
# # 679197496 Julio 1991
# start_obj = timestamp_to_month_year(645069496)
# end_obj = timestamp_to_month_year(679197496)

# hist_temps = get_historic_temps_in_range(start_obj, end_obj, temp_data_table_tuples)
# print(hist_temps)