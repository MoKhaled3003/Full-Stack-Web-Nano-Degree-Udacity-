"""
list of movies that feed into fresh_tomatoes.py file

"""
import media
import fresh_tomatoes

# Green Mile movie object
THE_GREEN_MILE = media.Movie("The Green Mile",
                             "https://upload.wikimedia.org/wikipedia/en/thumb/c/ce/Green_mile.jpg/220px-Green_mile.jpg",  # NOQA
                             "https://www.youtube.com/watch?v=Ki4haFrqSrw")

# Batman movie object
THE_BATMAN = media.Movie("The Dark Knight",
                         "https://upload.wikimedia.org/wikipedia/en/thumb/8/8a/Dark_Knight.jpg/220px-Dark_Knight.jpg",  # NOQA
                         "https://www.youtube.com/watch?v=EXeTwQWrcwY")

# Sully movie object
SULLY = media.Movie("Sully",
                    "https://upload.wikimedia.org/wikipedia/en/8/82/Sully_xxlg.jpeg",  # NOQA
                    "https://www.youtube.com/watch?v=mjKEXxO2KNE")

# American Psycho movie object
AMERICAN_PSYCHO = media.Movie("American Psycho",
                              "https://upload.wikimedia.org/wikipedia/en/thumb/6/63/Americanpsychoposter.jpg/220px-Americanpsychoposter.jpg",  # NOQA
                              "https://www.youtube.com/watch?v=2GIsExb5jJU")

# Accountant movie object
THE_ACCOUNTANT = media.Movie("The Accountant",
                             "http://www.dvdsreleasedates.com/posters/300/T/The-Accountant-2016.jpg",  # NOQA
                             "https://www.youtube.com/watch?v=DBfsgcswlYQ")
# Mechanic movie object
THE_MECHANIC = media.Movie("The Mechanic",
                           "https://upload.wikimedia.org/wikipedia/en/thumb/6/6d/Mark_Isham_-_The_Mechanic.jpg/220px-Mark_Isham_-_The_Mechanic.jpg",  # NOQA
                           "https://www.youtube.com/watch?v=CMklQNn0OH0")

# Array of movies
movies = [THE_GREEN_MILE, THE_BATMAN, SULLY, AMERICAN_PSYCHO,
          THE_ACCOUNTANT, THE_MECHANIC]

fresh_tomatoes.open_movies_page(movies)
