# core/views.py
from django.shortcuts import render
from news.models import NewsItem
from .models import CpdArticle, History, Formation
import logging
from members.models import News, Job

logger = logging.getLogger(__name__)

def home(request):
    news_items = NewsItem.objects.all()[:3]
    cpd_articles = CpdArticle.objects.all()[:3]
    context = {
        'news_items': news_items,
        'news_loading': False,
        'cpd_articles': cpd_articles,
        'cpd_loading': False,
    }
    return render(request, 'core/home.html', context)

def news_list(request):
    news_items = News.objects.all().order_by('-date')
    return render(request, 'core/news.html', {'news_items': news_items})

def placeholder(request):
    return render(request, 'core/placeholder.html', {'message': 'This page is under construction.'})

def history(request):
    history_data = History.objects.first()
    context = {
        'history_content': history_data.history_content if history_data else "No history content available",
        'change_designation': history_data.change_designation if history_data else "No designation change info available",
        'salary_scale': history_data.salary_scale if history_data else "No salary scale info available",
        'training_institutions': history_data.training_institutions if history_data else "No training institutions info available",
    }
    logger.debug(f"History context: {context}")
    return render(request, 'core/history.html', context)


def formation_adtn(request):
    formation_data = Formation.objects.first()
    context = {
        'formation_content': formation_data.formation_content if formation_data else "No formation content available",
    }
    logger.debug(f"Formation context: {context}")
    return render(request, 'core/formation_adtn.html', context)
