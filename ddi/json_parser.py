
#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import json
import os
import multiprocessing as mp
import time


print("Start: JSONParser")
df_file = pd.DataFrame()
path = '/nfs/home/vyasa/projects/proj_os/data_os/bluebert_data/bert_data/ddi2013-type/pubmed_data/'

    
def parse(filename):
    with open(filename) as f:
        for js_obj in f:
            js_obj = json.loads(js_obj)
            yield js_obj
    

def parse_obj(js_obj):
    tmp_dict = {}
    tmp_dict['pmid']= int(js_obj['pmid'])
    tmp_dict['title']=js_obj['title']
    tmp_dict['abstract']=js_obj['abstract']
    return tmp_dict


def paserFile(filename):
    l = [parse_obj(js_obj)for js_obj in parse(filename)]
    df = pd.DataFrame.from_records(l)
    return df
    


filesList = sorted(os.listdir(path))
pool = mp.Pool(mp.cpu_count())

files= [path+file for file in filesList]

    
for result in pool.map(paserFile, files):
    startTime = time.time()
    df_file = df_file.append(result, ignore_index=True)
    elapsedTime = time.time() - startTime
    print ("TimeTakenByFileParsing", elapsedTime)
    del result
    
pool.close()
pool.join()


# print (files)
# for file in files:
#     paserFile(file)

df_file.to_csv('./data/final_file.tsv', sep='\t', index=False, encoding='utf-8')

print('End: JSONParser')