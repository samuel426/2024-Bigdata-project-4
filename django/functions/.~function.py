import os
import findspark
import pyspark
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import col, to_date, udf

import pandas as pd
import numpy as np

os.environ["SPARK_HOME"] = "/home/hadoop/spark"
findspark.init()
sc = pyspark.SparkContext(appName = "tomato_score")
sqlContext = SQLContext(sc)


def gaussian(x, mean, std_dev):
    return (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev) ** 2)

def user_tomato_score(PFBS_NTRO_CBDX_CTRN, EXTN_TPRT, STRTN_WATER, WATER_LACK_VL, EXTN_ACCMLT_QOFLG, NTSLT_SPL_PH_LVL, NTSLT_SPL_ELCDT, AVE_INNER_TPRT_1_2, AVE_INNER_HMDT_1_2):
    file_path = "hdfs://master01:9000/user/hadoop/tomato_avg.csv"
    df = spark.read.csv(file_path, header=True, inferSchema=True)
    pdf=df.toPandas()
    stats = pdf.describe().transpose()
    means = stats['mean']
    std_devs = stats['std']
    
    return (gaussian(PFBS_NTRO_CBDX_CTRN, means['PFBS_NTRO_CBDX_CTRN'], std_devs['PFBS_NTRO_CBDX_CTRN']) * 560 + \
    gaussian(EXTN_TPRT, means['EXTN_TPRT'], std_devs['EXTN_TPRT']) * 42 + \
    gaussian(STRTN_WATER, means['STRTN_WATER'], std_devs['STRTN_WATER']) * 12 + \
    gaussian(WATER_LACK_VL, means['WATER_LACK_VL'], std_devs['WATER_LACK_VL']) * 30 + \
    gaussian(EXTN_ACCMLT_QOFLG, means['EXTN_ACCMLT_QOFLG'], std_devs['EXTN_ACCMLT_QOFLG']) * 1700 * 8 + \
    gaussian(NTSLT_SPL_PH_LVL, means['NTSLT_SPL_PH_LVL'], std_devs['NTSLT_SPL_PH_LVL']) * 5.5 + \
    gaussian(NTSLT_SPL_ELCDT, means['NTSLT_SPL_ELCDT'], std_devs['NTSLT_SPL_ELCDT']) * 8.5 + \
    gaussian(AVE_INNER_TPRT_1_2, means['AVE_INNER_TPRT_1_2'], std_devs['AVE_INNER_TPRT_1_2']) * 72 + \
    gaussian(AVE_INNER_HMDT_1_2, means['AVE_INNER_HMDT_1_2'], std_devs['AVE_INNER_HMDT_1_2']) * 168)

def find_tomato_near_row(score):
    file_path = "hdfs://master01:9000/user/hadoop/tscore.csv"
    df = spark.read.csv(file_path, header=True, inferSchema=True)
    df.withColumn('ScoreLoss', score-col('Score'))
    df.registerTempTable('tomato_score_loss')
    df_f=sqlContext.sql("select * from tomato_score_loss order by ScoreLoss limit 1")
    return df_f

def find_column(df, col):
    return df.select(col)

def user_strawberry_score():

