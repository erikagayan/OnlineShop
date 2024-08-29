from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.conf import settings
from django import forms
import requests
from .models import MicroserviceUserProxy
from django.contrib.admin.views.main import ChangeList
from django.contrib.admin.helpers import AdminForm

class UserEditForm(forms.ModelForm):
    class Meta:
        model = MicroserviceUserProxy
        fields = ['email', 'username', 'is_manager', 'is_moderator']

class UserAddForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = MicroserviceUserProxy
        fields = ['email', 'username', 'is_manager', 'is_moderator', 'password', 'password_confirmation']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            self.add_error('password_confirmation', "Passwords do not match")

        return cleaned_data

class MicroserviceUserQuerySet:
    def __init__(self, data):
        self.data = data

    def __iter__(self):
        return iter(self.data)

    def count(self):
        return len(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def all(self):
        return self

    def filter(self, *args, **kwargs):
        return self

    def order_by(self, *args, **kwargs):
        return self

    def _clone(self):
        return MicroserviceUserQuerySet(self.data[:])

class MicroserviceUserChangeList(ChangeList):
    def get_queryset(self, request):
        return MicroserviceUserQuerySet([])

class MicroserviceUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'is_manager', 'is_moderator')
    readonly_fields = ('id',)
    actions = ['delete_users']
    form = UserEditForm

    # Добавляем add_fieldsets для отображения дополнительных полей при добавлении пользователя
    add_fieldsets = (
        (None, {
            'fields': ('email', 'username', 'is_manager', 'is_moderator', 'password', 'password_confirmation'),
        }),
    )

    def get_changelist(self, request, **kwargs):
        return MicroserviceUserChangeList

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('edit-user/<str:user_id>/', self.admin_site.admin_view(self.edit_user), name='edit-user'),
        ]
        return custom_urls + urls

    def get_queryset(self, request):
        return MicroserviceUserQuerySet([])

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        try:
            token = request.session.get('auth_token') or request.headers.get('Authorization')
            if not token:
                self.message_user(request, "Authorization token is missing.", level='error')
                return response

            if token.startswith('Bearer '):
                token = token.split(' ', 1)[1]

            headers = {'Authorization': f'Bearer {token}'}

            response_data = requests.get(f'{settings.MICROSERVICE_USER_URL}/api/users/users/', headers=headers)
            if response_data.status_code != 200:
                self.message_user(request, f"Error fetching users: {response_data.status_code}", level='error')
                return response

            users_data = response_data.json()

            users_queryset = MicroserviceUserQuerySet([
                MicroserviceUserProxy(
                    id=user['id'],
                    email=user['email'],
                    username=user['username'],
                    is_manager=user['is_manager'],
                    is_moderator=user['is_moderator']
                ) for user in users_data
            ])

            extra_context = extra_context or {}
            response.context_data['cl'].result_list = users_queryset
            response.context_data['cl'].full_result_count = users_queryset.count()
            response.context_data.update(extra_context)

        except Exception as e:
            print(f"Unexpected error: {e}")
            self.message_user(request, f"Unexpected error: {e}", level='error')
        return response

    def add_view(self, request, form_url='', extra_context=None):
        """
        Custom view to handle the addition of a new user.
        """
        if request.method == 'POST':
            form = UserAddForm(request.POST)
            if form.is_valid():
                token = request.session.get('auth_token') or request.headers.get('Authorization')
                if not token:
                    self.message_user(request, "Authorization token is missing.", level='error')
                    return HttpResponseRedirect('..')

                if token.startswith('Bearer '):
                    token = token.split(' ', 1)[1]

                headers = {'Authorization': f'Bearer {token}'}
                user_data = form.cleaned_data
                user_data.pop('password_confirmation')  # Убираем поле подтверждения пароля

                try:
                    response = requests.post(
                        f'{settings.MICROSERVICE_USER_URL}/api/users/register/',
                        headers=headers,
                        json=user_data
                    )
                    if response.status_code in [200, 201]:
                        self.message_user(request, "User added successfully.")
                    else:
                        self.message_user(request, f"Error adding user: {response.status_code}", level='error')
                except Exception as e:
                    self.message_user(request, f"Unexpected error: {e}", level='error')
                return HttpResponseRedirect('..')

        else:
            form = UserAddForm()

        # Создание объекта AdminForm для рендеринга формы в админ-панели
        admin_form = AdminForm(form, self.add_fieldsets, self.prepopulated_fields, self.readonly_fields, model_admin=self)

        # Обновляем контекст для метода render_change_form
        context = {
            'adminform': admin_form,
            'form': form,
            'add': True,
            'change': False,
            'is_popup': False,
            'save_as': False,
            'has_add_permission': True,
            'has_change_permission': False,
            'has_delete_permission': False,
            'has_view_permission': True,
            'show_save_and_add_another': False,
            'show_save_and_continue': False,
            'inline_admin_formsets': [],  # Обязательно добавляем этот ключ в контекст
            'errors': form.errors,  # Отображение ошибок формы
        }

        return self.render_change_form(request, context, add=True, change=False, form_url=form_url)

    def edit_user(self, request, user_id):
        if request.method == 'POST':
            form = UserEditForm(request.POST)
            if form.is_valid():
                token = request.session.get('auth_token') or request.headers.get('Authorization')
                if not token:
                    self.message_user(request, "Authorization token is missing.", level='error')
                    return HttpResponseRedirect('..')

                if token.startswith('Bearer '):
                    token = token.split(' ', 1)[1]

                headers = {'Authorization': f'Bearer {token}'}
                user_data = form.cleaned_data

                try:
                    response = requests.put(
                        f'{settings.MICROSERVICE_USER_URL}/api/users/{user_id}/',
                        headers=headers,
                        json=user_data
                    )
                    if response.status_code in [200, 204]:
                        self.message_user(request, "User updated successfully.")
                    else:
                        self.message_user(request, f"Error updating user: {response.status_code}", level='error')
                except Exception as e:
                    self.message_user(request, f"Unexpected error: {e}", level='error')
                return HttpResponseRedirect('..')

        else:
            token = request.session.get('auth_token') or request.headers.get('Authorization')
            if not token:
                self.message_user(request, "Authorization token is missing.", level='error')
                return HttpResponseRedirect('..')

            if token.startswith('Bearer '):
                token = token.split(' ', 1)[1]

            headers = {'Authorization': f'Bearer {token}'}

            try:
                response = requests.get(f'{settings.MICROSERVICE_USER_URL}/api/users/{user_id}/', headers=headers)
                if response.status_code == 200:
                    user_data = response.json()
                    form = UserEditForm(initial=user_data)
                    return self.render_change_form(request, context={'form': form, 'user_id': user_id})
                else:
                    self.message_user(request, f"Error fetching user: {response.status_code}", level='error')
            except Exception as e:
                self.message_user(request, f"Unexpected error: {e}", level='error')

            return HttpResponseRedirect('..')

    def delete_users(self, request, queryset):
        for user in queryset:
            token = request.session.get('auth_token') or request.headers.get('Authorization')
            if not token:
                self.message_user(request, "Authorization token is missing.", level='error')
                continue

            if token.startswith('Bearer '):
                token = token.split(' ', 1)[1]

            headers = {'Authorization': f'Bearer {token}'}

            try:
                response = requests.delete(f'{settings.MICROSERVICE_USER_URL}/api/users/{user.id}/', headers=headers)
                if response.status_code == 204:
                    self.message_user(request, f"User {user.email} deleted successfully.")
                else:
                    self.message_user(request, f"Error deleting user: {response.status_code}", level='error')
            except Exception as e:
                self.message_user(request, f"Unexpected error: {e}", level='error')

    delete_users.short_description = 'Delete selected users'

admin.site.register(MicroserviceUserProxy, MicroserviceUserAdmin)
