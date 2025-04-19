from django.contrib import admin
from django.urls import path, include
from .views import goalsedit, goalsgetpost
urlpatterns = [
    # path('goals', goalsgetpost),
    # path('goals/<int:pk>', goalsedit)
]
