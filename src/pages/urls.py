from django.urls import path

from pages.views import dynamic_pages_view, index_page_view,terms_condition,privacy_policy,faq,robots_txt,competition_one_result

app_name = "pages"

urlpatterns = [
    path("", index_page_view, name="index"),
    path("<str:template_name>/", dynamic_pages_view, name="dynamic_pages"),
    path("terms_condition/", terms_condition, name="terms_condition"),
    path("privacy_policy/", privacy_policy, name="privacy_policy"),
    path("competition_one_result/", competition_one_result, name="competition_one_result"),
    path("faq/", faq, name="faq"),
    path("robots.txt", robots_txt),

]
