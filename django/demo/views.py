from django.shortcuts import render
from django.utils import timezone
from .models import Post, Show
from .forms import ReceiveData


KEY_LIST = ['PFBS_NTRO_CBDX_CTRN', 'EXTN_TPRT', 'DWP_TPRT', 'ABSLT_HMDT', 
            'STRTN_WATER', 'WATER_LACK_VL', 'EXTN_SRQT', 'EXTN_ACCMLT_QOFLG', 
            'NTSLT_SPL_PH_LVL', 'NTSLT_SPL_ELCDT', 'AVE_INNER_TPRT_1_2', 'AVE_INNER_HMDT_1_2']


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
    produce_info = request.POST['produce_info']
    input_dict = {}
    for key in KEY_LIST:
        input_dict[key] = float(request.POST[key])

    for k, v in input_dict.items():
        print(k, v)
    print(type(v))

    # 2.
    receive_data = ReceiveData(produce_info, input_dict)
    f_path = receive_data.sendQueryToHDFS()

    # 3.
    # 아래 지정하는 변수가 다 request에서 파싱한 결과가 되어야 함.
    input_1 = 1
    #input_2 = 2
    query = Show(f_path, input_1)
    results = query.getDataFromHDFS()
    return render(request, 'demo/show_result.html', {'results': results})