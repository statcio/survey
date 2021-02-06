from django.urls import path

from . import apiviews

app_name = 'polls'
urlpatterns = [
    path('login/', apiviews.login, name='login'),
    path('polls/create/', apiviews.polls_view, name='poll_create'),
    path('polls/update/<int:poll_id>/', apiviews.poll_detail_view, name='poll_update'),
    path('polls/view/', apiviews.poll_view, name='poll_view'),
    path('polls/view/current/', apiviews.current_poll_view, name='current_poll_view'),
    path('question/create/', apiviews.questions_view, name='question_create'),
    path('question/update/<int:question_id>/', apiviews.question_detail_view, name='question_update'),
    path('option/create/', apiviews.options_view, name='option_create'),
    path('option/update/<int:option_id>/', apiviews.option_detail_view, name='option_update'),
    path('reply/create/', apiviews.reply_create, name='reply_create'),
    path('reply/view/<int:user_id>/', apiviews.reply_view, name='reply_view'),
    path('reply/update/<int:reply_id>/', apiviews.reply_update, name='reply_update'),

]
