
#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import json
import os
import multiprocessing as mp
import time
import argparse
from collections import OrderedDict


def parse(filename):
    with open(filename) as f:
        for js_obj in f:
            js_obj = json.loads(js_obj)
            yield js_obj
    

#entities": {"gene": [{"end": 61, "id": "CUI-less", "start": 47}, {"end": 77, "id": "CUI-less", "start": 66}], "disease": [], 
# "drug": [{"end": 61, "id": "CUI-less", "start": 47}, {"end": 77, "id": "CUI-less", "start": 66}], "species": [], "mutation": [], "pathway": [], "miRNA": []}
def parse_obj(js_obj):
    tmp_dict = {}
    if 'entities' in js_obj:
        if 'drug' in js_obj['entities']:
            if len(js_obj['entities']['drug'])>=2:
                tmp_dict['pmid']= js_obj['pmid']
                # tmp_dict['title'] = js_obj['title']
                # tmp_dict['abstract'] = js_obj['abstract']
                tmp_dict['sentence'] = js_obj['title'] + ' ' + js_obj['abstract'] # space between title and abstract
                for i, drug in enumerate(js_obj['entities']['drug']):
                    tmp_dict['drug_{}'.format(i)] = tmp_dict['sentence'][drug['start']:drug['end']]
                    tmp_dict['start_{}'.format(i)] = drug['start']
                    tmp_dict['end_{}'.format(i)] = drug['end']
                return OrderedDict(tmp_dict)
    return tmp_dict


def paserFile(filename):
    l = [parse_obj(js_obj)for js_obj in parse(filename)]
    df = pd.DataFrame.from_records(l).dropna(how='all')
    return df
    

def run_parser(files_list_all, start_id, end_id, output_path):
    print ("Processing files_{}_from_[start:_{}_end:_{})".format(len(files_list_all), start_id+1, end_id+1))
    df_file = pd.DataFrame()
    pool = mp.Pool(mp.cpu_count())
    print ('No of pools', pool)
    startTime = time.time()

    files = files_list_all[start_id:end_id]
    for result in pool.map(paserFile, files):
        startTime = time.time()
        df_file = df_file.append(result, ignore_index=True)
        del result
        elapsedTime = time.time() - startTime
        print ("Time_by_Pool: ", elapsedTime)

    
    pool.close()
    pool.join()
    
    elapsedTime = time.time() - startTime
    print ("\t\t Time_Taken_by_File_Parsing_Each_Loop: ", elapsedTime)
    
    df_file.to_csv(os.path.join(output_path,'parsed_file_{}_{}.tsv'.format(start_id+1, end_id+1)), sep='\t', index=False, encoding='utf-8')
    del df_file
    
    return None

def add_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input_path', dest='input_path', help='json_file path', required=True)
    parser.add_argument('-o','--output_path', dest='output_path', help='tsv_file path', required=True)
    parser.add_argument('-n','--n_files_per_loop', dest='n_files_per_loop', type=int, help='number of files per loop', required=True)
    return parser

    
def write_output(df_file, start_id, end_id, output_path):
    df_file.to_csv(os.path.join(output_path,'parsed_file_{}_{}.tsv'.format(start_id+1, end_id+1)), sep='\t', index=False, encoding='utf-8')
    del df_file
    return None


def main():
    
    parser = add_arguments()
    args = parser.parse_args()
    input_path = args.input_path
    output_path = args.output_path
    n_files_per_loop = args.n_files_per_loop
    print ("input_path: {}, output_path: {}, n_files_per_loop: {}".format(input_path, output_path, n_files_per_loop))

    files_list_all = [os.path.join(input_path, file) for file in sorted(os.listdir(input_path))]
    print ('Sample_file: {}, number_of_files: {}'.format(files_list_all[0], len(files_list_all)))
    

    # File parser
    n_files = len(files_list_all)-1199

    start_end_id_l = [(i*n_files_per_loop, i*n_files_per_loop + n_files_per_loop) \
                    for i in range(0, n_files//n_files_per_loop)] +\
                    [((n_files//n_files_per_loop)*n_files_per_loop, n_files)]
    

    out = [run_parser(files_list_all, s_i, e_i, output_path) for s_i, e_i in start_end_id_l]

if __name__ == "__main__":
    print("Start: JSONParser")
    startTime = time.time()
    main()
    elapsedTime = time.time() - startTime
    print ("\t\t Total_Time", elapsedTime)
    print('End: JSONParser')

