from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

from .models import BookingEvent, History

# Create your views here.


@csrf_exempt
def uclapi_webhook(request):
    events = json.loads(request.body.decode('utf-8'))

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

    booking_events_to_keep = BookingEvent.objects.all().order_by(
        '-created'
    )[:100]
    BookingEvent.objects.exclude(
        pk__in=booking_events_to_keep
    ).delete()

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

def incoming_websocket(request):
    pass
