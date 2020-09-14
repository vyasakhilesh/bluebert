export DATASET_DIR=/nfs/home/vyasa/projects/proj_os/data_os/bluebert_data/bert_data/ddi2013-type
export PYTHONPATH=/nfs/home/vyasa/projects/proj_os/repos/bluebert
export BlueBERT_DIR=/nfs/home/vyasa/projects/proj_os/data_os/bluebert_data/NCBI_BERT_pubmed_uncased_L-12_H-768_A-12
export OUTPUT_DIR=/nfs/home/vyasa/projects/proj_os/data_os/bluebert_data/output
source /nfs/home/vyasa/software/pkg/blue_bert_py_env/bin/activate

# python bluebert/run_bluebert.py \
#   --do_train=true \
#   --do_eval=false \
#   --do_predict=true \
#   --task_name="ddi" \
#   --vocab_file=$BlueBERT_DIR/vocab.txt \
#   --bert_config_file=$BlueBERT_DIR/bert_config.json \
#   --init_checkpoint=$BlueBERT_DIR/bert_model.ckpt \
#   --num_train_epochs=10.0 \
#   --data_dir=$DATASET_DIR \
#   --output_dir=$OUTPUT_DIR \
#   --do_lower_case=true


#   python bluebert/run_bluebert.py \
#   --do_train=false \
#   --do_eval=false \
#   --do_predict=true \
#   --task_name="ddi" \
#   --vocab_file=$BlueBERT_DIR/vocab.txt \
#   --bert_config_file=$BlueBERT_DIR/bert_config.json \
#   --init_checkpoint=$BlueBERT_DIR/bert_model.ckpt \
#   --num_train_epochs=10.0 \
#   --data_dir=$DATASET_DIR \
#   --output_dir=$OUTPUT_DIR \
#   --do_lower_case=true


  