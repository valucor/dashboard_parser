import csv
import re

def clean_data(result):
    result = re.sub("'\w", '', result)
    return result

def get_S2(quarter, product):
    s2_data = []
    with open('/Users/traenqui/Projects/Valucor/Parser/test_csvfile/CheckS2.csv', newline='') as csvfile:
        import_file = csv.reader(csvfile, delimiter=',')
        for row in import_file:
            s2_data.append(list(row))
    
    index = s2_data[0].index(quarter)
    for row in s2_data[1:]:
        if(row.count(product) >= 1):
            res = row[index]
            # print(f'{quarter} {product} has {res} EUR S2')
            return round(float(res), 2)
    # print(f'{product} has no S2 data')
    return 0

def get_StatRes(quarter, product):
    statres_data = []
    with open('/Users/traenqui/Projects/Valucor/Parser/test_csvfile/CheckStatRes.csv', newline='') as csvfile:
        import_file = csv.reader(csvfile, delimiter=',')
        for row in import_file:
            statres_data.append(list(row))
    
    index = statres_data[0].index(quarter)
    for row in statres_data[1:]:
        if(row.count(product) >= 1):
            res = row[index]
            # print(f'{quarter} {product} has {res} EUR StatRes')
            return round(float(res), 2)
    # sprint(f'{product} has no StatRes data')
    return 0

def get_policies(quarter, product):
    policy_data = []
    with open('/Users/traenqui/Projects/Valucor/Parser/test_csvfile/CheckNoPolicies.csv', newline='') as csvfile:
        import_file = csv.reader(csvfile, delimiter=',')
        for row in import_file:
            policy_data.append(list(row))
    
    index = policy_data[0].index(quarter)
    for row in policy_data[1:]:
        if(row.count(product) >= 1):
            res = row[index]
            # print(f'{quarter} {product} has {res} active Policies')
            return int(res)
    # print(f'{product} has no Policy data')
    return 0
