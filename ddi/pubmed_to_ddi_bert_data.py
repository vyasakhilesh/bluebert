
#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import json
import os
import multiprocessing as mp
import time
import argparse
from collections import OrderedDict
from itertools import combinations


def parse(filename):
    with open(filename) as f:
        for js_obj in f:
            js_obj = json.loads(js_obj)
            yield js_obj
    
# sample_data
# sample_data = {"pmid": "30941", "title": "Chloride binding and the Bohr effect of human fetal erythrocytes and HbFII solutions.", "abstract": "1. We have observed that the alkaline Bohr effect of washed human fetal erythrocytes was larger than in human adult intact red cells, in physiological conditions of pH, PCO2 and temperature. This was also observed independently of the presence of CO2 and of 2,3 diphosphoglycerate (fresh or stored erythrocytes). 2. Experiments performed in purified HbFII and HbA1 solutions and direct titration of protons released upon oxygenation confirmed the larger alkaline Bohr effect of fetal hemoglobin, at physiological ionic strength. 3. At low chloride concentration HbFII solutions had an alkaline Bohr effect identical to that measured in HbA1 solutions. 4. Titration of purified Hb solutions with increasing concentrations of NaCl evidenced a lower O2 linked chloride binding by HbFII and predominantly at acid pH. 5. It is concluded that the larger alkaline Bohr effect of fetal erythrocytes of HbFII solutions is related to a diminished acid Bohr effect, due to the lower affinity of HbFII for chloride anions. 6. The physiological interest of these results for placental O2 transfer (double Bohr effect) and O2 delivery to the foetus is discussed.", "srctitle": "Pflugers Archiv : European journal of physiology", "pmid_ver": 1, "year": 1978, "month": 9, "keywords": ["Aging", "Chlorides", "Erythrocytes", "Female", "Fetal Hemoglobin", "Fetus", "Hemoglobin A", "Humans", "Hydrogen-Ion Concentration", "In Vitro Techniques", "Oxyhemoglobins", "Pregnancy"], "authors": ["C Poyart", "E Bursaux", "P Guesnon", "B Teisseire"], "affiliations": [], "issn": "0031-6768", "entities": {"gene": [{"end": 74, "id": "CUI-less", "start": 69}, {"end": 441, "id": "CUI-less", "start": 436}, {"end": 450, "id": "323589602", "start": 446}, {"end": 580, "id": "CUI-less", "start": 564}, {"end": 653, "id": "CUI-less", "start": 648}, {"end": 726, "id": "323589602", "start": 722}, {"end": 765, "id": 326403902, "start": 763}, {"end": 868, "id": "CUI-less", "start": 863}, {"end": 1075, "id": "CUI-less", "start": 1070}], "disease": [], "drug": [{"end": 8, "id": "4167203", "start": 0}, {"end": 29, "id": "CUI-less", "start": 25}, {"end": 128, "id": "CUI-less", "start": 124}, {"end": 336, "id": "292621503", "start": 333}, {"end": 366, "id": "271302003", "start": 344}, {"end": 633, "id": "4167203", "start": 625}, {"end": 814, "id": "314219703", "start": 810}, {"end": 835, "id": "301100803", "start": 833}, {"end": 851, "id": "4167203", "start": 843}, {"end": 947, "id": "CUI-less", "start": 943}, {"end": 1032, "id": "CUI-less", "start": 1028}, {"end": 1088, "id": "4167203", "start": 1080}, {"end": 1160, "id": "301100803", "start": 1158}, {"end": 1197, "id": "301100803", "start": 1195}], "species": [{"end": 45, "id": "960605", "start": 40}, {"end": 151, "id": "960605", "start": 146}, {"end": 195, "id": "960605", "start": 190}], "mutation": [], "pathway": [], "miRNA": []}, "logits": {"disease": [], "drug": [[{"end": 7, "start": 0}, 0.999968409538269], [{"end": 28, "start": 25}, 0.999947190284729], [{"end": 127, "start": 124}, 0.9999926090240479], [{"end": 335, "start": 333}, 0.9999954700469971], [{"end": 365, "start": 344}, 0.9999983310699463], [{"end": 632, "start": 625}, 0.9994506239891052], [{"end": 813, "start": 810}, 0.9999898672103882], [{"end": 834, "start": 833}, 0.9999958276748657], [{"end": 850, "start": 843}, 0.9999293088912964], [{"end": 946, "start": 943}, 0.9999911785125732], [{"end": 1031, "start": 1028}, 0.9999326467514038], [{"end": 1087, "start": 1080}, 0.9999936819076538], [{"end": 1159, "start": 1158}, 0.9999966621398926], [{"end": 1196, "start": 1195}, 0.9999963045120239]], "gene": [[{"end": 73, "start": 69}, 0.9999961853027344], [{"end": 440, "start": 436}, 0.9999970197677612], [{"end": 449, "start": 446}, 0.9999973773956299], [{"end": 579, "start": 564}, 0.9999966025352478], [{"end": 652, "start": 648}, 0.9999954700469971], [{"end": 725, "start": 722}, 0.9999966621398926], [{"end": 764, "start": 763}, 0.9999966621398926], [{"end": 867, "start": 863}, 0.999996542930603], [{"end": 1074, "start": 1070}, 0.999996542930603]], "species": [[{"end": 44, "start": 40}, 0.9999998807907104], [{"end": 150, "start": 146}, 0.9999998807907104], [{"end": 194, "start": 190}, 0.9999998807907104]]}}

