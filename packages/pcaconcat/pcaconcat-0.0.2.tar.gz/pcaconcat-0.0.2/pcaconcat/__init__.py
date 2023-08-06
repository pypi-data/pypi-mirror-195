"""Top-level package for pcaconcat."""

__author__ = """advancehs"""
__email__ = '1019753743@qq.com'
__version__ = '0.0.2'


import addana
import pandas as pd



def pcaconcat(df,*col ):
    
    '''
    df: 处理的表
    col: 字符串，可以一列，可以多列
    '''
    print(len(col))
    if len(col)==1:
        df_ =  addana.transform(df[col[0]])
    elif len(col)==2:
        df_ =  addana.transform(df[col[0]]+df[col[1]])
    elif len(col)==3:
        df_ =  addana.transform(df[col[0]]+df[col[1]] +df[col[2]])
    else:
        print("最对传入三个列")


    if (df_["市"]=="").sum() >0:    ## 查看省市为空的个数
        index_error = df_[df_["市"]==""].index
        df_.loc[index_error,"市"] =  df_.loc[index_error,"区"]
        

    if (df_["市"]=="").sum() >0:
        print("注意，下面的行的市为空：" ,"\n",df_[df_["市"]==""].drop_duplicates())
    else:
        print("处理完毕，所有市都被识别")

    df_.columns = ["prov_s","city_s","area_s","loca_s"]  
     
    return  pd.concat([df,df_.iloc[:,0:len(col)]],axis=1)