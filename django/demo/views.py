from django.shortcuts import render
from django.utils import timezone
from .models import Post, Show


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'demo/post_list.html', {'posts': posts})

def show_result(request):
    '''
    request parsing하는 부분
    일단은 임의의 값을 준다.
    '''
    # 아래 지정하는 변수가 다 request에서 파싱한 결과가 되어야 함.
    input_1 = 1
    input_2 = 2


    query = Show(input_1, input_2)
    results = query.getDataFromHDFS()
    return render(request, 'demo/show_result.html', {'results': results})