from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, TemplateView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from .models import Pothole, Category, CategoryPrivate, Agent
from .forms import PotholeForm, ProyectForm, AgentForm
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.core.exceptions import PermissionDenied
import json
from django.conf import settings
import os
from django.db.models import Count

# Create your views here.
class CategoryBrowseView(LoginRequiredMixin, PermissionRequiredMixin,TemplateView):
    template_name = 'report_potholes/category/browse.html'
    permission_required = 'report_potholes.view_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Categorías'
        return context


class CategoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Category
    template_name = 'report_potholes/category/list.html'
    permission_required = 'report_potholes.view_category'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)


class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Category
    template_name = 'report_potholes/category/add_edit.html'
    fields = ('name', 'icon')
    success_url = reverse_lazy('admin_ssu:report_potholes:category_browse')
    permission_required = 'report_potholes.add_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Crear'
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'

class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Category
    template_name = 'report_potholes/category/add_edit.html'
    fields = ('name', 'icon')
    success_url = reverse_lazy('admin_ssu:report_potholes:category_browse')
    permission_required = 'report_potholes.change_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Actualizar'
        return context

class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Category
    permission_required = 'report_potholes.delete_category'
    # template_name = 'category_delete.html'
    success_url = reverse_lazy('admin_ssu:report_potholes:category_browse')

#Pothole admin
class PotholeBrowseView(LoginRequiredMixin, PermissionRequiredMixin,TemplateView):
    template_name = 'report_potholes/potholes/browse.html'
    permission_required = 'report_potholes.view_pothole'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search', '')
        context['title'] = 'Proyectos Registrados'
        return context
    

class PotholesListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Pothole
    template_name = 'report_potholes/potholes/list.html'
    context_object_name = 'potholes'
    paginate_by = 10
    permission_required = 'report_potholes.view_pothole'

    def get_queryset(self):
        queryset = Pothole.objects.filter(approved=True)
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)


