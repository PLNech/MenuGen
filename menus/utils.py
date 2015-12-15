import json

from collections import namedtuple


def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)


def list_pk(queryset):
    if queryset is None:
        return "0"
    items = queryset.all()
    if len(items):
        pklist = [str(i.pk) for i in items]
        uniquelist = sorted(list(set(pklist)), key=lambda i: int(i))
        return ",".join(uniquelist)
    else:
        return "None"
