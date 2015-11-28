import json
from collections import namedtuple


def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)


def list_pk(queryset):
    items = queryset.all()
    if len(items):
        return ",".join([str(i.pk) for i in sorted(items, key=lambda i: i.pk)])
    else:
        return "None"
