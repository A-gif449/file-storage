from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from .models import File, FileShare
from .forms import FileUploadForm, FileShareForm, UserRegisterForm
import os

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'storage_app/register.html', {'form': form})

@login_required
def dashboard(request):
    # Get user's files and files shared with user
    owned_files = File.objects.filter(owner=request.user)
    shared_files = File.objects.filter(
        shared_with__user=request.user,
        shared_with__permission__in=['view', 'edit']
    ).distinct()

    context = {
        'owned_files': owned_files,
        'shared_files': shared_files,
        'total_files': owned_files.count() + shared_files.count(),
        'total_size': sum(f.file_size for f in owned_files)
    }
    return render(request, 'storage_app/dashboard.html', context)

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.owner = request.user
            file.save()
            messages.success(request, 'File uploaded successfully!')
            return redirect('dashboard')
    else:
        form = FileUploadForm()
    return render(request, 'storage_app/upload.html', {'form': form})

@login_required
def file_list(request):
    files = File.objects.filter(owner=request.user)
    return render(request, 'storage_app/file_list.html', {'files': files})

@login_required
def share_file(request, file_id):
    file = get_object_or_404(File, id=file_id, owner=request.user)
    
    if request.method == 'POST':
        form = FileShareForm(request.POST, user=request.user)
        if form.is_valid():
            users = form.cleaned_data['users']
            permission = form.cleaned_data['permission']
            can_download = form.cleaned_data['can_download']

            # Remove existing shares for this file
            FileShare.objects.filter(file=file).delete()

            # Create new shares
            for user in users:
                FileShare.objects.create(
                    file=file,
                    user=user,
                    permission=permission,
                    can_download=can_download
                )

            messages.success(request, f'File shared with {users.count()} users!')
            return redirect('dashboard')
    else:
        form = FileShareForm(user=request.user)

    return render(request, 'storage_app/share_file.html', {'form': form, 'file': file})

@login_required
def delete_file(request, file_id):
    file = get_object_or_404(File, id=file_id, owner=request.user)
    
    if request.method == 'POST':
        file.file.delete()
        file.delete()
        messages.success(request, 'File deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'storage_app/confirm_delete.html', {'file': file})

@login_required
def view_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    
    # Check permissions
    if file.owner != request.user:
        share = FileShare.objects.filter(file=file, user=request.user).first()
        if not share or share.permission not in ['view', 'edit']:
            return HttpResponseForbidden("You don't have permission to view this file.")
    
    context = {'file': file}
    return render(request, 'storage_app/view_file.html', context)

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'storage_app/home.html')