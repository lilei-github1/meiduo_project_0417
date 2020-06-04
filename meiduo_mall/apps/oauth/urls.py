from django.urls import path
from . import views
urlpattens = [
    path('qq/authorization/',views.QQURLView.as_view())
]