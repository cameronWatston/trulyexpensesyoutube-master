from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
     path('debt-savings', views.debt_savings_calculator, name='debt_savings_calculator'),

]
