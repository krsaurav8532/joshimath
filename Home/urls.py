from django.urls import path

from . import views

app_name = 'Home'

urlpatterns = [
    path("", views.Home, name="index"),
    path("about/", views.About, name="about"),
    path("contact/", views.contact_view, name="contact"),
    path("services/", views.Services, name="services"),
    path("events/", views.Events, name="events"),
    path("stotras/", views.Stotras, name="stotras"),
    path("announcements/", views.Announcements, name="announcements"),
    path('<slug:slug>/', views.event_detail, name='event_detail'),
    path('announcements/<slug:slug>/', views.announcement_detail, name='announcement_detail'),

]