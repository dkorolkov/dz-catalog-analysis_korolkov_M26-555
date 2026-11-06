import unittest

from catalog_analysis import (
    above_average,
    actor_filmography,
    all_genres,
    average_rating,
    catalog_age_stats,
    common_actors,
    count_by_genre,
    count_long_movies,
    decade_label,
    duration_in_hours,
    format_report_line,
    genres_only_in_one,
    make_slug,
    normalize_title,
    rating_tier,
    titles_sorted_by_rating,
    top_n_by_rating,
)


class DurHoursTestCase(unittest.TestCase):
    def test_duration_in_hours(self):
        self.assertEqual(duration_in_hours(0), "0ч 0м")
        self.assertEqual(duration_in_hours(30), "0ч 30м")
        self.assertEqual(duration_in_hours(60), "1ч 0м")
        self.assertEqual(duration_in_hours(62), "1ч 2м")
        self.assertEqual(duration_in_hours(153), "2ч 33м")

    def test_negative_value(self):
        with self.assertRaises(ValueError):
            duration_in_hours(-1)

class AverageRatingTestCase(unittest.TestCase):
    def test_average_rating_one_item(self):
        movies = [
        {"title": "The Dune Chronicles", "year": 2021,
             "genres": {"sci-fi", "drama"},
             "rating": 8.6, "duration_min": 155,
             "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"]},
        ]
        self.assertAlmostEqual(average_rating(movies), 8.6, 1)

    def test_average_rating_many_items(self):
        movies = [
            {"title": "The Dune Chronicles", "year": 2021,
             "genres": {"sci-fi", "drama"},
             "rating": 8.6, "duration_min": 155,
             "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"]},
            {"title": "Kitchen Stories", "year": 2019,
             "genres": {"comedy", "drama"},
             "rating": 7.1, "duration_min": 98,
             "actors": ["A. Novak", "M. Ferguson"]},
            {"title": "silent hours", "year": 2016,
             "genres": {"thriller", "drama"},
             "rating": 6.4, "duration_min": 112,
             "actors": ["J. Bloom", "K. Lee"]},
        ]
        self.assertAlmostEqual(average_rating(movies), 7.4, 1)

    def test_average_rating_zero_items(self):
        with self.assertRaises(ValueError):
            average_rating([])

class AgeStatsTestCase(unittest.TestCase):
    def test_catalog_age_stats_one_item_default_year(self):
        movies = [
        {"title": "The Dune Chronicles", "year": 2021,
             "genres": {"sci-fi", "drama"},
             "rating": 8.6, "duration_min": 155,
             "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"]},
        ]
        oldest_movie, newest_movie, average = catalog_age_stats(movies)
        self.assertEqual(oldest_movie, 5)
        self.assertEqual(newest_movie, 5)
        self.assertEqual(average, 5)

    def test_catalog_age_stats_one_item_specified_year(self):
        movies = [
        {"title": "The Dune Chronicles", "year": 2021,
             "genres": {"sci-fi", "drama"},
             "rating": 8.6, "duration_min": 155,
             "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"]},
        ]
        oldest_movie, newest_movie, average = catalog_age_stats(movies, 2025)
        self.assertEqual(oldest_movie, 4)
        self.assertEqual(newest_movie, 4)
        self.assertEqual(average, 4)

    def test_catalog_age_stats_many_items_default_year(self):
        movies = [
            {"title": "The Dune Chronicles", "year": 2021,
             "genres": {"sci-fi", "drama"},
             "rating": 8.6, "duration_min": 155,
             "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"]},
            {"title": "Kitchen Stories", "year": 2019,
             "genres": {"comedy", "drama"},
             "rating": 7.1, "duration_min": 98,
             "actors": ["A. Novak", "M. Ferguson"]},
            {"title": "silent hours", "year": 2016,
             "genres": {"thriller", "drama"},
             "rating": 6.4, "duration_min": 112,
             "actors": ["J. Bloom", "K. Lee"]},
        ]
        oldest_movie, newest_movie, average = catalog_age_stats(movies)
        self.assertEqual(oldest_movie, 10)
        self.assertEqual(newest_movie, 5)
        self.assertEqual(average, 8)


    def test_catalog_age_stats_year_before_movie(self):
        movies = [
            {"title": "The Dune Chronicles", "year": 2021,
             "genres": {"sci-fi", "drama"},
             "rating": 8.6, "duration_min": 155,
             "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"]},
            {"title": "Kitchen Stories", "year": 2019,
             "genres": {"comedy", "drama"},
             "rating": 7.1, "duration_min": 98,
             "actors": ["A. Novak", "M. Ferguson"]},
            {"title": "silent hours", "year": 2016,
             "genres": {"thriller", "drama"},
             "rating": 6.4, "duration_min": 112,
             "actors": ["J. Bloom", "K. Lee"]},
        ]
        with self.assertRaises(ValueError):
            catalog_age_stats(movies, 2017)


