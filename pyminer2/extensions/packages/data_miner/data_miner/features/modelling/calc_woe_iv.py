# -*- coding:utf-8 -*-
__author__ = 'boredbird'
import os
import numpy as np
import pandas as pd

import logging

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir = os.path.dirname(parent_dir)
output_dir = root_dir + r'\output'
features_dir = root_dir + r'\features'
modelling_dir = root_dir + r'\features\modelling'

import woe.feature_process as fp
import woe.GridSearch as gs

logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)

def config(data_path):
    data=data_path
    var_name=[]
    var_dtype=[]
    is_tobe_bin=[]
    is_candidate=[]
    is_modelfeature=[]
    for i in data.columns:
        var_name.append(i)
        #变量类型
        var_dtype.append(str(data[i].dtypes))
        #是否分箱
        if i.lower() in ['y', 'target']:
            tobe_bin = 0
        elif i.lower() in ['id', 'userid', 'user_id', 'order_no', 'order_id']:
            tobe_bin = 0
        elif str(data[i].dtypes)=="object":
            tobe_bin = 0
        else:
            tobe_bin=1
        is_tobe_bin.append(tobe_bin)
        #是否候选变量
        if i.lower() in ['y', 'target']:
            candidate = 0
        elif i.lower() in ['id', 'userid', 'user_id', 'order_no', 'order_id']:
            candidate = 0
        else:
            candidate=1
        is_candidate.append(candidate)
        #是否模型特征
        if i.lower() in ['y', 'target']:
            modelfeature = 0
        elif i.lower() in ['id', 'userid', 'user_id', 'order_no', 'order_id']:
            modelfeature = 0
        else:
            modelfeature=1
        is_modelfeature.append(modelfeature)

    df = pd.DataFrame({"var_name": var_name, 'var_dtype': var_dtype, 'is_tobe_bin': is_tobe_bin, 'is_candidate': is_candidate,'is_modelfeature': is_modelfeature})
    logging.info("配置文件修改完成")
    print(df)
    return df

        
def woe(data_path):
    config_path = config(data_path)
    data_path = data_path
    feature_detail_path = output_dir+'\\features_detail.csv'
    rst_pkl_path = output_dir+'\\woe_rule.pkl'
    # train Weight of Evidence rule
    feature_detail,rst = fp.process_train_woe(infile_path=data_path
                                           ,outfile_path=feature_detail_path
                                           ,config_path=config_path)
    return feature_detail
    logging.info("WOE和IV计算完成")
