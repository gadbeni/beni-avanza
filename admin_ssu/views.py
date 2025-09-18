from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
# formularios
from .forms import EmailAuthenticationForm
from . import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib import messages
#json
from django.http import JsonResponse
from django.core import serializers

# models
from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import Concat

# views
from django.contrib.auth.views import LoginView
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy
# Create your views here.
# views.py
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

class EmailLoginView(LoginView):
    # Descomentar para autenticar con email
    # form_class = EmailAuthenticationForm
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('admin_ssu:home')
        return super().dispatch(request, *args, **kwargs)
    
    
class HomePageView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        return render(request, 'admin_ssu/home.html')


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'admin_ssu/users/user_profile.html'  # Asegúrate de cambiar esto a tu plantilla real
    context_object_name = 'user'

    def get_object(self):
        return self.request.user
      

# Usuarios
class UserListView(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    model = User
    template_name = 'admin_ssu/users/user_list.html'
    context_object_name = 'users'
    paginate_by = 10
    permission_required = 'auth.view_user'
    
    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Usuarios'
        return context
    

class UserSearchView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        if query:
            users = User.objects.annotate(
                full_name=Concat('first_name', V(' '), 'last_name')
            ).filter(Q(full_name__icontains=query) | Q(username__icontains=query))
        else:
            users = User.objects.all()
        users_json = serializers.serialize('json', users)
        return JsonResponse(users_json, safe=False)
    

class UserCreateView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = User
    form_class = forms.CustomUserCreationForm
    template_name = 'admin_ssu/users/user_create.html'
    success_url = reverse_lazy('admin_ssu:user_view')
    permission_required = 'auth.add_user'
    

class UserEditView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = User
    form_class = forms.CustomUserEditForm
    # form_class = UserChangeForm
    template_name = 'admin_ssu/users/user_edit.html'
    success_url = reverse_lazy('admin_ssu:user_view')
    permission_required = 'auth.change_user'
    
    
class UserChangePasswordView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user)
        return render(request, 'admin_ssu/users/user_change_password.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important, to update the session with the new password
            messages.success(request, 'Tu contraseña fue actualizada exitosamente!')
            return redirect('admin_ssu:user_profile')
        else:
            messages.error(request, 'Por favor corrige el error abajo.')
        return render(request, 'admin_ssu/users/user_change_password.html', {'form': form})


class AdminChangePasswordView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'auth.change_user'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=kwargs['pk'])
        form = SetPasswordForm(user)
        return render(request, 'admin_ssu/users/admin_change_password.html', {'form': form, 'user': user})

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=kwargs['pk'])
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'La contraseña fue actualizada exitosamente!')
            return redirect('admin_ssu:user_view')
        else:
            messages.error(request, 'Por favor corrige el error abajo.')
        return render(request, 'admin_ssu/users/admin_change_password.html', {'form': form, 'user': user})
    

class UserDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = User
    # template_name = 'admin_ssu/users/user_confirm_delete.html'
    success_url = reverse_lazy('admin_ssu:user_view')
    permission_required = 'auth.delete_user'
    

class UserDetailView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    model = User
    template_name = 'admin_ssu/users/user_detail.html'
    context_object_name = 'user'
    permission_required = 'auth.view_user'
    
#fin usuarios

# Grupos
class GroupListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = Group
    template_name = 'admin_ssu/groups/group_list.html'
    context_object_name = 'groups'
    paginate_by = 10
    permission_required = 'auth.view_group'
    
    def get_queryset(self):
        queryset = Group.objects.all().order_by('-id')
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context

    
class GroupCreateView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = Group
    template_name = 'admin_ssu/groups/group_add_edit.html'
    form_class = forms.GroupForm
    success_url = reverse_lazy('admin_ssu:group_list')
    permission_required = 'auth.add_group'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        content_types = ContentType.objects.all().order_by('model')
        permissions_by_group = []
        for content_type in content_types:
            permissions_of_model = Permission.objects.filter(content_type=content_type)
            if permissions_of_model:
                permissions_by_group.append((content_type, permissions_of_model))
        context['permissions_by_group'] = permissions_by_group
        
        context['action'] = 'Crear'
        return context
    

class GroupUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = Group
    template_name = 'admin_ssu/groups/group_add_edit.html'
    form_class = forms.GroupForm
    success_url = reverse_lazy('admin_ssu:group_list')
    permission_required = 'auth.change_group'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        content_types = ContentType.objects.all().order_by('model')
        permissions_by_group = []
        for content_type in content_types:
            permissions_of_model = Permission.objects.filter(content_type=content_type)
            if permissions_of_model:
                permissions_by_group.append((content_type, permissions_of_model))
        context['permissions_by_group'] = permissions_by_group
        context['group_permissions'] = self.object.permissions.all()
        
        context['action'] = 'Editar'
        return context
    

class GroupDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = Group
    # template_name = 'admin_ssu/users/user_confirm_delete.html'
    success_url = reverse_lazy('admin_ssu:group_list')
    permission_required = 'auth.delete_group'
    
    
# permisos
class AllPermissionsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Permission
    template_name = 'admin_ssu/permissions/permissions_list.html'
    paginate_by = 10
    permission_required = 'auth.view_permission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context