import csv
import re

# Reads the csv files and converts them to the right format
def get_data(path):
    result = []
    # path = input("Enter path to file: ")
    # print("Path to file: " + str(path))
    with open(path, newline='') as csvfile:
        import_file = csv.reader(csvfile, delimiter=',')
        for row in import_file:
            result.append(tuple(row))
        for row in result:
            for e in row:
                clean_res(e)
    return result[1:]

def clean_res(result):
    result = re.sub("[(,)']", '', result)
    return result

# get header and data
def get_header():
    header = [
        "product_group" ,
        "product" ,
        "subproduct" ,
        "policy_number" ,
        "policy_status" ,
        "policy_gender" ,
        "policy_age" ,
        "joint_life" ,
        "date_start" ,
        "date_lapse" ,
        "date_end" ,
        "premium_annual" ,
        "premium_single" ,
        "premium_indexation" ,
        "premium_changing" ,
        "funds_value" ,
        "pvprem" ,
        "pvfp" ,
        "pvcost" ,
        "pvscr" ,
        "statutory_res" ,
        "s2_res" ,
        "death_benefit_sum" ,
        "sum_of_salary" ,
        "disability_annuity" ,
        "benefit_indexation" ,
        "waiting_period" ,
        "coverage_style" ,
        "benefit_duration" ,
        "nbm" ,
        "coc" ,
        "combined_ratio"
    ]
    return header

# create table query
def table_query(header):
    query = ""
    for colum in header:
        query += colum + ' ' + "VARCHAR(255), "
    query = query[:-2]
    return query

# create the insert query 
def insert_query(table_name, header):
    temp = ""
    for column in header:
        temp += column + ', '
    temp = temp[:-2]
    
    value_string = "%s, " * len(header)
    value_string = value_string[:-2]

    sql = 'INSERT INTO ' + table_name + ' (' + temp + ' ) VALUES (' + value_string + ")"
    return sql