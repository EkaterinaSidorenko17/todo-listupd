from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # graphiql - мини IDE для разработки graphql запросов
    path('graphql/', GraphQLView.as_view(graphiql=settings.DEBUG))
]
