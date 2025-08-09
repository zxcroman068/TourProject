from django.urls import path
from TourSite.views import (main_page, AuthenticationView, SignupView, profile, ToursView, NewsView, CreateRateView,
                            about_us, BookView, RatesListView, logout_view, book_succes_view, rate_success,
                            TourDetailView, NewsDetailView)

urlpatterns = [
    path("", main_page, name="main_page"),
    path("profile/signin/", AuthenticationView.as_view(), name="login"),
    path("profile/signup/", SignupView.as_view()),
    path("profile/", profile),
    path("news/", NewsView.as_view()),
    path("news/<int:pk>/", NewsDetailView.as_view(), name="news_detail"),
    path("about/", about_us),
    path("tours/", ToursView.as_view()),
    path("tours/<int:pk>/", TourDetailView.as_view(), name="tour_detail"),
    path("tours/book/", BookView.as_view()),
    path("tours/book/success", book_succes_view),
    path("rates/", RatesListView.as_view()),
    path("rates/success", rate_success),
    path("rates/send_rate/", CreateRateView.as_view()),
    path("profile/logout/", logout_view),
]
