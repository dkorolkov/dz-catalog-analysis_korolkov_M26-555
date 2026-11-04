import unittest

from catalog_analysis import average_rating, catalog_age_stats, duration_in_hours


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

if __name__ == '__main__':
    unittest.main()
