from django.db import models
import json

# Create your models here.


class BookingEvent(models.Model):
    siteid = models.CharField(max_length=40, blank=True, null=True)
    roomid = models.CharField(max_length=160, blank=True, null=True)
    roomname = models.CharField(max_length=320, blank=True, null=True)
    slotid = models.BigIntegerField(primary_key=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    weeknumber = models.FloatField(blank=True, null=True)
    contact = models.CharField(max_length=4000, blank=True, null=True)
    phone = models.CharField(max_length=160, blank=True, null=True)
    description = models.CharField(max_length=523, blank=True, null=True)

    added = models.BooleanField()

    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


class History(models.Model):
    eventData = models.CharField(max_length=10000000)

    def setEventData(self, data):
        self.eventData = json.dumps(data)

    def getEventData(self):
        return json.loads(self.eventData)

    timestamp = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        auto_now=False
    )
