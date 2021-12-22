from django.shortcuts import render, redirect

from common.forms import UserForm


def signup(request):
    # 회원 가입
    if request.method == "POST":
        form = UserForm(request.POST)   # 입력 값을 가져옴
        if form.is_valid():
            form.save()     # 실제 저장
            return redirect('board:index')
    else:
        form = UserForm()   # 비어있는 폼
    return render(request, 'common/signup.html', {'form': form})

