from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('maintenance/', views.maintenance, name='maintenance'),
    path('maintenance/add/', views.add_membership, name='add_membership'),
    path('maintenance/update/', views.update_membership, name='update_membership'),
    path('maintenance/add_book/', views.add_book, name='add_book'),
    path('reports/', views.reports, name='reports'),
    path('transactions/', views.transactions, name='transactions'),
    path('transactions/issue/', views.issue_book, name='issue_book'),
    path('transactions/return/', views.return_book, name='return_book'),
]
