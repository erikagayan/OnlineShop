from django.contrib.admin.views.main import ChangeList


class MicroserviceUserChangeList(ChangeList):
    def get_queryset(self, request):
        # Возвращаем пустой QuerySet, так как данные получены не из базы данных
        return []


class FakeQuerySet:
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

    def __bool__(self):
        return bool(self.data)

    def _clone(self):
        # Возвращаем новый экземпляр FakeQuerySet с копией данных
        return FakeQuerySet(self.data[:])

