from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from board.models import Question, Answer, Comment
from board.forms import QuestionForm, AnswerForm, CommentForm


@login_required(login_url='common:login')
def question_create(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)  # 자료 전달받음(request.POST)
        if form.is_valid():
            question = form.save(commit=False)  # 가저장(날짜를 전달받지 못했기에 가저장)
            question.create_date = timezone.now()  # 날짜 시간 저장
            question.author = request.user  # 세션에 있는 유저 저장
            question.save()  # 실제 저장
            return redirect('board:board_list')  # 이동할 경로(앱네임 사용) 저장
    else:
        form = QuestionForm()  # form 객체 생성
    return render(request, 'board/question_form.html', {'form': form})


@login_required(login_url='common:login')
def question_modify(request, question_id):
    # 질문 수정
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)  # 수정된 질문 가저장
            question.author = request.user  # 세션 발급
            question.modify_date = timezone.now()  # 수정일
            question.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)  # instance를 쓰면 폼에 내용이 채워짐
    return render(request, 'board/question_form.html', {'form': form})


@login_required(login_url='common:login')
def question_delete(request, question_id):
    # 질문 삭제
    question = get_object_or_404(Question, pk=question_id)
    question.delete()  # 질문 삭제
    return redirect('board:index')