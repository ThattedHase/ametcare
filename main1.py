from django.db import models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.urls import reverse
from datetime import timedelta

from django.http import HttpResponse
from django.views import View

app = Flask(__name__)
app.static_folder = 'static'
app.config['SECRET_KEY'] = '93422'
app.config['DATABASES'] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "users.db",
    }
}

db = models

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
cache = Cache(app)
app.permanent_session_lifetime = timedelta(days=30)


class User(models.Model, UserMixin):
    username = models.CharField(max_length=80, unique=True, null=False)
    email = models.CharField(max_length=120, unique=True, null=False)
    password = models.CharField(max_length=120, null=False)
    gender = models.CharField(max_length=10)
    weight = models.FloatField()
    height = models.FloatField()
    age = models.IntegerField()
    goal = models.CharField(max_length=20)
    preferences = models.ManyToManyField('Preference', related_name='user')


class Preference(models.Model):
    preference_name = models.CharField(max_length=50)


class Allergy(models.Model):
    allergy_name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


@login_manager.user_loader
def load_user(user_id):
    return User.objects.get(pk=int(user_id))


class IndexView(View):
    def get(self, request):
        return render(request, 'start1.html')


class Index1View(View):
    def get(self, request):
        return render(request, 'start2.html')


@login_required
class AllergyView(View):
    def get(self, request):
        return render(request, 'allergy.html')

    def post(self, request):
        selected_allergies = request.POST.getlist('allergy')
        current_user.allergies.clear()

        for allergy_name in selected_allergies:
            allergy, created = Allergy.objects.get_or_create(user=current_user, allergy_name=allergy_name)

        messages.success(request, 'Allergies saved.')
        return redirect(reverse('main'))


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if not username or not password or not email:
            return redirect(reverse('register'))

        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            return redirect(reverse('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password, email=email)
        new_user.save()

        return redirect(reverse('userinfo'))


@login_required
class IndprefView(View):
    def get(self, request):
        return render(request, 'indpref.html')

    def post(self, request):
        selected_preferences = request.POST.getlist('preferences')
        current_user.preferences.clear()

        for preference_name in selected_preferences:
            preference, created = Preference.objects.get_or_create(user=current_user, preference_name=preference_name)

        messages.success(request, 'Preferences saved.')
        return redirect(reverse('choose'))


class ChooseView(View):
    def get(self, request):
        return render(request, 'choose.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect(reverse('main'))
        else:
            messages.error(request, 'Login failed. Check your username and password.')

        return render(request, 'login.html')


@login_required
class UserinfoView(View):
    def get(self, request):
        return render(request, 'userinfo.html')

    def post(self, request):
        current_user.gender = request.POST.get('gender')
        current_user.weight = float(request.POST.get('weight'))
        current_user.height = float(request.POST.get('height'))
        current_user.first_name = request.POST.get('first_name')
        current_user.last_name = request.POST.get('last_name')
        current_user.age = int(request.POST.get('age'))
        current_user.goal = request.POST.get('goal')
        current_user.save()

        messages.success(request, 'User information saved.')
        return redirect(reverse('indpref'))


@login_required
class MainView(View):
    def get(self, request):
        return render(request, 'main.html')


class CalendarView(View):
    def get(self, request):
        return render(request, 'calendar.html')


@login_required
class ProductsView(View):
    def get(self, request):
        return render(request, 'products.html')


@login_required
class EtcView(View):
    def get(self, request):
        return render(request, 'etc.html')


if __name__ == '__main__':
    app.run(debug=True)
