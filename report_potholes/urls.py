from django.urls import path, include
from . import views

app_name = 'report_potholes'

urlpatterns = [
    # admin categories
    path('category/', views.CategoryBrowseView.as_view(), name='category_browse'),
    path('category/list', views.CategoryListView.as_view(), name='category_list'),
    # path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('category/add/', views.CategoryCreateView.as_view(), name='category_add'),
    path('category/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    # admin potholes
    path('proyects',views.PotholeBrowseView.as_view(), name='potholes_browse'),
    path('proyects/list',views.PotholesListView.as_view(), name='potholes_list'),
    path('proyects/<int:pk>/detalles', views.PotholeDetailviewAdmin.as_view(), name='pothole_detail'),
    path('proyects/add/', views.PotholeCreateView.as_view(), name='pothole_add'),
    path('proyects/<int:pk>/edit/', views.PotholeUpdateView.as_view(), name='pothole_edit'),


    # path('solicitude', views.UnapprovedPotholeListView.as_view(), name='solicitude_potholes'),
    # path('approve_pothole/<int:pk>/', views.approve_pothole, name='approve_pothole'),
    path('delete/<int:pk>/', views.PotholeDeleteView.as_view(), name='delete_pothole'),
    path('deletepoint/<int:pk>/', views.PotholePointDeleteView.as_view(), name='delete_potholepoint'),
    # path('pothole/<int:pk>/', views.PotholeDetailMapView.as_view(), name='pothole_detail_map'),

    # admin categories private
    path('categoryp/', views.CategoryPrivateBrowseView.as_view(), name='categoryp_browse'),
    path('categoryp/list', views.CategoryPrivateListView.as_view(), name='categoryp_list'),
    path('categoryp/add/', views.CategoryPrivateCreateView.as_view(), name='categoryp_add'),
    path('categoryp/<int:pk>/edit/', views.CategoryPrivateUpdateView.as_view(), name='categoryp_edit'),
    path('categoryp/<int:pk>/delete/', views.CategoryPrivateDeleteView.as_view(), name='categoryp_delete'),
    # admin agent
    path('agents/', views.AgentBrowseView.as_view(), name='agent_browse'),
    path('agent/list', views.AgentListView.as_view(), name='agent_list'),
    path('agent/add/', views.AgentCreateView.as_view(), name='agent_add'),
    path('agent/<int:pk>/detalle',views.AgentDetailview.as_view(), name='agent_detail'),
    path('agent/<int:pk>/edit/', views.AgentUpdateView.as_view(), name='agent_edit'),
    path('agent/<int:pk>/delete/', views.AgentDeleteView.as_view(), name='agent_delete'),
    path('agent/maps/', views.AgentMapView.as_view(),name='agent_map' )

]
