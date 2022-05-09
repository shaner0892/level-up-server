from django.db import models

class Event(models.Model):

    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    # list of gamers attending the event, many to many through EventGamer table, attendees is related to events
    # you don't have to use the through if you already have the table created; it will create a table automatically if you don't specify
    attendees = models.ManyToManyField("Gamer", through="EventGamer", related_name="events")

    # it's on the model, but not in the database
    # you could add a "readTime" property or a "abbreviatedDisplay" that has to be calculated before it is added
    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value