class PotholeCreateView(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    """Vista para reportar un proyecto."""
    model = Pothole
    form_class = ProyectForm
    # template_name = 'report_potholes/pothole_add.html'
    # success_url = reverse_lazy('thanks')
    template_name = 'report_potholes/potholes/add_edit.html'
    success_url = reverse_lazy('admin_ssu:report_potholes:potholes_browse')
    permission_required = 'report_potholes.add_pothole'
    
    def form_valid(self, form):
        form.instance.approved = True
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Crear'
        return context
    

class PotholeUpdateView(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    """Vista para actualizar un proyecto."""
    model = Pothole
    form_class = ProyectForm
    template_name = 'report_potholes/potholes/add_edit.html'
    success_url = reverse_lazy('admin_ssu:report_potholes:potholes_browse')
    permission_required = 'report_potholes.change_pothole'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Editar'
        return context
    

class PotholeDetailviewAdmin(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Pothole
    template_name = 'report_potholes/potholes/detail.html'
    context_object_name = 'pothole'
    permission_required = 'report_potholes.view_pothole'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        return Pothole.objects.filter(approved=True)

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)

# end pothole admin   


    

class PotholeThanksView(TemplateView):
    """vista de agradecimiento."""
    template_name = 'report_potholes/pothole_thanks.html'


class ApprovedPotholeMapView(TemplateView):
    """Muestra un mapa"""
    template_name = 'report_potholes/pothole_maps.html'  # reemplaza con el nombre de tu plantilla

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.request.GET.get('category')
        if category:
            potholes = Pothole.objects.filter(approved=True, category__id=category)
        else:
            potholes = Pothole.objects.filter(approved=True)
        potholes_data = []
        for pothole in potholes:
            pothole_data = {
                'title': pothole.title.upper() if pothole.title else 'SIN TÍTULO',
                'latitude': pothole.latitude,
                'longitude': pothole.longitude,
                'url': reverse('pothole_detail', args=[pothole.id]),
                'image': pothole.thumbnail.url if pothole.thumbnail else None,
                'category_icon': pothole.category.icon.url if pothole.category and pothole.category.icon else None
            }
            potholes_data.append(pothole_data)
        context['potholes'] = json.dumps(potholes_data, cls=DjangoJSONEncoder, ensure_ascii=False)
        context['total_potholes'] = potholes.count()
        context['categories'] = Category.objects.all()
        context['categories'] = Category.objects.annotate(num_photos=Count('pothole')).filter(num_photos__gt=0)
        return context
    

class PotholeDetailView(DetailView):
    """Muestra los detalles"""
    model = Pothole
    template_name = 'report_potholes/pothole_detail.html'
    context_object_name = 'pothole'


# administrador
class UnapprovedPotholeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Muestra"""
    model = Pothole
    template_name = 'report_potholes/potholes/pothole_solicitude.html'  # reemplaza con el nombre de tu plantilla
    context_object_name = 'potholes'
    paginate_by = 10
    permission_required = 'report_potholes.view_pothole'

    def get_queryset(self):
        return Pothole.objects.filter(approved=False)


@login_required
def approve_pothole(request, pk):
    """Aprueba"""
    if not request.user.has_perm('app_name.can_approve_pothole'):
        raise PermissionDenied
    pothole = get_object_or_404(Pothole, pk=pk)
    pothole.approved = True
    pothole.save()
    return redirect('admin_ssu:report_potholes:solicitude_potholes')
    

class PotholeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Vista para descartar y eliminar"""
    model = Pothole
    success_url = reverse_lazy('admin_ssu:report_potholes:solicitude_potholes')
    permission_required = 'report_potholes.delete_pothole'
    

class PotholePointDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Vista para descartar y eliminar"""
    model = Pothole
    success_url = reverse_lazy('admin_ssu:report_potholes:potholes_browse')
    permission_required = 'report_potholes.delete_pothole'
    

from math import radians, sin, cos, sqrt, atan2

class PotholeDetailMapView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Pothole
    template_name = 'report_potholes/potholes/pothole_detail.html'
    context_object_name = 'pothole'
    permission_required = 'report_potholes.view_pothole'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Radio de la Tierra en kilómetros
        R = 6371.0

        lat1 = radians(self.object.latitude)
        lon1 = radians(self.object.longitude)

        nearby_potholes = []
        for pothole in Pothole.objects.filter(approved=True):
            lat2 = radians(pothole.latitude)
            lon2 = radians(pothole.longitude)

            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = R * c

            # Si la distancia es menor a 1 kilómetro, añade el  a la lista
            if distance < 1:
                nearby_potholes.append({'latitude': float(pothole.latitude), 'longitude': float(pothole.longitude),'url': reverse('pothole_detail', args=[pothole.id])})

        context['potholejs'] = {'latitude': float(self.object.latitude), 'longitude': float(self.object.longitude)}
        context['nearby_potholes'] = nearby_potholes
        return context
    

#Category private
class CategoryPrivateBrowseView(LoginRequiredMixin, PermissionRequiredMixin,TemplateView):
    template_name = 'report_potholes/category_private/browse.html'
    permission_required = 'report_potholes.view_categoryprivate'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Categorías privadas'
        return context


class CategoryPrivateListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CategoryPrivate
    template_name = 'report_potholes/category_private/list.html'
    permission_required = 'report_potholes.view_categoryprivate'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)


class CategoryPrivateCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = CategoryPrivate
    template_name = 'report_potholes/category_private/add_edit.html'
    fields = ('name', 'icon')
    success_url = reverse_lazy('admin_ssu:report_potholes:categoryp_browse')
    permission_required = 'report_potholes.add_categoryprivate'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Crear'
        return context
    

class CategoryPrivateUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = CategoryPrivate
    template_name = 'report_potholes/category_private/add_edit.html'
    fields = ('name', 'icon')
    success_url = reverse_lazy('admin_ssu:report_potholes:categoryp_browse')
    permission_required = 'report_potholes.change_categoryprivate'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Actualizar'
        return context
    

class CategoryPrivateDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = CategoryPrivate
    permission_required = 'report_potholes.delete_categoryprivate'
    success_url = reverse_lazy('admin_ssu:report_potholes:categoryp_browse')


#Agent admin
class AgentBrowseView(LoginRequiredMixin, PermissionRequiredMixin,TemplateView):
    template_name = 'report_potholes/agent/browse.html'
    permission_required = 'report_potholes.view_agent'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search', '')
        context['title'] = 'Dirigentes'
        return context
    

class AgentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Agent
    template_name = 'report_potholes/agent/list.html'
    context_object_name = 'agents'
    paginate_by = 10
    permission_required = 'report_potholes.view_agent'

    def get_queryset(self):
        queryset = Agent.objects.filter(active=True)
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(full_name__icontains=search)
        return queryset
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)


class AgentCreateView(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    """Vista para crear un Agente."""
    model = Agent
    form_class = AgentForm
    template_name = 'report_potholes/agent/add_edit.html'
    success_url = reverse_lazy('admin_ssu:report_potholes:agent_browse')
    permission_required = 'report_potholes.add_agent'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Crear'
        return context
    

class AgentUpdateView(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    """Vista para actualizar un agente."""
    model = Agent
    form_class = AgentForm
    template_name = 'report_potholes/agent/add_edit.html'
    success_url = reverse_lazy('admin_ssu:report_potholes:agent_browse')
    permission_required = 'report_potholes.change_agent'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Editar'
        return context
    

class AgentDetailview(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Agent
    template_name = 'report_potholes/agent/detail.html'
    context_object_name = 'agent'
    permission_required = 'report_potholes.view_agent'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CategoryPrivate.objects.all()
        return context

    def get_queryset(self):
        return Agent.objects.filter(active=True)

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)


class AgentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Vista para eliminar Agentes"""
    model = Agent
    success_url = reverse_lazy('admin_ssu:report_potholes:agent_browse')
    permission_required = 'report_potholes.delete_agent'


class AgentMapView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Muestra un mapa"""
    template_name = 'report_potholes/agent/maps.html'
    permission_required = 'report_potholes.view_agent'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.request.GET.get('category')
        if category:
            agents = Agent.objects.filter(active=True, category__id=category)
        else:
            agents = Agent.objects.filter(active=True)
        agents_data = []
        for agent in agents:
            agent_data = {
                'title': agent.full_name.upper() if agent.full_name else 'SIN TÍTULO',
                'latitude': agent.latitude,
                'longitude': agent.longitude,
                'url': reverse('admin_ssu:report_potholes:agent_detail', args=[agent.id]),
                'image': agent.thumbnail.url if agent.thumbnail else None,
                'category_icon': agent.category.icon.url if agent.category and agent.category.icon else None
            }
            agents_data.append(agent_data)
        context['agents'] = json.dumps(agents_data, cls=DjangoJSONEncoder, ensure_ascii=False)
        context['total_agents'] = agents.count()
        context['categories'] = CategoryPrivate.objects.all()
        context['categories'] = CategoryPrivate.objects.annotate(num_agents=Count('agent')).filter(num_agents__gt=0)
        return context
# end pothole admin