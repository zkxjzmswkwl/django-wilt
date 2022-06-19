#!/usr/bin/env python
# -*- coding: utf-8 -*-

from members.models import Member
from .models import Scrobble

def gen_scrobble_sheet(user_id: int):
    """
    Generates spreadsheet containing all scrobbles for a given user.
    """

    user = Member.objects.get(id=user_id)
    scrobbles = Scrobble.objects.filter(belongs_to__id=user_id)
    doc_data = ""
    for s in scrobbles:
        doc_data += s.spreadsheet_entry + "\n"

    return doc_data


