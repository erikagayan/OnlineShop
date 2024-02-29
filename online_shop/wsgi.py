import os
from django.core.wsgi import get_wsgi_application

settings_module = "online_shop.deployment" if "WEBSITE_HOSTNAME" in os.environ else "online_shop.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

application = get_wsgi_application()
