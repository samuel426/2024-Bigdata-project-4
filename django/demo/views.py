from django.shortcuts import render
from django.utils import timezone
from .models import Post, Show
from .forms import ReceiveData

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from functions.function import find_column


KEY_LIST = ['PFBS_NTRO_CBDX_CTRN', 'EXTN_TPRT',
            'STRTN_WATER', 'WATER_LACK_VL', 'EXTN_ACCMLT_QOFLG', 
            'AVE_INNER_TPRT_1_2', 'AVE_INNER_HMDT_1_2']

KEY_LIST_TOMATO = ['DWP_TPRT', 'NTSLT_SPL_PH_LVL', 'NTSLT_SPL_ELCDT']


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'demo/post_list.html', {'posts': posts})

def input_data(request):
    return render(request, 'demo/input.html')

def show_result(request):
    '''
    1. input_data 페이지에서 입력받은 데이터가 여기로 넘어온다.
    2. 넘어온 데이터를 HDFS나 다른 함수를 실행시켜 분석을 하고, 그 결과가 HDFS에 저장
    3. HDFS에 저장된 파일을 읽어옴
    '''
    
    # 1.
    produce_type = request.POST['produce_type']
    produce_info = {}

    if produce_type == 'tomato':
        for k in KEY_LIST_TOMATO:
            KEY_LIST.append(k)
        
        COLUMNS = [
            'BLMNG_CLUSTER',
            'FRT_LNGTH',
            'YIELD_CLUSTER',
            'FRST_TREE_CNT',
            'LAST_FWRCT_NO',
            'FRST_CLUSTER',
            'FLWR_CNT',
            'YIELD_CNT',
            'STEM_THNS',
            'FRT_WDTH',
            'FRT_WT',
            'LEAF_LNGTH',
            'LEAF_WDTH',
            'LEAF_CNT',
            'GRTH_LNGTH',
            'PLT_LNGTH'
        ]
    
    elif produce_type == 'strawberry':
        COLUMNS = [
            'SHPMN_QTY',
            'PH_LVL',
            'SGCN',
            'FRT_WDTH',
            'FRT_LNGTH',
            'FRST_RATE',
            'FRT_WT_WDTH_RATE',
            'SGCN_PH_RATE',
            'FRT_WT',
            'FRST_TREE_CNT',
            'NOT_BLMNG_CNT',
            'BLMNG_CNT',
            'BLPRD_TPCD',
            'FLWRCLSTR_FLWR_NBR',
            'FLWRCLSTR_BDDG_TPCD',
            'GRTH_SPD',
            'LEAF_LNGTH_LEAF_WDTH_RATE',
            'ACCMLT_LEAF_CNT',
            'LEAF_CNT_INCR_SPD',
            'AXLRBD_OCRN_TPCD',
            'GRTH_LNGTH',
            'CRN_DIAM',
            'LEAF_CNT',
            'PTL_LNGTH',
            'LEAF_WDTH',
            'LEAF_LNGTH',
            'PLT_LNGTH'
        ]

    for key in KEY_LIST:
        produce_info[key] = float(request.POST[key])


    # 2.
    receive_data = ReceiveData(produce_type, produce_info)
    df_spark = receive_data.get()

    # 3.
    df_spark_subset = find_column(df_spark, COLUMNS)
    df_pandas = df_spark_subset.toPandas()
    results = df_pandas.to_html(index=False)

    return render(request, 'demo/show_result.html', {'results': results})
