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

import debug_toolbar
from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    # Rota administrativa padrão
    path("admin/", admin.site.urls),
    # =========================================================================
    # CENTRALIZAÇÃO DE API E VERSIONAMENTO GLOBAL
    # =========================================================================
    # Em vez de criar um re_path para cada aplicativo, envelopamos toda a API
    # sob o prefixo 'api/'. O Regex captura se é 'v1' ou 'v2' de forma global.
    # Usamos o 'include([...])' para criar um subgrupo de caminhos limpos.
    #
    # URLs resultantes: /api/v1/... ou /api/v2/...
    # =========================================================================
    re_path(
        r"^api/(?P<version>(v1|v2))/",
        include(
            [
                # Se a URL contiver 'products', o Django delega para o app_product
                path("", include("app_product.urls")),
                # Se a URL contiver 'orders', o Django delega para o app_order
                path("", include("app_order.urls")),
            ]
        ),
    ),
    path("__debug__/", include(debug_toolbar.urls)),
]
