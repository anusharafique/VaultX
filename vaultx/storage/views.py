from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import VaultItem


@login_required
def dashboard(request):
    items = VaultItem.objects.filter(
        user=request.user
    ).order_by('-created_at')

    search = request.GET.get('search', '')
    category = request.GET.get('category', '')

    if search:
        items = items.filter(title__icontains=search)

    if category:
        items = items.filter(category=category)

    all_items = VaultItem.objects.filter(user=request.user)

    context = {
        'items': items,
        'photos': all_items.filter(category='photo').count(),
        'documents': all_items.filter(category='document').count(),
        'notes': all_items.filter(category='note').count(),
        'search': search,
        'selected_category': category,
    }

    return render(request, 'storage/dashboard.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        return render(
            request,
            'storage/login.html',
            {'error': 'Invalid username or password.'}
        )

    return render(request, 'storage/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(
                request,
                'storage/register.html',
                {'error': 'Passwords do not match.'}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                'storage/register.html',
                {'error': 'Username already exists.'}
            )

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('login')

    return render(request, 'storage/register.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def add_item(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        description = request.POST.get('description')
        file = request.FILES.get('file')

        VaultItem.objects.create(
            user=request.user,
            title=title,
            category=category,
            description=description,
            file=file
        )

        return redirect('dashboard')

    return render(request, 'storage/add_item.html')

@login_required
def edit_item(request, item_id):
    item = get_object_or_404(
        VaultItem,
        id=item_id,
        user=request.user
    )

    if request.method == 'POST':
        item.title = request.POST.get('title')
        item.category = request.POST.get('category')
        item.description = request.POST.get('description')

        if request.FILES.get('file'):
            item.file = request.FILES.get('file')

        item.save()

        return redirect('dashboard')

    return render(
        request,
        'storage/edit_item.html',
        {'item': item}
    )
def delete_item(request, item_id):
    item = get_object_or_404(
        VaultItem,
        id=item_id,
        user=request.user
    )

    if request.method == 'POST':
        item.delete()

    return redirect('dashboard')