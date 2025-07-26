from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import FormView, ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Tours, News, Rate, Books
from .forms import SignupForm, LoginForm, AddRateForm, BookForm
from django.conf import settings


# Create your views here.

def main_page(request):
    return render(request, "TourSite/main-page.html")


class SignupView(FormView):
    template_name = "TourSite/signup.html"
    model = User
    form_class = SignupForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AuthenticationView(FormView):
    template_name = "TourSite/signin.html"
    model = User
    form_class = LoginForm

    def form_valid(self, form):
        login(self.request, form.user_cache)
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return settings.LOGIN_REDIRECT_URL


def profile(request):
    return render(request, template_name="TourSite/profile.html")


class ToursView(ListView):
    paginate_by = 4
    template_name = "TourSite/tours.html"
    model = Tours
    context_object_name = "tours"


class NewsView(ListView):
    paginate_by = 4
    template_name = "TourSite/news.html"
    model = News
    context_object_name = "news_list"


class RatesListView(ListView):
    paginate_by = 6
    template_name = "TourSite/rates/rates.html"
    model = Rate
    context_object_name = "rates"


class CreateRateView(LoginRequiredMixin, CreateView):
    model = Rate
    form_class = AddRateForm
    template_name = "TourSite/rates/send_rate.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        # return HttpResponse('Ви успішно відправили відгук!<a href="/">повернутись на головну сторінку</a>')
        return redirect(rate_success)


def rate_success(request):
    return render(request, "TourSite/rates/success.html")


def about_us(request):
    return render(request, "TourSite/about_us.html")


class BookView(LoginRequiredMixin, CreateView):
    model = Books
    form_class = BookForm
    template_name = "TourSite/book/book.html"

    def form_valid(self, form):
        print(self.request.user)
        form.instance.user = self.request.user
        form.save()
        return redirect(book_succes_view)


def book_succes_view(request):
    return render(request, "TourSite/book/book-success.html")


def logout_view(request):
    logout(request)
    return render(request, template_name="TourSite/main-page.html")
