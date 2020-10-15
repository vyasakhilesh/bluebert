from lxml import etree
import csv
import argparse
import os

import xml.etree.ElementTree as ET

# semantic_types_drug = ['Antibiotic', 'Substance', 'Chemical Viewed Structurally', 'Fish', 'Organism', 'Invertebrate', 
#                        'Hazardous or Poisonous Substance',  'Steroid', 'Therapeutic or Preventive Procedure', 'Organophosphorus Compound', 
#                        'Organic Chemical',  'Hormone', 'Laboratory Procedure', 'Clinical Drug', 'Chemical', 
#                        'Inorganic Chemical', 'Pharmacologic Substance', 'Vitamin', 'Carbohydrate', 'Biologically Active Substance']
# predicate_type_ddi = ['INTERACTS_WITH', 'INHIBITS', 'STIMULATES']

# Strict Drug Semantic-Type
semantic_types_drug = ['Pharmacologic Substance']
predicate_type_ddi = []


def replace_text(text, charoffset1, subtext1, charoffset2, subtext2, replace_string='@DRUG$'):
    ann1_start = charoffset1
    ann1_end = charoffset1 + len(subtext1)
    ann2_start = charoffset2
    ann2_end = charoffset2 + len(subtext2)
    if ann1_start <= ann2_start <= ann1_end \
            or ann1_start <= ann2_end <= ann1_end \
            or ann2_start <= ann1_start <= ann2_end \
            or ann2_start <= ann1_end <= ann2_end:
        start = min(ann1_start, ann2_start)
        end = max(ann1_end, ann2_end)
        before = text[:start]
        after = text[end:]
        # return before + f'@{ann1["type"]}-{ann2["type"]}$' + after
        return before + f'{replace_string}-{replace_string}' + after


    if ann1_start > ann2_start:
        ann1_start, ann1_end, ann2_start, ann2_end = ann2_start, ann2_end, ann1_start, ann1_end

    before = text[:ann1_start]
    middle = text[ann1_end:ann2_start]
    after = text[ann2_end:]

    # return before + f'@{ann1["type"]}$' + middle + f'@{ann2["type"]}$' + after
    return before + f'{replace_string}' + middle + f'{replace_string}' + after

def create_semrep_gld_bert(input_file, output_file, output_file_test, del_='\t'):
    fp = open(output_file, 'w', encoding='utf-8')
    writer = csv.writer(fp, delimiter=del_, lineterminator='\n')
    writer.writerow(['pmid', 'text', 'text_drug', 'semrep_label'])

    # Test file
    fp_test = open(output_file_test, 'w', encoding='utf-8')
    writer_test = csv.writer(fp_test, delimiter=del_, lineterminator='\n')
    writer_test.writerow(['pmid', 'text_drug',])
    cnt = 0

    tree = ET.parse(input_file)
    root  = tree.getroot()
    
    semantic_types_all = []
    predicate_types_all = []

    for i, medline_citation in enumerate(root.iter('MedlineCitation')):
        pmid = medline_citation.attrib['pmid']
        # print(pmid)
        for sentence in medline_citation.iter('Sentence'):
            text = sentence.attrib['text']
            # print(text)
            for predictions in sentence.iter('Predications'):
                for prediction in predictions.iter('Predication'):
                    for pred, sub, obj in zip(prediction.iter('Predicate'), prediction.iter('Subject'), prediction.iter('Object')):
                        # print (pred.attrib['type'])
                        # predicate_types_all.append(pred.attrib['type'])

                        # If Predicated Type is not decided
                        ## TODO
                        label = pred.attrib['type']

                        #Subject Parsing
                        flag_drug1 = False
                        charoffset1 = ''
                        subtext1 = ''

                        #Object Parsing
                        flag_drug2 = False
                        charoffset2 = ''
                        subtext2 = ''

                        if pred.attrib['type'] in predicate_type_ddi or True: # Always True as preicate type nt decided
                
                            for sem_type in sub.iter('SemanticTypes'):
                                for s_t_i in sem_type.iter('SemanticType'):
                                    # semantic_types_all.append(s_t_i.text)
                                    # print (s_t_i.text)
                                    if s_t_i.text in semantic_types_drug:
                                        charoffset1 = int(sub.attrib['charOffset'])
                                        subtext1 = sub.attrib['text']
                                        flag_drug1 = True
                                        break
                            
                            for sem_type in obj.iter('SemanticTypes'):
                                for s_t_i in sem_type.iter('SemanticType'):
                                    # semantic_types_all.append(s_t_i.text)
                                    # print (s_t_i.text)
                                    if s_t_i.text in semantic_types_drug:
                                        charoffset2 = int(obj.attrib['charOffset'])
                                        subtext2 = obj.attrib['text']
                                        flag_drug2 = True
                                        break
                            
                        if (flag_drug1 & flag_drug2):
                            text_drug = replace_text(text, charoffset1, subtext1, charoffset2, subtext2)
                            writer.writerow([pmid, text, text_drug, label])
                            writer_test.writerow([pmid, text_drug])


    # print (set(semantic_types))
    # print (set(predicate_types))

    
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
    
    output_file =os.path.join(output_path+'semrep_gld_bert_data_strict.tsv')
    output_file_test =os.path.join(output_path+'semrep_gld_bert_data_strict_test.tsv')
    # output_file =os.path.join(output_path+'semrep_gld_bert_data_nonstrict.tsv')
    # output_file_test =os.path.join(output_path+'semrep_gld_bert_data_nonstrict_test.tsv')
    
    create_semrep_gld_bert(input_file, output_file, output_file_test)
if __name__ == '__main__':
    main()

