from rest_framework.schemas import get_schema_view
from django_room.room_rental_project import urls
from django.contrib import admin
from django.urls import path,include
from endpoints import apis
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import SimpleRouter
import oauth2_provider.views as oauth2_views
from  oauth2_provider import urls as oauth2_urls
from rest_framework.documentation import include_docs_urls
import debug_toolbar
from django.conf import settings
import dotenv
import os

dotenv_file = os.path.join(settings.BASE_DIR , '.env')
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

# OAuth2 provider endpoints
oauth2_endpoint_views = [
    path('authorize/'+os.environ.get('AUTHORIZE') +'/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path('token'+os.environ.get('GETTOKEN') +'/', oauth2_views.TokenView.as_view(), name="token"),
    path('revoke_token/'+os.environ.get('REVOKETOKEN') + '/',oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
    path('refresh_token/'+os.environ.get('REFRESHTOKEN') + '/', oauth2_views.TokenView.as_view() , name="revoke-token"),
]

if settings.DEBUG:
    
    # OAuth2 Application Management endpoints
    oauth2_endpoint_views += [
        path('applications/', oauth2_views.ApplicationList.as_view(), name="list"),
        path('applications/register/', oauth2_views.ApplicationRegistration.as_view(), name="register"),
        path('applications/<pk>/', oauth2_views.ApplicationDetail.as_view(), name="detail"),
        path('applications/<pk>/delete/', oauth2_views.ApplicationDelete.as_view(), name="delete"),
        path('applications/<pk>/update/', oauth2_views.ApplicationUpdate.as_view(), name="update"),
    ]

    # OAuth2 Token Management endpoints
    oauth2_endpoint_views += [
        path('authorizedTokens/', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
        path('authorizedTokens/<pk>/delete/', oauth2_views.AuthorizedTokenDeleteView.as_view(),
            name="authorized-token-delete"),
    ]
        
urlpatterns = [
    path('admin'+os.environ.get('ADMIN') +'/', admin.site.urls),
    
    #application endpoints
    path('api/v1/roomRental/', include("endpoints.urls")),
    
    #oauth default endpoints
    path('oauth2/', include((oauth2_endpoint_views, 'oauth2_provider'), namespace='oauth2_provider')),
    
    #debug_toolbar urls
    path('_debug_/', include(debug_toolbar.urls)) if settings.DEBUG else path("",apis.Home, ),
    
    # path("",apis.Home, ),
    
    #auth_rest_framework 
    path('apiAuth/', include("rest_framework.urls")),

    #coreapi documentation
    path('api/v1/docs/',include_docs_urls(title='Room Rental APIs ')),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)



