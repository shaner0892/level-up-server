"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game
from levelupapi.models.game_type import GameType
from levelupapi.models.gamer import Gamer


class GameView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
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
        gamer = Gamer.objects.get(user=request.auth.user)
        # # Next, we retrieve the GameType object from the database. We do
        # # this to make sure the game type the user is trying to add the
        # # new game actually exists in the database. The data passed in
        # # from the client is held in the request.data dictionary.
        # # Whichever keys are used on the request.data must match what the
        # # client is passing to the server.
        # game_type = GameType.objects.get(pk=request.data["game_type"])

        # game = Game.objects.create(
        #     title=request.data["title"],
        #     maker=request.data["maker"],
        #     number_of_players=request.data["number_of_players"],
        #     skill_level=request.data["skill_level"],
        #     gamer=gamer,
        #     game_type=game_type
        # )
        # serializer = GameSerializer(game)
        # return Response(serializer.data)
        
        # Instead of making a new instance of the Game model, the request.data 
        # dictionary is passed to the new serializer as the data. The keys on 
        # the dictionary must match what is in the fields on the serializer. 
        # After creating the serializer instance, call is_valid to make sure the 
        # client sent valid data. If the code passes validation, then the save 
        # method will add the game to the database and add an id to the serializer.
        serializer = CreateGameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    
    def update(self, request, pk):
        # Just like in the retrieve method, we grab the Game object we want from 
        # the database. Each of the next lines are setting the fields on game 
        # to the values coming from the client, like in the create method. 
        # After all the fields are set, the changes are saved to the database.
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["number_of_players"]
        game.skill_level = request.data["skill_level"]
        game_type = GameType.objects.get(pk=request.data["game_type"])
        game.game_type = game_type
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Game
        fields = ('id', 'game_type', 'title', 'maker',
                  'gamer', 'number_of_players', 'skill_level')
        
class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title', 'maker', 'number_of_players', 'skill_level', 'game_type']
