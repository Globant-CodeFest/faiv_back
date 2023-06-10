import json
from logger_config import logger
from db_conn import Psycopg
from helpers import find_nearest_n_locations, get_average_temp, timestamp_to_month_year, get_historic_temps_in_range
from OpenAI import OpenAI
import requests

def lambda_handler(event, context):
    logger.info(f"Event: {json.dumps(event)}")
    try:
        body = json.loads(event.get('body'))
        logger.info(f"Body: {json.dumps(body)}")
    except Exception as e:
        logger.error(e)
        return {
            'statusCode': 400,
            'body': 'Bad request'
        }
    
    try:
        lat = body.get('location').get('lat')
        lng = body.get('location').get('lng')
        elevation = body.get('location').get('elevation')
        startDate = int(body.get('dateRange').get('startDate'))
        endDate = int(body.get('dateRange').get('endDate'))
        location_name = body.get('location').get('name')

        startDate = startDate - 365*24*60*60*5
        endDate = endDate - 365*24*60*60*5

        # Get nearest station
        psgs_db = Psycopg()
        stations_query = "SELECT * FROM station_data;"
        stations_table_tuples = psgs_db.query(stations_query)
        locations = stations_table_tuples.get('records')
        nearest_station = find_nearest_n_locations(lat, lng, locations, 1)
        logger.info(f"Nearest station: {nearest_station}")

        # Get temperature for nearest station
        psgs_db = Psycopg()
        temp_data_query = f"SELECT * FROM temperature_data WHERE id='{nearest_station[0][1]}';"
        temp_data_table_tuples = psgs_db.query(temp_data_query)

        # Calculate average temp
        average_temp = get_average_temp(temp_data_table_tuples)
        logger.info(f"Average temp: {average_temp}")

        start_obj = timestamp_to_month_year(startDate)
        end_obj = timestamp_to_month_year(endDate)

        logger.info(f"Start obj: {start_obj}")
        logger.info(f"End obj: {end_obj}")

        hist_temps = get_historic_temps_in_range(start_obj, end_obj, temp_data_table_tuples)
        logger.info(f"Historic temps: {hist_temps}")

        prompt = f"Para la zona de {location_name}, para la latitud {lat}º, y longitud {lng}º donde la temperatura histórica promedio ha sido {average_temp}º celcios y a una altitud {elevation} metros sobre el nivel del mar, cuales son los cultivos y frutales más recomendados para la zona?"

        oai = OpenAI()
        oai_messages_list = [
            {"role": "system", "content": "Eres una inteligencia artificial que sugiere qué sembrar en una zona geográfica"},
            {"role": "user", "content": prompt}
        ]
        logger.info(f"OAI messages list: {oai_messages_list}")
        try:
            res = oai.create_chat_completion(oai_messages_list)
            answer = res['choices'][0]['message']['content']
        except:
            answer = 'No tenemos sugerencias por el momento.'

    except Exception as e:
        logger.error(e)
        hist_temps = []

    response_body = {
        'historicTemperatures': hist_temps,
        'sowing_suggestion': answer
    }
    
    return {
        'statusCode': 200,
        'body': response_body
    }