class RatingTierTestCase(unittest.TestCase):
    def test_rating_tier(self):
        self.assertEqual(rating_tier(9.1), "шедевр")
        self.assertEqual(rating_tier(9), "шедевр")
        self.assertEqual(rating_tier(8.9), "хорошо")
        self.assertEqual(rating_tier(7.5), "хорошо")
        self.assertEqual(rating_tier(7), "хорошо")
        self.assertEqual(rating_tier(6.9), "средне")
        self.assertEqual(rating_tier(5.5), "средне")
        self.assertEqual(rating_tier(5), "средне")
        self.assertEqual(rating_tier(4.9), "слабо")
        self.assertEqual(rating_tier(1), "слабо")
        self.assertEqual(rating_tier(0), "слабо")


class DecadeLabelTestCase(unittest.TestCase):
    def test_decade_label(self):
        self.assertEqual(decade_label(2026), "новые")
        self.assertEqual(decade_label(2021), "новые")
        self.assertEqual(decade_label(2020), "недавние")
        self.assertEqual(decade_label(2017), "недавние")
        self.assertEqual(decade_label(2015), "недавние")
        self.assertEqual(decade_label(2014), "старые")
        self.assertEqual(decade_label(1980), "старые")


class CountMongMoviesTestCase(unittest.TestCase):
    def test_count_long_movies_empty_list(self):
        self.assertEqual(count_long_movies([]), 0)

    def test_count_long_movies_default_threshold(self):
        movies = [
            {"title": "The Dune Chronicles", "year": 2021,
             "genres": {"sci-fi", "drama"},
             "rating": 8.6, "duration_min": 155,
             "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"]},
            {"title": "Kitchen Stories", "year": 2019,
             "genres": {"comedy", "drama"},
             "rating": 7.1, "duration_min": 98,
             "actors": ["A. Novak", "M. Ferguson"]},
            {"title": "silent hours", "year": 2016,
             "genres": {"thriller", "drama"},
             "rating": 6.4, "duration_min": 112,
             "actors": ["J. Bloom", "K. Lee"]},
        ]
        self.assertEqual(count_long_movies(movies), 1)

    def test_count_long_movies_specified_threshold(self):
        movies = [
            {"title": "The Dune Chronicles", "year": 2021,
             "genres": {"sci-fi", "drama"},
             "rating": 8.6, "duration_min": 155,
             "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"]},
            {"title": "Kitchen Stories", "year": 2019,
             "genres": {"comedy", "drama"},
             "rating": 7.1, "duration_min": 98,
             "actors": ["A. Novak", "M. Ferguson"]},
            {"title": "silent hours", "year": 2016,
             "genres": {"thriller", "drama"},
             "rating": 6.4, "duration_min": 112,
             "actors": ["J. Bloom", "K. Lee"]},
        ]
        self.assertEqual(count_long_movies(movies, 100), 2)


class NormalizeTitleTestCase(unittest.TestCase):
    def test_normalize_title(self):
        self.assertEqual(normalize_title(""), "")
        self.assertEqual(normalize_title("title"), "Title")
        self.assertEqual(normalize_title("Title"), "Title")
        self.assertEqual(normalize_title("titLe"), "TitLe")
        self.assertEqual(normalize_title("TitlE"), "TitlE")
        self.assertEqual(normalize_title("many words"), "Many Words")
        self.assertEqual(normalize_title("Many words"), "Many Words")
        self.assertEqual(normalize_title("many Words"), "Many Words")
        self.assertEqual(normalize_title("Many Words"), "Many Words")
        self.assertEqual(normalize_title("manY woRds"), "ManY WoRds")
        self.assertEqual(normalize_title("MANY WORDS"), "MANY WORDS")


