from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Survey, Question, Answer, Choice
import json


def survey_list(request):
    """Список доступных опросов"""
    surveys = Survey.objects.filter(is_active=True)
    return render(request, 'surveys/survey_list.html', {'surveys': surveys})


def survey_detail(request, survey_id):
    """Страница с вопросами опроса"""
    survey = get_object_or_404(Survey, id=survey_id, is_active=True)
    questions = survey.questions.all()

    # Проверяем, не проходил ли уже этот пользователь опрос
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    # Для анонимных опросов проверяем по сессии
    if survey.is_anonymous:
        has_answered = Answer.objects.filter(
            question__survey=survey,
            session_key=session_key
        ).exists()
    else:
        # Для неанонимных - по пользователю
        if request.user.is_authenticated:
            has_answered = Answer.objects.filter(
                question__survey=survey,
                employee=request.user
            ).exists()
        else:
            has_answered = False

    if has_answered:
        messages.warning(request, 'Вы уже проходили этот опрос!')
        return redirect('survey_thanks')

    if request.method == 'POST':
        # Сохраняем ответы
        for question in questions:
            answer_key = f'question_{question.id}'
            if answer_key in request.POST:
                answer_value = request.POST[answer_key]

                # Сохраняем ответ в зависимости от типа вопроса
                if question.question_type == 'rating':
                    Answer.objects.create(
                        question=question,
                        rating_value=int(answer_value),
                        employee=request.user if not survey.is_anonymous else None,
                        session_key=session_key if survey.is_anonymous else ''
                    )
                elif question.question_type == 'text':
                    Answer.objects.create(
                        question=question,
                        text_value=answer_value,
                        employee=request.user if not survey.is_anonymous else None,
                        session_key=session_key if survey.is_anonymous else ''
                    )
                elif question.question_type == 'choice':
                    choice = get_object_or_404(Choice, id=int(answer_value))
                    Answer.objects.create(
                        question=question,
                        choice_value=choice,
                        employee=request.user if not survey.is_anonymous else None,
                        session_key=session_key if survey.is_anonymous else ''
                    )

        messages.success(request, 'Спасибо! Ваши ответы сохранены.')
        return redirect('survey_thanks')

    return render(request, 'surveys/survey_detail.html', {
        'survey': survey,
        'questions': questions,
    })


def survey_thanks(request):
    """Страница благодарности после прохождения опроса"""
    return render(request, 'surveys/thanks.html')


from django.db.models import Count, Avg, Q
from django.contrib.auth.decorators import login_required


@login_required
def survey_results(request, survey_id):
    """Дашборд с результатами опроса для HR"""
    survey = get_object_or_404(Survey, id=survey_id)
    questions = survey.questions.all()

    results = {}
    for question in questions:
        answers = Answer.objects.filter(question=question)
        total_answers = answers.count()

        if question.question_type == 'rating':
            avg_rating = answers.aggregate(Avg('rating_value'))['rating_value__avg']
            rating_distribution = {
                1: answers.filter(rating_value=1).count(),
                2: answers.filter(rating_value=2).count(),
                3: answers.filter(rating_value=3).count(),
                4: answers.filter(rating_value=4).count(),
                5: answers.filter(rating_value=5).count(),
            }
            results[question.id] = {
                'type': 'rating',
                'text': question.text,
                'total': total_answers,
                'avg': round(avg_rating, 2) if avg_rating else 0,
                'distribution': rating_distribution,
            }

        elif question.question_type == 'text':
            text_answers = [a.text_value for a in answers if a.text_value]
            results[question.id] = {
                'type': 'text',
                'text': question.text,
                'total': total_answers,
                'answers': text_answers[:20],  # последние 20 ответов
            }

        elif question.question_type == 'choice':
            choice_stats = {}
            for choice in question.choices.all():
                count = answers.filter(choice_value=choice).count()
                choice_stats[choice.text] = {
                    'count': count,
                    'percent': round(count / total_answers * 100, 1) if total_answers > 0 else 0
                }
            results[question.id] = {
                'type': 'choice',
                'text': question.text,
                'total': total_answers,
                'stats': choice_stats,
            }

    return render(request, 'surveys/survey_results.html', {
        'survey': survey,
        'results': results,
        'questions': questions,
    })


@login_required
def survey_list_hr(request):
    """Список опросов для HR с результатами"""
    surveys = Survey.objects.all().order_by('-created_at')
    return render(request, 'surveys/survey_list_hr.html', {'surveys': surveys})


from django.contrib.auth import logout
from django.shortcuts import redirect


def custom_logout(request):
    logout(request)
    return redirect('custom_logout_success')


def logout_success(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Выход из системы | PulseHR</title>
        <link rel="stylesheet" href="/static/surveys/css/style.css">
    </head>
    <body class="logout-page">
        <div class="logout-container">
            <h1>✅ Вы вышли из системы</h1>
            <p>Спасибо, что использовали PulseHR</p>
            <a href="/" class="btn">🏠 На главную</a>
            <a href="/accounts/login/" class="btn btn-results">🔐 Войти снова</a>
        </div>
    </body>
    </html>
    """
    from django.http import HttpResponse
    return HttpResponse(html)
