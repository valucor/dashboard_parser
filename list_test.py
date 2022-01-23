import os
import logging

from MySQL import *
from check import get_S2, get_StatRes, get_policies
from csv_reader import *
from temp import getPaths

## script to run

# Connection
localhost = "localhost"
root="root"
password="password"
connection = sql_connect(localhost, root, password)

all_paths = getPaths()

# Path and variables
for path in all_paths:

    temp = path.split('_')
    quarter = temp[3]
    quarter = quarter[:4]
    table_name = temp[2]

    diff_s2 = 0
    diff_statres = 0
    diff_policies = 0

    # remove old log
    if os.path.exists(f'logs/{quarter}_{table_name}.log'):
        os.remove(f'logs/{quarter}_{table_name}.log')

    # create logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # create file handler
    file_handler = logging.FileHandler(f'logs/{quarter}_{table_name}.log')
    file_handler.setLevel(logging.DEBUG)

    # create a formatter
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

    # add formate to handlers
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logging.info(f'This log is for {table_name} in {quarter}')

    s2_data = get_S2(quarter, table_name)
    StatRes_data = get_StatRes(quarter, table_name)
    policy_data = get_policies(quarter, table_name)

    #queries
    header = get_header()
    data = get_data(path)
    query_table = table_query(header)
    query_insert = insert_query(table_name, header)


    # Database logic
    connection = sql_connect(localhost, root, password)
    logging.info('Successfully connected to MySQL Server')
    if not database_exists(connection, quarter):
        logging.warning(f'{quarter} database does no exist!')
        database_create(connection, quarter)
        logging.info(f'Successfully created {quarter} database')
    # connect to the right database
    connection = database_connection(localhost, root, password, quarter)
    logging.info(f'Successfully connected to {quarter} database')

    # Table logic
    if table_exists(connection, table_name):
        logging.info(f'Table {table_name} already exists')
        table_delete(connection, table_name)
        table_create(connection, table_name, query_table)
        logging.info(f'Table {table_name} is now empty')
    else:
        logging.warning(f'Table {table_name} does not exist')
        table_create(connection, table_name, query_table)
        logging.info(f'Table {table_name} successfully created')

    # Table insert
    amount = table_insert_many(connection, query_insert, data, table_name)
    if(amount):
        logging.info(f'{amount} dataset inserted')


    diff_s2 = s2_data - check_s2(connection, table_name)
    diff_statres = StatRes_data - check_statres(connection, table_name)
    diff_policies = policy_data - check_policies(connection, table_name)

    # check values, set >1% info, >5% warning, >10% Critical
    diff_s2 = round(abs(diff_s2), 2)
    if diff_s2 <= (abs(s2_data) / 100):
        logging.info(f'Difference in S2 is less than 1% = {diff_s2}')
    elif diff_s2 < ((abs(s2_data) * 5) / 100):
        logging.warning(f'Difference in S2 is between 1-5% = {diff_s2}')
    elif diff_s2 < ((abs(s2_data) * 10) / 100):
        logging.critical(f'Difference in S2 is between 5-10% = {diff_s2}')
    else:
        logging.error(f'Difference in S2 is more than 10% = {diff_s2}')

    diff_statres = round(abs(diff_statres), 2)
    if diff_statres <= (StatRes_data / 100):
        logging.info(f'Difference in Stat Res = {diff_statres}')
    elif diff_statres < ((StatRes_data * 5) / 100):
        logging.warning(f'Difference in Stat Res = {diff_statres}')
    elif diff_statres < ((StatRes_data * 10) / 100):
        logging.critical(f'Difference in Stat Res = {diff_statres}')
    else:
        logging.error(f'Difference in Stat Res = {diff_statres}')


    diff_policies = round(abs(diff_policies),2)
    if diff_policies <= (diff_policies / 100):
        logging.info(f'Difference in active policies = {diff_policies}')
    elif diff_policies < ((diff_policies * 5) / 100):
        logging.warning(f'Difference in active policies = {diff_policies}')
    elif diff_policies < ((diff_policies * 10) / 100):
        logging.critical(f'Difference in active policies = {diff_policies}')
    else:
        logging.error(f'Difference in active policies = {diff_policies}')
