from django.core.files import File
import musicbrainzngs
import requests

def download_album_cover(instance):
    # Configure the MusicBrainz client
    musicbrainzngs.set_useragent("AppName", "1.0", "YourContactInfo")

    # Search for the album using the title
    print(instance.title)
    result = musicbrainzngs.search_releases(release=instance.title, limit=1)
    if not result['release-list']:
        print("No album found with the title:", instance.title)
        return

    # Get the first matching release
    release = result['release-list'][0]

    # Get the release details to fetch the cover art archive
    release_id = release['id']
    try:
        includes = ["release-groups"]
        release_details = musicbrainzngs.get_release_by_id(release_id, includes=includes)

        # Extract the Cover Art Archive URL from the release group
        release_group_id = release_details['release']['release-group']['id']
        cover_art_archive = musicbrainzngs.get_release_group_image_list(release_group_id)

        if cover_art_archive['images']:
            image_url = cover_art_archive['images'][0]['image']
            response = requests.get(image_url)

            # Save the image
            with open(f"{instance.title}_cover.jpg", "wb+") as file:
                file.write(response.content)
                file.seek(0)  # reset file pointer to beginning

                # Create or update the model instance
                instance.cover.save(f"{instance.title}_cover.jpg", File(file))
                instance.save()

            print(f"Cover downloaded successfully for '{instance.title}'.")
        else:
            print("No cover image found for:", instance.title)
    except musicbrainzngs.WebServiceError as exc:
        print("Failed to fetch cover art:", exc)
