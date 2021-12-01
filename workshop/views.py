from django.shortcuts import render, redirect
from .models import Workshop, Guard, Master, WorksOn, Defend, Review, AdminRequest
from django.views.generic import ListView, DetailView, CreateView
from .forms import ReviewForm, AuthUserForm, RegisterUserForm, AdminReqForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
# Create your views here.


# Метод, с помощь которого буду отправлять сообщения о соврешенных действиях
# например, о том, что отзыв создан. Вынес в отельный класс, чтобы потом просто
# наследоваться от него и использовать его методы(например, в ReviewCreateView)
class CustomSuccessMessageMixin:

    @property   # Декоратор для перевода резултата в строку
    def success_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)    # обращение к глобальной переменной messages
        return super().form_valid(form)


# Контроллер для входа в приложение(отправная точка)
def index(request):
    return render(request, 'workshop/index.html')


# Контроллер для стартовой страницы, после регистрации или авторизации
# В ходе работы над приложением в нем отпала надобность, не удаляю в виду
# того, что может пригодиться при масштабировании приложения
def start(request):
    return render(request, 'workshop/start.html')


# Контроллер для страницы специалистов
def masters(request):
    masters_info = Master.objects.all()
    works_on_info = WorksOn.objects.all()
    return render(request, 'workshop/masters.html', {'masters_info': masters_info, 'works_on_info': works_on_info})


# Контроллер для списка отзывов в виде класса гораздо
# удобнее, чем в виде функции(см. выше)
class ReviewListView(ListView):
    model = Review
    template_name = 'workshop/review.html'
    context_object_name = 'reviews_info'


# Контроллер для вывода каждого отзыва на отдельной странице
class ReviewDetailView(DetailView):
    model = Review
    template_name = 'workshop/detail.html'
    context_object_name = 'get_review'


# Контроллер для страницы охранных фирм
def guards(request):
    guard_info = Guard.objects.all()
    defend_info = Defend.objects.all()
    return render(request, 'workshop/guards.html', {'title': 'Наше охранные фирмы', 'guard_info': guard_info,
                                                    'defend_info': defend_info})


# Контроллер создания отзыва
class ReviewCreateView(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login_page')  # Перенаправление на страницу авторизации, если гость попытается зайти и написать отзыв
    model = Review  # Модель, из которой получаем данные
    template_name = 'workshop/make_review.html'     # Шаблон, на который отсылаем по GET-запросу
    form_class = ReviewForm     # Форма, через которую со страницы идет POST-запрос
    success_url = reverse_lazy('make_review')   # Ссылка для редиректа(в данномслучае) после отправки валидной формы
    success_msg = 'Запись создана'

    def form_valid(self, form):
        self.object = form.save(commit = False) # Пока не сохраняем данные из формы в БД, но данные получили
        self.object.author = self.request.user # Пполучили автора статьи из request
        self.object = form.save()   # теперь спокойно сохраняем статью с авторством
        return super().form_valid(form)


# Контроллер для страницы мастерских
# тут удобнее работать с функцией
def workshops(request):
    workshop_info = Workshop.objects.all()
    works_on_info = WorksOn.objects.all()
    masters_info = Master.objects.all()
    defend_info = Defend.objects.all()
    return render(request, 'workshop/workshops.html', {'title': 'Наши мастерские', 'workshop_info': workshop_info,
                                                       'works_on_info': works_on_info, 'masters_info': masters_info,
                                                       'defend_info': defend_info})


# Контроллер для авторизации
class MyprojectLoginView(LoginView):
    template_name = 'workshop/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('enter')     # Перенаправление пользователя на главную после авторизации

    def get_success_url(self):
        return self.success_url


# Контроллер для регистрации
class RegisterUserView(CreateView):
    model = User
    template_name = 'workshop/register_page.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('enter')     # Перенаправление пользователя на главную после регистрации(и заодно его авторизация)
    success_msg = 'Пользователь успешно создан'
    # Добавил функцию, чтобы только что зарегистрированный пользователь
    # был сразу авторизован, а не авторизовывался сам после регистрации

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid


# Контроллер для выхода из учетной записи
class MyProjectLogout(LogoutView):
    next_page = reverse_lazy('enter')   # Перенаправление пользователя на главную после выхода из учетки


# Функция, используемая в котроллере для отправки прямого SQL-запроса
def my_custom_sql(self, req):
    with connection.cursor() as cursor:
        cursor.execute(str(req))
        row = cursor.fetchall()
    return row


# Обработчик админского sql-запроса(см.контроллер ниже)
def my_custom_sql(self):
    with connection.cursor() as cursor:
        cursor.execute(self)
        row = cursor.fetchall()
    return row


# Контроллер для админской страницы создания запроса и вывода результата
def admin_req(request):
    if request.method == 'POST':
        form = AdminReqForm(request.POST)
        if form.is_valid():
            form.save()

    req_info = AdminRequest.objects.latest('id')
    req_info = str(req_info)
    res = my_custom_sql(req_info)
    form = AdminReqForm()
    context = {'req_info': req_info, 'form': form, 'res': res}
    template = 'workshop/admin_req.html'

    return render(request, template, context)