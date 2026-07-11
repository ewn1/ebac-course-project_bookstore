"""
URL configuration for bookstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    # Rota administrativa padrão
    path("admin/", admin.site.urls),
    # 1. VERSIONAMENTO DE API COM REGEX
    # Usamos 're_path' porque precisamos de lógica condicional (Regex).
    # 'product/' -> prefixo da URL.
    # '(?P<version>(v1|v2))/' -> captura 'v1' ou 'v2' e salva na variável 'version'.
    # Isso permite URLs como: /product/v1/ ou /product/v2/
    re_path("product/(?P<version>(v1|v2))/", include("app_product.urls")),
    # O mesmo conceito se aplica aqui para os pedidos (orders).
    re_path("order/(?P<version>(v1|v2))/", include("app_order.urls")),
]
