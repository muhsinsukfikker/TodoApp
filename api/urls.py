from django.urls import path
from api import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register('todos',views.TodosView, basename='todo')


urlpatterns = [
    path('register/',views.RegisterView.as_view()),
] + router.urls
