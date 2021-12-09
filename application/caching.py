#!/usr/bin/env python3
import requests
from cachecontrol import CacheControl
from cachecontrol.caches.file_cache import FileCache

session = CacheControl(requests.session(), cache=FileCache(".cache"))


def get(url, format=None):
    r = session.get(url)

    if r.status_code == 404:
        return None

    r.raise_for_status()
    if format == "json":
        return r.json()
    return r.text
