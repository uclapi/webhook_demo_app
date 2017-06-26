from channels import Group
from .models import BookingEvent
from django.db.models.signals import post_save
from django.dispatch import receiver
from ciso8601 import parse_datetime
import json


# Connected to websocket.connect
def ws_add(message):
    # Accept the incoming connection
    message.reply_channel.send({"accept": True})
    # Add them to the chat group
    Group("listeners").add(message.reply_channel)


# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("listeners").discard(message.reply_channel)


@receiver(post_save, sender=BookingEvent)
def send_message(sender, instance, **kwargs):
    payload = {
        "text": json.dumps({
            "new_booking": {
                "roomname": instance.roomname,
                "siteid": instance.siteid,
                "roomid": instance.roomid,
                "description": instance.description,
                "start_time": parse_datetime(instance.start_time).isoformat(),
                "end_time": parse_datetime(instance.end_time).isoformat(),
                "contact": instance.contact,
                "slotid": instance.slotid,
                "weeknumber": instance.weeknumber,
                "phone": instance.phone,
                "created": instance.created.isoformat(),
                "added": instance.added
            }
        })
    }
    Group("listeners").send(payload)

# import datetime
# from random import randint
# def send_test_message():
#     payload = {
#         "text": json.dumps({
#             "new_booking": {
#                 "roomname": "Test Room Name",
#                 "siteid": "1000",
#                 "roomid": "666",
#                 "description": "This is a booking for testing",
#                 "start_time": (
#                     datetime.datetime.now() - datetime.timedelta(hours=5)
#                 ).isoformat(),
#                 "end_time": (
#                     datetime.datetime.now() + datetime.timedelta(hours=5)
#                 ).isoformat(),
#                 "contact": "Meeeeeee",
#                 "slotid": randint(0, 100000),
#                 "weeknumber": 40.0,
#                 "phone": None,
#                 "created": datetime.datetime.now().isoformat(),
#                 "added": True
#             }
#         })
#     }
#     Group("listeners").send(payload)
