from django.shortcuts import render
from django.views.generic import FormView, ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.http import HttpResponse
from .models import User, Tours, News, Rate, Books
from .forms import SignupForm, LoginForm, AddRateForm, BookForm
from django.contrib.auth import logout


# Create your views here.

def main_page(request):
    return render(request, "TourSite/main-page.html")


class SignupView(FormView):
    template_name = "TourSite/signup.html"
    model = User
    form_class = SignupForm
    success_url = reverse_lazy("main_page")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AuthenticationView(FormView):
    template_name = "TourSite/signin.html"
    model = User
    form_class = LoginForm
    success_url = reverse_lazy("main_page")

    def form_valid(self, form):
        login(self.request, form.user_cache)
        return super().form_valid(form)


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
    template_name = "TourSite/rates.html"
    model = Rate
    context_object_name = "rates"


class CreateRateView(CreateView):
    model = Rate
    form_class = AddRateForm
    template_name = "TourSite/send_rate.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return HttpResponse('Ви успішно відправили відгук!<a href="/">повернутись на головну сторінку</a>')

def about_us(request):
    return render(request, "TourSite/about_us.html")

class BookView(CreateView):
    model = Books
    form_class = BookForm
    template_name = "TourSite/book.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return HttpResponse("Ви успішно забронювали тур! Через деякий час вам зателефонують для уточнення деталей!<a href='/'>повернутись на головну сторінку</a>")


def logout_view(request):
    logout(request)
    return render(request, template_name="TourSite/main-page.html")
