# -*- coding: utf-8 -*-

import argparse
import os
import pickle

import torch


from pyretri.config import get_defaults_cfg, setup_cfg
from pyretri.index import build_index_helper, feature_loader
from pyretri.evaluate import build_evaluate_helper
import pandas as pd
from pyretri.index.metric import KNN
from sklearn.cluster import AgglomerativeClustering, SpectralClustering, kmeans_plusplus

import copy
os.environ['CUDA_VISIBLE_DEVICES'] = '1'

eva_save_path=''
beit_save_path=''

feat_dir_dict = {
    eva_save_path: 0.1,
    beit_save_path: 0.9,
}

output_file_path = ''
# ===================================================
with open(os.path.join(eva_save_path,'names.pkl'), "rb") as f:
    data = pickle.load(f)
    query_names = [item[0].name.split("/")[-1] for item in data['query']]
    gallery_names = [item[0].name.split("/")[-1].split('.')[0] for item in data['gallery']]

if not os.path.exists(output_file_path):
    os.makedirs(output_file_path)


fuse_mode = 'sum'
if fuse_mode == 'sum':
    similarity = 0
    for fea_dir, weight in feat_dir_dict.items():

        with open(os.path.join(fea_dir,'similarity.pkl'), "rb") as f:
            sim = pickle.load(f)
        

        similarity += sim * weight

    with open(os.path.join(output_file_path, 'similarity.pkl'),'wb') as f:
        pickle.dump(similarity, f,protocol=4)

    retreival_results = []
    similarity_index = similarity.topk(k=20, dim=1)[1]  # indices
    for i in range(similarity_index.size(0)):
        temp_idx = similarity_index[i].tolist()
        temp_name_list = [gallery_names[j] for j in temp_idx]
        retreival_results.append(' '.join(temp_name_list))
    result_dict = pd.DataFrame({'Id':query_names,'Predicted':retreival_results})

    submit_file_name = 'submit_fused_{}'.format(output_file_path.split('/')[-1])


        

print("-")
