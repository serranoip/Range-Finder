
import csv
import json
from math import radians, cos, sin, asin, sqrt

csv_filename = 'problem1.csv'
json_filename = 'problem1.json'

with open(csv_filename) as csv_file:
    read_csv = csv.DictReader(csv_file)
    unseparated_csv = (list(read_csv))

with open(json_filename) as json_file:
    read_json = json.load(json_file)
    unseparated_json = read_json


# Haversine Formula
def haversine(csv_lat, csv_long,
              json_lat, json_long):
    """
    this function calculates the distance in metres of two flying objects
    :param csv_lat: latitude value of the flying object from the csv file
    :param csv_long: longitude value of the flying object from the csv file
    :param json_lat: latitude value of the flying object recorded in json format
    :param json_long: longitude of the flying object recorded in json format
    :return: returns the distance in metres between the two flying objects
    """
    long_distance = radians(json_long - float(csv_long))
    lat_distance = radians(json_lat - float(csv_lat))
    csv_lat = radians(float(csv_lat))
    json_lat = radians(json_lat)

    a = sin(lat_distance / 2) ** 2 + cos(csv_lat) * sin(long_distance / 2) ** 2 * cos(json_lat)
    c = 2 * asin(sqrt(a))
    radius = 6371000
    return c * radius


def separate_main_list(csv_list, json_list):
    """
    this function separates sensor ID's that are considered the same flying objects (distance less than or equal to
    100 meters) between the csv and json file and the sensor ID's that does not have a pair that produces less than
    or equal to 100 meters
    :param csv_list: list of dictionaries that contain the id, latitude, and longitude extracted from the csv file
    :param json_list: list of dictionaries that contain the id, latitude, and longitude extracted from the json file
    :return: this function returns four variables:
                    csv_distance_true: list that contains sensor ID's from the csv file that produces
                                              a distance of less than or equal to 100 meters
                    json_distance_true: list that contains sensor ID's from the json file that produces
                                               a distance of less than or equal to 100 meters
                    csv_distance_false: list that contains sensor ID's from the csv file that does not produce
                                               a distance of less than or equal to 100 meters
                    json_distance_false: list that contains sensor ID's from the json file that does not produce
                                               a distance of less than or equal to 100 meters
    """
    csv_distance_true = []
    json_distance_true = []
    csv_distance_false = []
    json_distance_false = []
    for i in range(len(csv_list)):
        for j in range(len(json_list)):
            distance_haversine = haversine(csv_list[i]['Latitude'], csv_list[i]['Longitude'],
                                           json_list[j]['Latitude'], json_list[j]['Longitude'])
            if distance_haversine <= 100:
                csv_distance_true.append(csv_list[i]['Id'])
                json_distance_true.append(json_list[j]['Id'])

            csv_distance_false = [item['Id'] for item in csv_list if item['Id'] not in csv_distance_true]
            json_distance_false = [item['Id'] for item in json_list if item['Id'] not in json_distance_true]

            if i == len(csv_list) - 1 and j == len(json_list) - 1:
                return csv_distance_true, json_distance_true, csv_distance_false, json_distance_false


def combine_csv_json(csv_two_sensor, json_two_sensor):
    """
    this function combines list of sensor ID's from csv and json files that has distance of less than or equal
    to 100 meters
    :param csv_two_sensor: list of ID's from the csv file that has distance of less than or equal to 100 meters
    :param json_two_sensor: list of ID's from the json file that has distance of less than or equal to 100 meters
    :return: list of pairs of sensor ID's that has a distance(maximum) of 100 meters
    """
    combined_list = list(zip(csv_two_sensor, json_two_sensor))
    return combined_list


def one_sensor_result(csv_one_sensor, json_one_sensor):
    """
    this function pairs the elements of both the csv and json list that does not produce a distance of less than or
    equal to 100 meters to -1 (negative one)
    :param csv_one_sensor: list that contains the sensor ID's from the csv file that does not produce
                           distance of less than or equal to 100 meters
    :param json_one_sensor: list that contains the sensor ID's from the csv file that does not produce
                           distance of less than or equal to 100 meters
    :return: a list of pairs of ID's from both the csv and json file that were paired with their
             corresponding -1 (negative one)
    """
    csv_tuple = [(csv_one_sensor[i], '-1') for i in range(len(csv_one_sensor))]
    json_tuple = [('-1', json_one_sensor[j]) for j in range(len(json_one_sensor))]
    return csv_tuple, json_tuple


def find_index_csv(main_csv_lst, one_id_csv):
    """
    this function finds the original position of each sensor ID paired with -1 (negative one) from
    the original list extracted from the csv file
    :param main_csv_lst: original list extracted from the csv file
    :param one_id_csv: list of tuples that contains sensor ID's from the csv file paired with -1 (negative one)
    :return: list of indexes that corresponds to the position of each sensor ID from the main list
    """
    key = 'Id'
    index = []
    count = 0
    for i, dic in enumerate(main_csv_lst):
        if dic[key] == one_id_csv[count][0]:
            count += 1
            index.append(i)
            if count > len(one_id_csv) - 1:
                break
    return index


def find_index_json(main_json_list, one_id_json):
    """
    this function finds the original position of each sensor ID paired with -1 (negative one) from
    the original list extracted from the json file
    :param main_json_list: original list extracted from the json file
    :param one_id_json: list of tuples that contains sensor ID's from the json file paired with -1 (negative one)
    :return: list of indexes that corresponds to the position of each sensor ID from the main list
    """
    key = 'Id'
    index = []
    count = 0
    for i, dic in enumerate(main_json_list):
        if dic[key] == one_id_json[count][1]:
            count += 1
            index.append(i)
            if count > len(one_id_json) - 1:
                break
    return index


def append_final_list(csv_index, json_index,
                      separated_csv, separated_json, main_lst):
    """
    this function adds both the csv and json sensor ID's paired with -1 (negative one) to the list of pairs of sensor
    ID's that has a separation distance of less than or equal to 100 meters.
    Also, this function inserts both csv and json ID's paired with -1 (negative one) to their appropriate index based
    on the original lists
    :param csv_index: list of indexes of the csv ID's paired with -1 (negative one)
    :param json_index: list of indexes of the json ID's paired with -1 (negative one)
    :param separated_csv: list of csv ID's paired with -1 (negative one)
    :param separated_json: list of json ID's paired with -1 (negative one)
    :param main_lst: list that contains csv and json ID's that has a distance of less than or equal to 100 meters
    :return: updated list that includes all the ID pairs
    """
    if len(csv_index) == len(json_index):
        for i in range(len(csv_index)):
            main_lst.insert(json_index[i], separated_json[i])
            main_lst.insert(csv_index[i], separated_csv[i])
    return main_lst


def write_to_file(main_lst):
    """
    this function writes the final result into a text file
    :param main_lst: final list that contains ID's that have a pair in both csv and json file and ID's paired
                     with -1 (negative one)
    """
    with open('output.txt', 'w') as fp:
        fp.write('\n'.join('%s:%s' % x for x in main_lst))


def main():

    csv_two_ids, json_two_ids, csv_one_id, json_one_id = separate_main_list(unseparated_csv, unseparated_json)
    csv_pair, json_pair = one_sensor_result(csv_one_id, json_one_id)
    csv_one_id_index = find_index_csv(unseparated_csv, csv_pair)
    json_one_id_index = find_index_json(unseparated_json, json_pair)
    temp_list = combine_csv_json(csv_two_ids, json_two_ids)
    final_list = append_final_list(csv_one_id_index, json_one_id_index,
                                   csv_pair, json_pair, temp_list)
    write_to_file(final_list)


main()
