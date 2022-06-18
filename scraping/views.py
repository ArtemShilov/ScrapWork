from django.shortcuts import render
from .models import Vacancy
from .forms import FindForm
from django.core.paginator import Paginator


def home_view(request):
    form = FindForm()
    return render(request, 'home.html', {'form': form})


def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    page_obj = []
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language
        qs = Vacancy.objects.filter(**_filter)

        paginator = Paginator(qs, 12)  # Show 25 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    return render(request, 'list.html', {'object_list': page_obj, 'form': form})
