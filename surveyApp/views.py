from django.shortcuts import render, redirect, get_object_or_404
from .models import Input, InputCategory, Productive, EmployWelfare
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from .models import InputCategory, Input, Productive, EmployWelfare
from django.db.models import Avg

def index(request):
    categories = InputCategory.objects.all()
    selected_category_id = request.GET.get('category_id')

    # Filter inputs based on the selected category
    if selected_category_id:
        inputs = Input.objects.filter(category_id=selected_category_id).prefetch_related('productives', 'employ_welfares')
    else:
        inputs = Input.objects.all().prefetch_related('productives', 'employ_welfares')

    # Calculate the average of selected items
    selected_productivities = Productive.objects.filter(is_selected=True)
    selected_welfares = EmployWelfare.objects.filter(is_selected=True)

    selected_productivity_avg = selected_productivities.aggregate(avg=Avg('productivity'))['avg']
    selected_employ_welfare_avg = selected_welfares.aggregate(avg=Avg('employ_welfare'))['avg']

    if request.method == 'POST':
        if 'add_category' in request.POST:
            # Handle category creation
            category_name = request.POST.get('category_name')
            if category_name:
                InputCategory.objects.create(name=category_name)
                return redirect('index')

        elif 'edit_productive' in request.POST:
            # Handle productive editing
            productive_id = request.POST.get('productive_id')
            productivity_value = float(request.POST.get('productivity_value'))
            if productive_id and productivity_value is not None:
                productive = get_object_or_404(Productive, id=productive_id)
                productive.productivity = productivity_value
                productive.save()
                return redirect('index')

        elif 'edit_welfare' in request.POST:
            # Handle welfare editing
            welfare_id = request.POST.get('welfare_id')
            employ_welfare_value = float(request.POST.get('employ_welfare_value'))
            if welfare_id and employ_welfare_value is not None:
                employ_welfare = get_object_or_404(EmployWelfare, id=welfare_id)
                employ_welfare.employ_welfare = employ_welfare_value
                employ_welfare.save()
                return redirect('index')

        elif 'select_productive' in request.POST:
            # Handle the selection/unselection of productivity
            productive_id = request.POST.get('select_productive')
            if productive_id:
                productive = get_object_or_404(Productive, id=productive_id)
                productive.is_selected = not productive.is_selected
                productive.save()
                return redirect('index')

        elif 'select_welfare' in request.POST:
            # Handle the selection/unselection of welfare
            welfare_id = request.POST.get('select_welfare')
            if welfare_id:
                employ_welfare = get_object_or_404(EmployWelfare, id=welfare_id)
                employ_welfare.is_selected = not employ_welfare.is_selected
                employ_welfare.save()
                return redirect('index')
        # if request.method == 'POST':
        # Handle the selection/unselection of productivity and welfare
        for key in request.POST:
            if key.startswith('productivity_'):
                productive_id = request.POST.get(key)
                if productive_id:
                    productive = get_object_or_404(Productive, id=productive_id)
                    productive.is_selected = not productive.is_selected
                    productive.save()

            elif key.startswith('welfare_'):
                welfare_id = request.POST.get(key)
                if welfare_id:
                    employ_welfare = get_object_or_404(EmployWelfare, id=welfare_id)
                    employ_welfare.is_selected = not employ_welfare.is_selected
                    employ_welfare.save()
        return redirect('index')  # Redirect to prevent resubmission

    context = {
        'categories': categories,
        'inputs': inputs,
        'selected_productivity_avg': selected_productivity_avg,
        'selected_employ_welfare_avg': selected_employ_welfare_avg,
    }

    return render(request, 'index.html', context)


def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        InputCategory.objects.create(name=category_name)
        return redirect('index')
    return render(request, 'index.html')

def add_input(request):
    if request.method == 'POST':
        input_name = request.POST.get('input_name')
        category_id = request.POST.get('category_id')
        productivity_value = request.POST.get('productivity')
        employ_welfare_value = request.POST.get('employ_welfare')

        category = get_object_or_404(InputCategory, id=category_id)
        new_input = Input.objects.create(name=input_name, category=category)
        Productive.objects.create(category=new_input, productivity=productivity_value)
        EmployWelfare.objects.create(category=new_input, employ_welfare=employ_welfare_value)

        return redirect('index')

def delete_input(request, input_id):
    input_instance = get_object_or_404(Input, id=input_id)
    input_instance.delete()
    return redirect('index')

def edit_input(request, input_id):
    input_instance = get_object_or_404(Input, id=input_id)

    if request.method == 'POST':
        input_name = request.POST.get('input_name')
        category_id = request.POST.get('category_id')
        productivity_value = request.POST.get('productivity')
        employ_welfare_value = request.POST.get('employ_welfare')

        input_instance.name = input_name
        input_instance.category_id = category_id

        if input_instance.productives.exists():
            productive = input_instance.productives.first()
            productive.productivity = productivity_value
            productive.save()
        else:
            Productive.objects.create(category=input_instance, productivity=productivity_value)

        if input_instance.employ_welfares.exists():
            welfare = input_instance.employ_welfares.first()
            welfare.employ_welfare = employ_welfare_value
            welfare.save()
        else:
            EmployWelfare.objects.create(category=input_instance, employ_welfare=employ_welfare_value)

        input_instance.save()
        return redirect('index')

    context = {
        'input': input_instance,
        'categories': InputCategory.objects.all(),
    }

    return render(request, 'edit.html', context)

def edit_productive(request):
    if request.method == 'POST':
        productive_id = request.POST.get('productive_id')
        productivity_value = request.POST.get('edit_productivity')

        productive = get_object_or_404(Productive, id=productive_id)
        productive.productivity = productivity_value
        productive.save()

        return redirect('index')

def edit_welfare(request):
    if request.method == 'POST':
        welfare_id = request.POST.get('welfare_id')
        employ_welfare_value = request.POST.get('edit_employ_welfare')

        welfare = get_object_or_404(EmployWelfare, id=welfare_id)
        welfare.employ_welfare = employ_welfare_value
        welfare.save()

        return redirect('index')