class MakeSlugTestCase(unittest.TestCase):
    def test_make_slug(self):
        self.assertEqual(make_slug(""), "")
        self.assertEqual(make_slug("title"), "title")
        self.assertEqual(make_slug("Title"), "title")
        self.assertEqual(make_slug("titLe"), "title")
        self.assertEqual(make_slug("TitlE"), "title")
        self.assertEqual(make_slug("many words"), "many-words")
        self.assertEqual(make_slug("Many words"), "many-words")
        self.assertEqual(make_slug("many Words"), "many-words")
        self.assertEqual(make_slug("Many Words"), "many-words")
        self.assertEqual(make_slug("manY woRds"), "many-words")
        self.assertEqual(make_slug("MANY WORDS"), "many-words")
        # Для замены последовательности пробелов одним дефисом
        # потребовалалось бы применить re.replace
        # или многократное применение str.replace
        self.assertEqual(make_slug("many  words"), "many--words")        


class FormatReportLineTestCase(unittest.TestCase):
    def test_format_report_line(self):
        self.assertEqual(format_report_line({
            "title": "The Quiet Algorithm",
            "year": 2024,
            "genres": {"sci-fi", "drama"},
            "rating": 9.2,
            "duration_min": 118,
            "actors": ["M. Ferguson", "O. Isaac"]
        }),
        '"The Quiet Algorithm" (2024) — 9.2/10, 1ч 58м, жанры: drama, sci-fi')


class TitlesSortedByRatingTestCase(unittest.TestCase):
    def test_titles_sorted_by_rating_empty_list(self):
        self.assertEqual(titles_sorted_by_rating([]), [])

    def test_titles_sorted_by_rating(self):
        movies = [
            {"title": "Kitchen Stories", "year": 2019,
             "genres": {"comedy", "drama"},
             "rating": 7.1, "duration_min": 98,
             "actors": ["A. Novak", "M. Ferguson"]},
            {"title": "The Dune Chronicles", "year": 2021,
             "genres": {"sci-fi", "drama"},
             "rating": 8.6, "duration_min": 155,
             "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"]},
            {"title": "silent hours", "year": 2016,
             "genres": {"thriller", "drama"},
             "rating": 6.4, "duration_min": 112,
             "actors": ["J. Bloom", "K. Lee"]},
        ]
        self.assertEqual(titles_sorted_by_rating(movies),
        ["The Dune Chronicles",
         "Kitchen Stories",
         "silent hours",
        ])


class TopNByRatingTestCase(unittest.TestCase):
    def test_top_n_by_rating_empty_list(self):
        self.assertEqual(top_n_by_rating([]), [])

    def test_top_n_by_rating_default_n(self):
        movies = [
            {"title": "The Dune Chronicles", "year": 2021,
             "genres": {"sci-fi", "drama"},
             "rating": 8.6, "duration_min": 155,
             "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"]},
            {"title": "Kitchen Stories", "year": 2019, "genres": {"comedy", "drama"},
             "rating": 7.1, "duration_min": 98, "actors": ["A. Novak", "M. Ferguson"]},
            {"title": "silent hours", "year": 2016, "genres": {"thriller", "drama"},
             "rating": 6.4, "duration_min": 112, "actors": ["J. Bloom", "K. Lee"]},
            {"title": "Comet Racers", "year": 2023, "genres": {"sci-fi", "action"},
             "rating": 5.9, "duration_min": 101, "actors": ["O. Isaac", "P. Diaz"]},
            {"title": "The Last Bakery", "year": 2014, "genres": {"comedy"},
             "rating": 7.8, "duration_min": 89, "actors": ["A. Novak", "T. Chalamet"]},
        ]
        self.assertEqual(top_n_by_rating(movies),
        [("The Dune Chronicles", 8.6),
         ("The Last Bakery", 7.8),
         ("Kitchen Stories", 7.1),
        ])

    def test_top_n_by_rating_specified_n(self):
        movies = [
            {"title": "The Dune Chronicles", "year": 2021,
             "genres": {"sci-fi", "drama"},
             "rating": 8.6, "duration_min": 155,
             "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"]},
            {"title": "Kitchen Stories", "year": 2019, "genres": {"comedy", "drama"},
             "rating": 7.1, "duration_min": 98, "actors": ["A. Novak", "M. Ferguson"]},
            {"title": "silent hours", "year": 2016, "genres": {"thriller", "drama"},
             "rating": 6.4, "duration_min": 112, "actors": ["J. Bloom", "K. Lee"]},
            {"title": "Comet Racers", "year": 2023, "genres": {"sci-fi", "action"},
             "rating": 5.9, "duration_min": 101, "actors": ["O. Isaac", "P. Diaz"]},
            {"title": "The Last Bakery", "year": 2014, "genres": {"comedy"},
             "rating": 7.8, "duration_min": 89, "actors": ["A. Novak", "T. Chalamet"]},
        ]
        self.assertEqual(top_n_by_rating(movies, 2),
        [("The Dune Chronicles", 8.6),
         ("The Last Bakery", 7.8),
        ])

    def test_top_n_by_rating_n_more_than_list_length(self):
        movies = [
            {"title": "The Dune Chronicles", "year": 2021,
             "genres": {"sci-fi", "drama"},
             "rating": 8.6, "duration_min": 155,
             "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"]},
            {"title": "Kitchen Stories", "year": 2019, "genres": {"comedy", "drama"},
             "rating": 7.1, "duration_min": 98, "actors": ["A. Novak", "M. Ferguson"]},
        ]
        self.assertEqual(top_n_by_rating(movies, 5),
        [("The Dune Chronicles", 8.6),
         ("Kitchen Stories", 7.1),
        ])


