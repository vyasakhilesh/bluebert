from lxml import etree
import csv
import argparse
import os

import xml.etree.ElementTree as ET

semantic_types_drug = ['Antibiotic', 'Biologically Active Substance', 'Clinical Drug', 'Organic Chemical',  
                      'Substance', 'Therapeutic or Preventive Procedure',]
predicate_type_ddi = ['INTERACTS_WITH', 'INHIBITS', 'STIMULATES']

def get_ann(arg, obj):
    for ann in obj['annotations']:
        if ann['id'] == arg:
            return ann
    raise ValueError

def replace_text():
    pass

def create_semrep_gld_bert(input_file, output_file, del_='\t'):
    fp = open(output_file, 'w', encoding='utf-8')
    writer = csv.writer(fp, delimiter=del_, lineterminator='\n')
    writer.writerow(['pmid', 'text', 'semrep_label'])
    cnt = 0

    tree = ET.parse(input_file)
    root  = tree.getroot()
    
    semantic_types = []
    predicate_types = []

    for i, medline_citation in enumerate(root.iter('MedlineCitation')):
        pmid = medline_citation.attrib['pmid']
        print(pmid)
        for sentence in medline_citation.iter('Sentence'):
            text = sentence.attrib['text']
            # print(text)
            for predictions in sentence.iter('Predications'):
                for prediction in predictions.iter('Predication'):
                    for pred, sub, obj in zip(prediction.iter('Predicate'), prediction.iter('Subject'), prediction.iter('Object')):
                        print (pred.attrib['type'])
                        predicate_types.append(pred.attrib['type'])
                        if pred.attrib['type'] in predicate_type_ddi:
                            pass
                            
                            #Subject Parsing
                        for sem_type in sub.iter('SemanticTypes'):
                            for s_t_i in sem_type.iter('SemanticType'):
                                semantic_types.append(s_t_i.text)
                                print (s_t_i.text)
                            
                            #Object Parsing
                        for sem_type in obj.iter('SemanticTypes'):
                            for s_t_i in sem_type.iter('SemanticType'):
                                semantic_types.append(s_t_i.text)
                                print (s_t_i.text)
    print (set(semantic_types))
    print (set(predicate_types))

    
def add_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input_file', dest='input_file', help='input xml file', required=True)
    parser.add_argument('-s','--sep', dest='del_', type=str, help='file field delimiter')
    parser.add_argument('-o','--output_path', dest='output_path', type=str, help='output path', required=True)
    return parser

def main():
    print ('In Main')
    parser = add_arguments()
    args = parser.parse_args()
    input_file = args.input_file
    del_ = args.del_
    output_path = args.output_path
    print (input_file, str(del_))
    
    output_file =os.path.join(output_path+'semrep_gld_bert_data.tsv')
    create_semrep_gld_bert(input_file, output_file)

if __name__ == '__main__':
    main()

