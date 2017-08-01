"""
here we have class movie() in the media.py which will
be used in entertainement_center.py
"""


class Movie():

    """
    this will be the specifications of the created object soon.
    title:
        the official name of the movie
    image:
        the url of the image from wikipedia
    trailer:
        the official trailer will be provided as a url from
        youtube

    """
    def __init__(self, title, image, trailer):
        self.title = title
        self.poster_image_url = image
        self.trailer_youtube_url = trailer