class CountByGenreTestCase(unittest.TestCase):
    def test_count_by_genre_empty_list(self):
        self.assertEqual(count_by_genre([]), {})

    def test_count_by_genre(self):
        movies = [
            {"title": "Kitchen Stories", "year": 2019,
             "genres": {"comedy", "drama"},
             "rating": 7.1, "duration_min": 98,
             "actors": ["A. Novak", "M. Ferguson"]},
            {"title": "The Dune Chronicles", "year": 2021,
             "genres": {"sci-fi", "drama"},
             "rating": 8.6, "duration_min": 155,
             "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"]},
            {"title": "silent hours", "year": 2016,
             "genres": {"thriller", "drama"},
             "rating": 6.4, "duration_min": 112,
             "actors": ["J. Bloom", "K. Lee"]},
        ]
        self.assertEqual(count_by_genre(movies), {
            "comedy": 1,
            "drama": 3,
            "sci-fi": 1,
            "thriller": 1,
        })


class ActorFilmographyTestCase(unittest.TestCase):
    def test_actor_filmography_empty_list(self):
        self.assertEqual(actor_filmography([]), {})

    def test_actor_filmography(self):
        movies = [
            {"title": "Kitchen Stories", "year": 2019,
             "genres": {"comedy", "drama"},
             "rating": 7.1, "duration_min": 98,
             "actors": ["A. Novak", "M. Ferguson"]},
            {"title": "The Dune Chronicles", "year": 2021,
             "genres": {"sci-fi", "drama"},
             "rating": 8.6, "duration_min": 155,
             "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"]},
            {"title": "silent hours", "year": 2016,
             "genres": {"thriller", "drama"},
             "rating": 6.4, "duration_min": 112,
             "actors": ["J. Bloom", "K. Lee"]},
            {"title": "The Last Bakery", "year": 2014, "genres": {"comedy"},
             "rating": 7.8, "duration_min": 89,
             "actors": ["A. Novak", "T. Chalamet"]},
        ]
        self.assertEqual(actor_filmography(movies), {
            "A. Novak": ["Kitchen Stories", "The Last Bakery"],
            "J. Bloom": ["silent hours"],
            "K. Lee": ["silent hours"],
            "M. Ferguson": ["Kitchen Stories"],
            "O. Isaac": ["The Dune Chronicles"],
            "R. Ferguson": ["The Dune Chronicles"],
            "T. Chalamet": ["The Dune Chronicles", "The Last Bakery"],
        })


