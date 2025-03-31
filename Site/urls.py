"""
URL configuration for Site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from Applicaion import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil, name='accueil'),
    path('a-propos/', views.a_propos, name='a_propos'),
    path('contact/', views.contact, name='contact'),
    path('tableau-amortissement/', views.tableau_amortissement, name='tableau_amortissement'),
    path('differe/', views.differe, name='differe'),
    path('non-differe/', views.non_differe, name='non_differe'),
    path('Nouvelle_page/',views.Nouvelle_page, name='Nouvelle_page'),
    path('non-differe/', views.non_differe, name='non_differe'),
    path('differe/', views.differe, name='differe'),
]
