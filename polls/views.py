from django.shortcuts import render
from polls.models import Question, Choice


def index(request):
    # 설문 메인
    poll_list = Question.objects.all()
    context = {'poll_list': poll_list}
    return render(request, 'polls/poll_list.html', context)


def detail(request, pk):
    # 해당 id(순번)로 자료를 조회
    question = Question.objects.get(id=pk)
    return render(request, 'polls/detail.html', {'question': question})


def vote(request, pk):
    question = Question.objects.get(id=pk)

    # 선택 자료 넘겨 받음
    try:
        choice_id = request.POST['choice']
        sel_choice = question.choice_set.get(id=choice_id)
    except:
        return render(request, 'polls/detail.html',
                      {'question': question, 'error': '선택을 확인해주세요.'})
    else:
        sel_choice.votes = sel_choice.votes + 1
        sel_choice.save()
        return render(request, 'polls/vote_result.html', {'question': question})

