# custom_filters.py
from django import template
from Guest.models import Room

register = template.Library()

@register.filter
def split_rooms(rooms_str):
    # Remove square brackets and extra spaces, then split into individual room names
    room_names = rooms_str.replace('[', '').replace(']', '').split(',')
    print(room_names)
    # Strip single quotes from each room name
    room_names = [room_name.strip().strip("'") for room_name in room_names]
    print(room_names)
    return room_names
@register.filter
def get_room(room_id):
    return Room.objects.get(pk=room_id)

@register.filter
def split(value, delimiter):
    return value.split(delimiter)
