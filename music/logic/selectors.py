from music.models import Artist, Album, Song, Scrobble

def get_song(**kwargs):
    id = kwargs.get("id", None)
    title = kwargs.get("title", None)
    title_substr = kwargs.get("title_substr", None)

    if id is not None:
        return Song.objects.get(id=id)
    if title is not None:
        return Song.objects.get(title__iexact=title)
    if title_substr is not None:
        return Song.objects.get(title__icontains=title_substr)
    
def get_artist(**kwargs):
    id = kwargs.get("id", None)
    title = kwargs.get("title", None)
    title_substr = kwargs.get("title_substr", None)

    if id is not None:
        return Artist.objects.get(id=id)
    if title is not None:
        return Artist.objects.get(title__iexact=title)
    if title_substr is not None:
        return Artist.objects.get(title__icontains=title_substr)

