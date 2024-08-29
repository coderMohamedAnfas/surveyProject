from django.shortcuts import render, redirect, get_object_or_404
from .models import InputCategory, Input, Productive, EmployWelfare
from django.db.models import Avg

def index(request):
    selected_productivity_avg = Productive.objects.filter(is_selected=True).aggregate(Avg('productivity'))['productivity__avg']
    selected_employ_welfare_avg = EmployWelfare.objects.filter(is_selected=True).aggregate(Avg('employ_welfare'))['employ_welfare__avg']

    context = {
        'selected_productivity_avg': selected_productivity_avg,
        'selected_employ_welfare_avg': selected_employ_welfare_avg,
        'categories': InputCategory.objects.all(),
    }
    return render(request, 'index.html', context)

def data_management_view(request):
    category_id = request.GET.get('category_id')
    if category_id:
        inputs = Input.objects.filter(category_id=category_id)
    else:
        inputs = Input.objects.all()

    if request.method == 'POST':
        input_id = request.POST.get('input_id')
        if 'select_productivity' in request.POST:
            productive = get_object_or_404(Productive, category_id=input_id)
            productive.is_selected = not productive.is_selected
            productive.save()
        elif 'select_employ_welfare' in request.POST:
            employ_welfare = get_object_or_404(EmployWelfare, category_id=input_id)
            employ_welfare.is_selected = not employ_welfare.is_selected
            employ_welfare.save()

    context = {
        'inputs': inputs,
        'categories': InputCategory.objects.all(),
    }
    return render(request, 'data_management.html', context)

def add_input_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        InputCategory.objects.create(name=name)
        return redirect('data_management_view')

def add_input(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category_id')
        category = get_object_or_404(InputCategory, id=category_id)
        Input.objects.create(name=name, category=category)
        return redirect('data_management_view')
