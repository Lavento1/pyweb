from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from board.models import Question, Answer
from board.forms import QuestionForm, AnswerForm


def index(request):
    return render(request, 'board/index.html')


def board_list(request):
    # 질문 목록
    # question_list = Question.objects.all()  # db 전체 조회
    # 작성일 기준 내림차순( - 기호 사용)
    question_list = Question.objects.order_by('-create_date')
    
    # 페이지 처리
    page = request.GET.get('page', 1)   # 127.0.0.1:8000/
    paginator = Paginator(question_list, 10)    # 페이지당 10개 씩 설정
    page_obj = paginator.get_page(page)  # 페이지 가져오기

    return render(request, 'board/question_list.html',
                  {'question_list': page_obj})
    # return HttpResponse("pyweb 사이트입니다.")


def detail(request, question_id):
    # 질문 / 답변 상세 - 해당 id의 질문
    # question = Question.objects.get(id=question_id)
    # 경로에 오류가 있을 때 404로 처리(페이지가 없음)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'board/detail.html', {'question': question})


@login_required(login_url='common:login')
def question_create(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)   # 자료 전달받음(request.POST)
        if form.is_valid():
            question = form.save(commit=False)  # 가저장(날짜를 전달받지 못했기에 가저장)
            question.create_date = timezone.now()   # 날짜 시간 저장
            question.author = request.user  # 세션에 있는 유저 저장
            question.save()     # 실제 저장
            return redirect('board:index')  # 이동할 경로(앱네임 사용) 저장
    else:
        form = QuestionForm()   # form 객체 생성
    return render(request, 'board/question_form.html', {'form': form})


@login_required(login_url='common:login')
def answer_create(request, question_id):
    # 답변 등록
    question = Question.objects.get(id=question_id) # 해당 id의 질문 객체 생성
    if request.method == "POST":
        form = AnswerForm(request.POST) # 입력값 전달받음
        if form.is_valid():
            answer = form.save(commit=False)  # 내용만 저장됨
            answer.create_date = timezone.now() # 작성일
            answer.author = request.user    # 세션 발급
            answer.question = question  # 외래키 질문 저장
            answer.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}

    return render(request, 'board/detail.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    # 질문 수정
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)  # 수정된 질문 가저장
            question.author = request.user  # 세션 발급
            question.modify_date = timezone.now()   # 수정일
            question.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)  # instance를 쓰면 폼에 내용이 채워짐
    return render(request, 'board/question_form.html', {'form': form})


@login_required(login_url='common:login')
def question_delete(request, question_id):
    # 질문 삭제
    question = get_object_or_404(Question, pk=question_id)
    question.delete()   # 질문 삭제
    return redirect('board:index')


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    # 답변 수정
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)  # 수정된 답변 가저장
            answer.author = request.user  # 세션 발급
            answer.modify_date = timezone.now()  # 수정일
            answer.save()
            return redirect('board:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    return render(request, 'board/answer_form.html', {'form': form})


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    # 질문 삭제
    answer = get_object_or_404(Answer, pk=answer_id)
    answer.delete()   # 질문 삭제
    return redirect('board:detail', question_id=answer.question.id)

