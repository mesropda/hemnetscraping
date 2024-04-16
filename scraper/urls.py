from django.urls import path

from .views import home_page, contact_us

app_name = "scraper"

urlpatterns = [
    path('', home_page, name='home'),
    path('contact-us', contact_us, name='contact-us'),
]
