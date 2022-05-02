from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from levelupapi.views import GameTypeView, EventView, GameView
from levelupapi.views import register_user, login_user

# The trailing_slash=False tells the router to accept /gametypes instead of /gametypes/. 
# It’s a very annoying error to come across, when your server is not responding and the 
# code looks right, the only issue is your fetch url is missing a / at the end.
router = routers.DefaultRouter(trailing_slash=False)
# The next line is what sets up the /gametypes resource. The first parameter, r'gametypes, 
# is setting up the url. The second GameTypeView is telling the server which view to use 
# when it sees that url. The third, gametype, is called the base name. You’ll only see the 
# base name if you get an error in the server. It acts as a nickname for the resource and 
# is usually the singular version of the url.
router.register(r'gametypes', GameTypeView, 'gametype')
router.register(r'events', EventView, 'event')
router.register(r'games', GameView, 'game')


urlpatterns = [
    # Requests to http://localhost:8000/register will be routed to the register_user function
    path('register', register_user),
    # Requests to http://localhost:8000/login will be routed to the login_user function
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]