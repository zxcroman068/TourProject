from django.urls import path
from TourSite.views import main_page, AuthenticationView, SignupView, profile, ToursView, NewsView, CreateRateView, about_us, BookView, RatesListView, logout_view, book_succes_view, rate_success

urlpatterns = [
    path("", main_page, name="main_page"),
    path("signin/", AuthenticationView.as_view()),
    path("signup/", SignupView.as_view()),
    path("profile/", profile),
    path("tours/", ToursView.as_view()),
    path("news/", NewsView.as_view()),
    path("rates/send_rate/", CreateRateView.as_view()),
    path("about/", about_us),
    path("tours/book/", BookView.as_view()),
    path("tours/book/success", book_succes_view),
    path("rates/", RatesListView.as_view()),
    path("rates/success", rate_success),
    path("logout/", logout_view),
]
