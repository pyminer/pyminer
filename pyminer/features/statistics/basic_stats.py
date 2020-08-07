import pandas as pd
import numpy as np
import logging
import math
logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)


def varStats(dataframe,round=2):
    format_str = "{" + "0:,." + str(round) + "f}"
    data=dataframe
    list_role = []
    list_dtype = []
    list_level = []
    list_use = []
    list_sum = []
    list_max = []
    list_min = []
    list_total_count = []
    list_null = []
    list_null_rate = []
    list_unique = []
    list_unique_rate = []
    list_mean = []
    list_median=[]
    list_q1=[]
    list_q3=[]
    list_var = []
    list_std=[]
    list_skew = []
    list_kurt=[]
    list_notnull_count = []
    list_mode = []
    list_range = []
    list_qrange = []
    list_cov = []
    list_sum_of_squares=[]
    list_se = []
    for i in data.columns:
        if i.lower() in ['y', 'target']:
            role = "目标"
        elif i.lower() in ['id','userid','user_id','order_no','order_id']:
            role = "ID"
        else:
            role = "输入"
        list_dtype.append(str(data[i].dtypes))
        list_role.append(role)
        if  data[i].nunique()==2:
            list_level.append("二值型")
        elif data[i].nunique()>2 and str(data[i].dtypes)=="object":
            list_level.append("名义型")
        elif data[i].nunique()==1:
            list_level.append("单一值")
        else:
            list_level.append("区间型")
        list_use.append("是")
        list_total_count.append(len(data))
        list_notnull_count.append(data[i].notnull().sum())
        list_null.append(data[i].isnull().sum())
        list_null_rate.append('{:,.2%}'.format(data[i].isnull().sum() / len(data)))
        list_unique.append(data[i].nunique())
        list_unique_rate.append('{:,.2%}'.format(data[i].nunique() / len(data)))
        list_mode.append(data[i].mode()[0])
        #数值变量计算
        if str(data[i].dtypes)=="int64" or str(data[i].dtypes)=="float64":
            list_min.append(data[i].min())
            list_q1.append(format_str.format(data[i].quantile(0.25)))
            list_q3.append(format_str.format(data[i].quantile(0.75)))
            list_skew.append(format_str.format(data[i].skew()))
            list_kurt.append(format_str.format(data[i].kurt()))
            list_mean.append(format_str.format(data[i].mean()))
            list_var.append(format_str.format(data[i].var()))
            list_std.append(format_str.format(data[i].std()))
            list_median.append(format_str.format(data[i].median()))
            list_max.append(data[i].max())
            list_range.append(format_str.format(data[i].max()-data[i].min()))
            list_qrange.append(format_str.format(data[i].quantile(0.75) - data[i].quantile(0.25)))
            list_cov.append(format_str.format(data[i].std()/data[i].mean()))
            list_sum.append(format_str.format(data[i].sum()))
            list_sum_of_squares.append(format_str.format(sum([num*num for num in data[i]])))
            list_se.append(format_str.format(data[i].var()/math.sqrt(data[i].notnull().sum())))
        else:
            list_min.append("")
            list_q1.append("")
            list_q3.append("")
            list_skew.append("")
            list_kurt.append("")
            list_mean.append("")
            list_var.append("")
            list_std.append("")
            list_median.append("")
            list_max.append("")
            list_range.append("")
            list_qrange.append("")
            list_cov.append("")
            list_sum.append("")
            list_sum_of_squares.append("")
            list_se.append("")
    df = pd.DataFrame(
        {"变量名": data.columns, '数据类型': list_dtype, '角色': list_role, '水平': list_level, '是否使用': list_use,'总体计数': list_total_count,'非缺失值计数': list_notnull_count,'均值':list_mean,'均值标准误':list_se,'方差': list_var,'标准差':list_std,'变异系数':list_cov,'总和':list_sum,'平方和':list_sum_of_squares,'众数':list_mode,'最小值': list_min,'Q1': list_q1,'中位数': list_median,'Q3':list_q3,'最大值': list_max,'极差': list_range,'四分位间距': list_qrange,'峰度':list_kurt,'偏度':list_skew,'缺失值': list_null, '缺失值占比': list_null_rate,'唯一值': list_unique, '唯一值占比': list_unique_rate})
    df.to_csv("var_stats.csv")
    logging.info('描述统计处理完成')
    return df

