"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event
from levelupapi.models import gamer
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
        gamer = Gamer.objects.get(user=request.auth.user)
        # Set the `joined` property on every event
        for event in events:
            # Check to see if the gamer is in the attendees list on the event
            event.joined = gamer in event.attendees.all()
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
        # # Next, we retrieve the GameType object from the database. We do
        # # this to make sure the game type the user is trying to add the
        # # new game actually exists in the database. The data passed in
        # # from the client is held in the request.data dictionary.
        # # Whichever keys are used on the request.data must match what the
        # # client is passing to the server.
        # game_id = Game.objects.get(pk=request.data["game_id"])

        # event = Event.objects.create(
        #     game = game_id,
        #     description = request.data["description"],
        #     date = request.data["date"],
        #     time = request.data["time"],
        #     organizer = organizer_id
        # )

        # serializer = EventSerializer(event)
        # return Response(serializer.data)
    
        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=organizer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        # Just like in the retrieve method, we grab the Game object we 
        # want from the database. Each of the next lines are setting the 
        # fields on game to the values coming from the client, like in 
        # the create method. After all the fields are set, the changes 
        # are saved to the database.
        """Handle PUT requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """

        event = Event.objects.get(pk=pk)
        game = Game.objects.get(pk=request.data["game"])
        event.game = game
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]
        organizer = Gamer.objects.get(user=request.auth.user)
        event.organizer = organizer
        # event.attendees??
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
    # Using the action decorator turns a method into a new route. 
    # In this case, the action will accept POST methods and because 
    # detail=True the url will include the pk. Since we need to know 
    # which event the user wants to sign up for we’ll need to have the 
    # pk. The route is named after the function. So to call this method 
    # the url would be http://localhost:8000/events/2/signup
    
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""
    
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(gamer)
        event.joined = True
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)
    
    # Removes a gamer from an event
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Delete request for a user to leave an event"""
    
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        event.joined = False
        return Response({'message': 'Gamer removed'}, status=status.HTTP_204_NO_CONTENT)
    
    
class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time', 'organizer', 'attendees', 'joined')
        
class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'game', 'description', 'date', 'time']