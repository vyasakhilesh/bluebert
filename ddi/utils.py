import pandas as pd 
import os
import argparse
from sklearn import metrics as sm

pd.options.display.max_columns=None
pd.options.display.max_colwidth=999


class utils(object):
    def __init__(self, result_file, test_file, file_sep):
        self.result_file = result_file
        self.test_file = test_file
        self.file_sep = file_sep

    
    def get_df(self, filename, sep, header=None):
        return pd.read_csv(filename, sep=sep, header=header, encoding='utf-8')

    def get_max_id_label(self, df, axis=1):
        max_col = df.idxmax(axis)
        return max_col
    
    def get_label_frm_index(self, col, unique_label_ind, unique_label):
        label_col = col.replace(unique_label_ind, unique_label)
        return label_col

    def get_label(self, df, col_name):
        return df[col_name]

    def get_precision(self, tr_labels, pre_labels, average='macro'):
        return sm.precision_score(tr_labels, pre_labels, average=average)

    def get_recall(self, tr_labels, pre_labels, average='macro'):
        return sm.recall_score(tr_labels, pre_labels, average=average)

    def get_f1(self, tr_labels, pre_labels, average='macro'):
        return sm.f1_score(tr_labels, pre_labels, average=average)

    def add_column(self, df, col, col_name):
        df[col_name] = col
        return df
    
    def display_df(self, df):
        print (df.head(5))


def add_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r','--result_file', dest='result_file', help='result tsv_file with label probability')
    parser.add_argument('-t','--test_file', dest='test_file', help='test tsv_file with label')
    parser.add_argument('-s','--sep', dest='file_sep', type=str, help='file field delimiter')
    parser.add_argument('-o','--output_path', dest='output_path', type=str, help='output path')
    return parser
    
def main():
    print ('In Main')
    parser = add_arguments()
    args = parser.parse_args()
    result_file = args.result_file
    test_file = args.test_file
    file_sep = args.file_sep
    output_path = args.output_path
    print (result_file, test_file, str(file_sep))

    uni_label_id = [0, 1, 2, 3, 4]
    uni_label = ['DDI-advise', 'DDI-effect', 'DDI-int', 'DDI-mechanism', 'DDI-false']
    evl = utils(result_file, test_file, str(file_sep))
    res_df = evl.get_df(result_file, file_sep)
    print (evl.display_df(res_df))
    res_label = evl.get_label_frm_index(evl.get_max_id_label(res_df), uni_label_id, uni_label)

    # DDI-task-2013
    # tes_df = evl.get_df(test_file, file_sep, header='infer')
    # print (evl.display_df(tes_df))
    # tes_label = evl.get_label(tes_df, 'label')
    # print ('##################################')
    # print (type(res_label), type(tes_label))
    # print (res_label.shape, tes_label.shape)
    # print (res_label[0:5], tes_label[0:5])
    # print (evl.get_precision(tes_label, res_label))
    # print (evl.get_recall(tes_label, res_label))
    # print (evl.get_f1(tes_label, res_label))
    
    # For SDM ddi data
    # df = evl.get_df(test_file, ',', header='infer')
    # df['predicted_label'] = res_label
    # df.to_csv(os.path.join(output_path,'new_pattern_pred_label.csv'), index=False)

    # For pubmed data
    df = evl.get_df(test_file, '\t', header='infer')
    df['predicted_label'] = res_label
    df.to_csv(os.path.join(output_path,'new_pattern_pred_label_pubmed_sample.tsv'), index=False, sep='\t')

if __name__ == "__main__":
    print('#######')
    main()
    



