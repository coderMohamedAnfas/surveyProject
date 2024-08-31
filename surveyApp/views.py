from django.shortcuts import render, redirect, get_object_or_404
from .models import InputCategory, Input, Productive, EmployWelfare
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

def add_input(request):
    if request.method == 'POST':
        input_name = request.POST.get('input_name')
        category_id = request.POST.get('category_id')
        productivity_value = request.POST.get('productivity')
        employ_welfare_value = request.POST.get('employ_welfare')
        
        category = InputCategory.objects.get(id=category_id)
        new_input = Input.objects.create(name=input_name, category=category)
        Productive.objects.create(category=new_input, productivity=productivity_value)
        EmployWelfare.objects.create(category=new_input, employ_welfare=employ_welfare_value)

        return redirect('index')

    categories = InputCategory.objects.all()
    context = {
        'categories': categories,
    }
    
    return render(request, 'index.html', context)

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
        input_instance.productive.productivity = productivity_value
        input_instance.employwelfare.employ_welfare = employ_welfare_value
        
        input_instance.save()
        input_instance.productive.save()
        input_instance.employwelfare.save()

        return redirect('index')

    categories = InputCategory.objects.all()
    context = {
        'input': input_instance,
        'categories': categories,
    }
    
    return render(request, 'edit.html', context)

def edit_productive(request, productive_id):
    productive = get_object_or_404(Productive, id=productive_id)
    if request.method == 'POST':
        productive.productivity = float(request.POST.get('productivity'))
        productive.save()
        return redirect('index')  # Redirect after saving
    return render(request, 'edit.html', {'productive': productive})

def edit_employ_welfare(request, employ_welfare_id):
    employ_welfare = get_object_or_404(EmployWelfare, id=employ_welfare_id)
    if request.method == 'POST':
        employ_welfare.employ_welfare = float(request.POST.get('employ_welfare'))
        employ_welfare.save()
        return redirect('index')  # Redirect after saving
    return render(request, 'edit.html', {'employ_welfare': employ_welfare})

def edit_category(request, category_id):
    category = get_object_or_404(InputCategory, id=category_id)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.save()
        return redirect('index')  # Redirect after saving
    return render(request, 'edit.html', {'category': category})
