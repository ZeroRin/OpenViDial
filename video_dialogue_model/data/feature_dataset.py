# encoding: utf-8
"""
@author: Yuxian Meng
@contact: yuxian_meng@shannonai.com

@version: 1.0
@file: feature_dataset
@time: 2020/11/14 12:07
@desc: Read feature dataset from directory generated by preprocess_video_data.py

"""

import numpy as np
import torch
from torch.utils.data import Dataset
from typing import List
from video_dialogue_model.data.utils import sent_num_file, offsets_file, feature_file, warmup_mmap_file


class FeatureDataset(Dataset):
    """Load Feature dataset"""
    def __init__(self, data_dir, split="train"):
        self.data_dir = data_dir
        self.sent_num = np.load(sent_num_file(data_dir, split))
        self.offsets = np.load(offsets_file(data_dir, split))
        self.dim = 1000
        self.total_num = self.offsets[-1] + self.sent_num[-1]
        warmup_mmap_file(feature_file(data_dir, split))
        self.features = np.memmap(feature_file(data_dir, split), dtype='float32', mode='r',
                                  shape=(self.total_num, self.dim))

    def __getitem__(self, item):
        return self.features[item]

    def __len__(self):
        return self.total_num


def test_feature_dataset():
    from tqdm import tqdm
    d = FeatureDataset(data_dir="../../sample_data/preprocessed_data")
    for x in tqdm(d):
        print(x.shape)
        print(x)


if __name__ == '__main__':
    test_feature_dataset()