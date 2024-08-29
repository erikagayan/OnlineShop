from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.conf import settings
from django import forms
import requests
from .models import MicroserviceUserProxy
from django.contrib.admin.views.main import ChangeList

class UserEditForm(forms.ModelForm):
    class Meta:
        model = MicroserviceUserProxy
        fields = ['email', 'username', 'is_manager', 'is_moderator']

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
        # Возвращаем пустой QuerySet, чтобы избежать обращения к базе данных
        return MicroserviceUserQuerySet([])

class MicroserviceUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'is_manager', 'is_moderator')
    readonly_fields = ('id',)
    actions = ['delete_users']

    def get_changelist(self, request, **kwargs):
        # Используем кастомный ChangeList
        return MicroserviceUserChangeList

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('edit-user/<str:user_id>/', self.admin_site.admin_view(self.edit_user), name='edit-user'),
        ]
        return custom_urls + urls

    def get_queryset(self, request):
        # Возвращаем пустой QuerySet, чтобы избежать обращения к базе данных
        return MicroserviceUserQuerySet([])

    def changelist_view(self, request, extra_context=None):
        # Используем кастомный ChangeList
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

            # Оборачиваем данные в кастомный QuerySet
            users_queryset = MicroserviceUserQuerySet([
                MicroserviceUserProxy(
                    id=user['id'],
                    email=user['email'],
                    username=user['username'],
                    is_manager=user['is_manager'],
                    is_moderator=user['is_moderator']
                ) for user in users_data
            ])

            # Обновляем контекст для отображения данных в админ-панели
            extra_context = extra_context or {}
            response.context_data['cl'].result_list = users_queryset
            response.context_data['cl'].full_result_count = users_queryset.count()
            response.context_data.update(extra_context)

        except Exception as e:
            print(f"Unexpected error: {e}")
            self.message_user(request, f"Unexpected error: {e}", level='error')
        return response

    def edit_user(self, request, user_id):
        """
        Custom view for editing a user.
        """
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
                    return self.admin_site.admin_view(render)(request, 'admin/edit_user.html', {'form': form, 'user_id': user_id})
                else:
                    self.message_user(request, f"Error fetching user: {response.status_code}", level='error')
            except Exception as e:
                self.message_user(request, f"Unexpected error: {e}", level='error')

            return HttpResponseRedirect('..')

    def delete_users(self, request, queryset):
        """
        Action for deleting users via microservice API.
        """
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
