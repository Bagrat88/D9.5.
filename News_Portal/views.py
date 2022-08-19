import logging
import instance
from django.db.models.functions import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.views.generic.edit import FormMixin

from .forms import UserRegisterForm, UserLoginForm, ContactForm, CommentForm
from .models import Post, Category, Tag, Order
from django.db.models import F
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail

logger = logging.getLogger('django')


class Home(ListView):
    model = Post
    template_name = 'News_Portal/index.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CLASSIC BLOG DESIGN'
        return context


class PostByCategory(ListView):
    template_name = 'News_Portal/index.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class PostsByTag(ListView):
    template_name = 'News_Portal/index.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Записи по тегу: ' + str(Tag.objects.get(slug=self.kwargs['slug']))
        return context


class CustomSuccessMessageMixin:
    def __init__(self):
        self.request = None

    @property
    def success_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)

    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)


class GetPost(CustomSuccessMessageMixin, FormMixin, DetailView):
    model = Post
    template_name = 'News_Portal/single.html'
    context_object_name = 'post'
    form_class = CommentForm
    success_msg = 'Комментарий успешно создана,.ожидайте модерации'

    def get_success_url(self, **kwargs):
        return reverse_lazy('post')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return redirect('home')
        else:
            messages.error(request, 'Ошибка Комментарий')
        return render(request, 'News_Portal/single.html', {"form": form})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.article = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class Search(ListView):
    template_name = 'News_Portal/search.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрированы')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'News_Portal/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'News_Portal/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')


def test(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'EMAIL_HOST_USER', ['mail-кто будет получать'], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('test')
            else:
                messages.error(request, 'ошибка отправки')
        else:
            messages.error(request, 'ошибка регистрации')
    else:
        form = ContactForm
    return render(request, 'News_Portal/test.html', {"form": form})


class IndexView(TemplateView):
    template_name = "board/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.all()
        return context


class NewOrderView(CreateView):
    model = Order
    fields = ['products']  # единственное поле
    template_name = 'board/new.html'

    def form_valid(self, form):
        order = form.save()
        order.cost = sum([prod.price for prod in order.products.all()])
        order.save()
        complete_order.apply_async([order.pk], countdown=60)
        return redirect('/')

    def take_order(request, oid):
        order = Order.objects.get(pk=oid)
        order.time_out = datetime.now()
        order.save()
        return redirect('/')


def edit_page(request):
    template = 'edit_page.html'
    context = {

    }
    return render(request, template, context)


# class AppointmentView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'make_appointment.html', {})
#
#     def post(self, request, *args, **kwargs):
#         appointment = Appointment(
#             date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
#             client_name=request.POST['client_name'],
#             messages=request.POST['message'],
#         )
#         appointment.save()
        # return redirect('appointments.mke_appointment')
