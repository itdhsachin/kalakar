from django.urls import path

from pages.views import dynamic_pages_view, index_page_view

app_name = "pages"

urlpatterns = [
    path("", index_page_view, name="index"),
    path("<str:template_name>/", dynamic_pages_view, name="dynamic_pages"),
]
