from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import os

from .models import BookingEvent, History
# from .consumers import send_test_message

# Create your views here.


@csrf_exempt
def uclapi_webhook(request):
    arrived_hook_content = json.loads(request.body.decode('utf-8'))

    if not (
        arrived_hook_content["verification_secret"] ==
        os.environ["UCLAPI_WEBHOOK_VERIFICATION_SECRET"]
    ):
        response = JsonResponse({
            "ok": False,
            "error": "Invalid verification secret."
        })
        response.status_code = 400
        return response

    if arrived_hook_content["type"] == "challenge":
        return JsonResponse({
            "challenge": arrived_hook_content["challenge"]
        })

    events = arrived_hook_content["content"]

    new_history_item = History()
    new_history_item.setEventData(events)
    new_history_item.save()

    if "bookings_added" in events:
        for booking in events["bookings_added"]:
            new_booking = BookingEvent(
                added=True,
                **booking
            )
            new_booking.save()

    if "bookings_removed" in events:
        for booking in events["bookings_removed"]:
            new_booking = BookingEvent(
                added=False,
                **booking
            )
            new_booking.save()

    bookings_to_delete = BookingEvent.objects.all().order_by(
        '-created'
    )[100:]
    for booking in bookings_to_delete:
        booking.delete()

    return JsonResponse({
        "ok": True
    })


def index(request):
    bookings = BookingEvent.objects.all()
    serialized_bookings = []
    for booking in bookings:
        serialized_bookings.append({
            "roomname": booking.roomname,
            "siteid": booking.siteid,
            "roomid": booking.roomid,
            "description": booking.description,
            "start_time": booking.start_time.isoformat(),
            "end_time": booking.end_time.isoformat(),
            "contact": booking.contact,
            "slotid": booking.slotid,
            "weeknumber": booking.weeknumber,
            "phone": booking.phone,
            "created": booking.created.isoformat(),
            "added": booking.added
        })
    return render(request, 'index.html', context={
        "initial_data": json.dumps({
            "bookings": serialized_bookings
        })
    })

# def test_message(request):
#     send_test_message()
#     return JsonResponse({
#         "ok": True
#     })
