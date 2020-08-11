"""
Editted by Mike K on 2020-06-26.
"""
import os
import pandas as pd
from pdsql import mssql
import yaml
import logging
import json
import re
from time import sleep

pd.options.display.max_columns = 10


def read_params():
    base_dir = os.path.realpath(os.path.dirname(__file__))

    with open(os.path.join(base_dir, 'parameters.yml')) as param:
            param = yaml.safe_load(param)

    return param


def main(param):
    logging.basicConfig(filename='dhi-to-hydrotel.log', format='%(asctime)s: %(levelname)s: %(message)s', level=logging.INFO)

    run_time_start = pd.Timestamp.now()

    ######################################
    ### Parameters

    base_path = param['Input']['base_path']
    result_folders = param['Input']['result_folders']
    file_index = param['Input']['file_index']
    min_file_size = param['Input']['min_file_size']

    ####################################
    ### Get the files

    logging.info('--Get the files')

    files = {}
    for fold in result_folders:
        files1 = [files.update({os.path.join(base_path, fold, f): int(os.path.getmtime(os.path.join(base_path, fold, f)))}) for f in os.listdir(os.path.join(base_path, fold)) if (f.endswith('.txt') and (os.path.getsize(os.path.join(base_path, fold, f)) > min_file_size))]

    if not files:
        logging.error('No files found...something is wrong')
        raise ValueError('No files found...something is wrong')

    logging.info('Compare to previous run')

    if os.path.isfile(os.path.join(base_path, file_index)):
        with open(os.path.join(base_path, file_index)) as file:
            old_files = json.load(file)
    else:
        logging.info('First run')
        old_files = {}

    new_files = {}
    for f in files:
        if f in old_files:
            if files[f] > old_files[f]:
                new_files.update({f: files[f]})
        else:
            new_files.update({f: files[f]})

    combo_files = old_files.copy()
    combo_files.update(new_files)

    if new_files:
        ####################################
        ### Parse txt files and save to Hydrotel

        logging.info('Saving new data')

        regex = re.compile('\d+')
        date_col = 'Time'

        for f in new_files:
            data1 = pd.read_table(f, skiprows=1, parse_dates=[date_col], infer_datetime_format=True)
            cols = data1.columns.copy()
            data_col = [c for c in cols if c != date_col][0]

            point_num = int(regex.findall(data_col)[0])

            data2 = data1.rename(columns={date_col: 'DT', data_col: 'SampleValue'}).copy()
            data2['DT'] = data2['DT'].dt.floor('5Min')
            data2 = data2[data2.DT >= (run_time_start - pd.DateOffset(hours=12))]
            data2['Point'] = point_num
            data2['Quality'] = param['Output']['quality_code']
            data2['BypassValidation'] = 0
            data2['BypassAlarms'] = 0
            data2['BypassScaling'] = 0
            data2['BypassTimeOffset'] = 0
            data2['Priority'] = 3

            try:
                mssql.to_mssql(data2, param['Output']['server'], param['Output']['database'], param['Output']['sample_table'])
            except Exception as err:
                logging.error(str(err))
                raise ValueError(str(err))

        ## Save new index

        with open(os.path.join(base_path, file_index), 'w') as outfile:
            json.dump(combo_files, outfile)

    else:
        logging.info('No new files found')

    logging.info('Success')



####################################################################
### run

param = read_params()
scheduling = param['Input']['scheduling']

# Set delay
sleep(scheduling['delay'])

while True:
    time1 = str(pd.Timestamp.now())
    print(time1 + ': Run start')

    param = read_params()
    scheduling = param['Input']['scheduling']

    main(param)

    time2 = str(pd.Timestamp.now())
    print(time2 + ': Run finish')

    # Set run frequency
    sleep(scheduling['frequency'])
