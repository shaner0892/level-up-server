"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event
from levelupapi.models.game import Game
from levelupapi.models.gamer import Gamer


class EventView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)
        

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    # Inside the method, the first line of code is getting the game that
    # is logged in. Since all of our postman or fetch requests have the
    # user’s auth token in the headers, the request will get the user
    # object based on that token. From there, we use the request.auth.user
    # to get the Gamer object based on the user. Here’s the equivalent sql.
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        organizer = Gamer.objects.get(user=request.auth.user)
        # Next, we retrieve the GameType object from the database. We do
        # this to make sure the game type the user is trying to add the
        # new game actually exists in the database. The data passed in
        # from the client is held in the request.data dictionary.
        # Whichever keys are used on the request.data must match what the
        # client is passing to the server.
        game = Game.objects.get(pk=request.data["game"])

        event = Event.objects.create(
            game = game,
            description = request.data["description"],
            date = request.data["date"],
            time = request.data["time"],
            organizer = organizer
        )

        serializer = EventSerializer(event)
        return Response(serializer.data)
    
class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time', 'organizer')