class AboveAverageTestCase(unittest.TestCase):
    def test_above_average_empty_list(self):
        self.assertEqual(above_average([]), {})

    def test_above_average(self):
        movies = [
            {"title": "Kitchen Stories", "year": 2019,
             "genres": {"comedy", "drama"},
             "rating": 7.1, "duration_min": 98,
             "actors": ["A. Novak", "M. Ferguson"]},
            {"title": "The Dune Chronicles", "year": 2021,
             "genres": {"sci-fi", "drama"},
             "rating": 8.6, "duration_min": 155,
             "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"]},
            {"title": "silent hours", "year": 2016,
             "genres": {"thriller", "drama"},
             "rating": 6.4, "duration_min": 112,
             "actors": ["J. Bloom", "K. Lee"]},
            {"title": "The Last Bakery", "year": 2014, "genres": {"comedy"},
             "rating": 7.8, "duration_min": 89,
             "actors": ["A. Novak", "T. Chalamet"]},
        ]
        self.assertEqual(above_average(movies), {
            "The Dune Chronicles": 8.6,
            "The Last Bakery": 7.8,
        })


class AllGenresTestCase(unittest.TestCase):
    def test_all_genres_empty_list(self):
        self.assertEqual(all_genres([]), set())

    def test_all_genres(self):
        movies = [
            {"title": "Kitchen Stories", "year": 2019,
             "genres": {"comedy", "drama"},
             "rating": 7.1, "duration_min": 98,
             "actors": ["A. Novak", "M. Ferguson"]},
            {"title": "The Dune Chronicles", "year": 2021,
             "genres": {"sci-fi", "drama"},
             "rating": 8.6, "duration_min": 155,
             "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"]},
            {"title": "silent hours", "year": 2016,
             "genres": {"thriller", "drama"},
             "rating": 6.4, "duration_min": 112,
             "actors": ["J. Bloom", "K. Lee"]},
            {"title": "The Last Bakery", "year": 2014, "genres": {"comedy"},
             "rating": 7.8, "duration_min": 89,
             "actors": ["A. Novak", "T. Chalamet"]},
        ]
        self.assertEqual(all_genres(movies), {
            "comedy",
            "drama",
            "sci-fi",
            "thriller",
        })


class CommonActorsTestCase(unittest.TestCase):
    def test_common_actors_no_common(self):
        movie1 = {"title": "Kitchen Stories", "year": 2019,
             "genres": {"comedy", "drama"},
             "rating": 7.1, "duration_min": 98,
             "actors": ["A. Novak", "M. Ferguson"],
            }
        movie2 = {"title": "The Dune Chronicles", "year": 2021,
             "genres": {"sci-fi", "drama"},
             "rating": 8.6, "duration_min": 155,
             "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"],
            }
        self.assertEqual(common_actors(movie1, movie2), set())

    def test_common_actors(self):
        movie1 = {"title": "Kitchen Stories", "year": 2019,
             "genres": {"comedy", "drama"},
             "rating": 7.1, "duration_min": 98,
             "actors": ["A. Novak", "M. Ferguson"]
            }
        movie2 = {"title": "The Last Bakery", "year": 2014, "genres": {"comedy"},
             "rating": 7.8, "duration_min": 89,
             "actors": ["A. Novak", "T. Chalamet"],
            }
        self.assertEqual(common_actors(movie1, movie2), {"A. Novak"})


class GenresOnlyInOneTestCase(unittest.TestCase):
    def test_genres_only_in_one(self):
        movies_a = [
            {"title": "Kitchen Stories", "year": 2019,
             "genres": {"comedy", "drama"},
             "rating": 7.1, "duration_min": 98,
             "actors": ["A. Novak", "M. Ferguson"]},
            {"title": "The Dune Chronicles", "year": 2021,
             "genres": {"sci-fi", "drama"},
             "rating": 8.6, "duration_min": 155,
             "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"]},
        ]
        movies_b = [
            {"title": "silent hours", "year": 2016,
             "genres": {"thriller", "drama"},
             "rating": 6.4, "duration_min": 112,
             "actors": ["J. Bloom", "K. Lee"]},
            {"title": "The Last Bakery", "year": 2014, "genres": {"comedy"},
             "rating": 7.8, "duration_min": 89,
             "actors": ["A. Novak", "T. Chalamet"]},
        ]
        self.assertEqual(genres_only_in_one(movies_a, movies_b), {"sci-fi"})

    
if __name__ == '__main__':
    unittest.main()