def replace_string(sentence, ann1_start, ann1_end, ann2_start, ann2_end, replace_string='@DRUG$'):
    if ann1_start <= ann2_start <= ann1_end \
            or ann1_start <= ann2_end <= ann1_end \
            or ann2_start <= ann1_start <= ann2_end \
            or ann2_start <= ann1_end <= ann2_end:
        start = min(ann1_start, ann2_start)
        end = max(ann1_end, ann2_end)
        before = sentence[:start]
        after = sentence[end:]
        # return before + f'@{ann1["type"]}-{ann2["type"]}$' + after
        return before + f'{replace_string}-{replace_string}' + after


    if ann1_start > ann2_start:
        ann1_start, ann1_end, ann2_start, ann2_end = ann2_start, ann2_end, ann1_start, ann1_end

    before = sentence[:ann1_start]
    middle = sentence[ann1_end:ann2_start]
    after = sentence[ann2_end:]

    # return before + f'@{ann1["type"]}$' + middle + f'@{ann2["type"]}$' + after
    return before + f'{replace_string}' + middle + f'{replace_string}' + after

def parse_obj(js_obj):
    tmp_dict_l = []
    if 'entities' in js_obj:
        if 'drug' in js_obj['entities']:
            if len(js_obj['entities']['drug'])>=2:
                tmp_list_start_end = [(drug['start'], drug['end']) for i, drug in enumerate(js_obj['entities']['drug'])]
                pairs_combination = combinations(tmp_list_start_end, 2)

                for pair in pairs_combination:
                    sentence = js_obj['title'] + ' ' + js_obj['abstract'] # title, space and abstract
                    drug_1 = sentence[pair[0][0]:pair[0][1]]
                    drug_2 = sentence[pair[1][0]:pair[1][1]]
                    if drug_1!=drug_2:
                        tmp_dict = {}
                        tmp_dict['pmid']= js_obj['pmid']
                        # tmp_dict['sentence'] = sentence # space between title and abstract
                        tmp_dict['sentence_@DRUG$'] = replace_string(sentence, pair[0][0], pair[0][1], pair[1][0], pair[1][1])
                        # print (sentence)
                        # print (tmp_dict['sentence_@DRUG$'])
                        tmp_dict['drug_1'] = drug_1
                        tmp_dict['drug_2'] = drug_2
                        tmp_dict_l.append (OrderedDict(tmp_dict))
    return tmp_dict_l


def paserFile(filename):
    l = [parse_obj(js_obj) for js_obj in parse(filename)]
    # l = [parse_obj(filename)]
    flat_l = [i for s_l in l for i in s_l]
    # print (flat_l)
    df = pd.DataFrame.from_records(flat_l).dropna(how='all')
    #print (df)
    return df

def run_parser(files_list_all, start_id, end_id, output_path):
    print ("Processing files_{}_from_[start:_{}_end:_{})".format(len(files_list_all), start_id+1, end_id+1))
    df_file = pd.DataFrame()
    print ('No of pools', mp.cpu_count())
    pool = mp.Pool(mp.cpu_count())
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
    df_file[['pmid', 'sentence_@DRUG$']][0:3000].to_csv(os.path.join(output_path,'pubmed_file_bert_data_{}_{}.tsv'.format(start_id+1, end_id+1)), sep='\t', index=False, encoding='utf-8')
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
    

    out = [run_parser(files_list_all, s_i, e_i, output_path) for s_i, e_i in start_end_id_l if s_i!=e_i]

if __name__ == "__main__":
    print("Start: JSONParser")
    startTime = time.time()
    main()
    # paserFile(sample_data)
    elapsedTime = time.time() - startTime
    print ("\t\t Total_Time", elapsedTime)
    print('End: JSONParser')

