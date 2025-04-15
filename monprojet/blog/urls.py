from django.urls import path
from .views import inscription, connexion, deconnexion, dashboard,create_article, liste_articles, update_article, delete_article, afficher_pdf, liste_bib, create_bib, create_article_id, HTML_To_PDF, get_articles, add_article, put_article, sup_article,register_user, CustomTokenObtainPairView
#from .admin import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from rest_framework.permissions import IsAuthenticated

urlpatterns=[
    path("inscription/", inscription, name="inscription"),
    path("connexion/", connexion, name="connexion"),
    path("deconnexion/", deconnexion, name="deconnexion"),
    path("dashboard/", dashboard, name="dashboard"),


    # bib
    path('liste_bib/', liste_bib, name='liste_bib'),
    path('create_bib/', create_bib, name='create_bib'),
    # Articl's routes
    path("liste_articles/<int:id>",liste_articles, name="liste_articles"),
    path("create_article/",create_article, name="create_article"),
    path("create_article_id/<int:id>",create_article_id, name="create_article_id"),
    path("update_article/<int:id>",update_article, name="update_article"),
    path("delete_article/<int:id>/<int:id_lib>/",delete_article, name="delete_article"),
    path('voir-pdf/<int:id>/', afficher_pdf, name='afficher_pdf'),
    path('HTML_To_PDF/<int:id>', HTML_To_PDF, name='HTML_To_PDF'),

    # DRF
    path('get_articles/',get_articles, name='get_articles'),
    path('add_article/',add_article, name='add_article'),
    path('put_article/<int:id_article>',put_article, name='put_article'),
    path('sup_article/<int:id_article>',sup_article, name='sup_article'),

    # JWT
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register_user/', register_user, name='register_user'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)