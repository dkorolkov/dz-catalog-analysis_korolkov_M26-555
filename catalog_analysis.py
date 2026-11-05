from math import ceil

movies = [
    {"title": "The Dune Chronicles", "year": 2021, "genres": {"sci-fi", "drama"},
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
    {"title": "midnight in oslo", "year": 2020, "genres": {"thriller", "mystery"},
     "rating": 8.9, "duration_min": 124, "actors": ["K. Lee", "R. Ferguson"]},
    {"title": "Garden of Static", "year": 2022, "genres": {"drama"},
     "rating": 4.8, "duration_min": 137, "actors": ["P. Diaz", "J. Bloom"]},
    {"title": "The Quiet Algorithm", "year": 2024, "genres": {"sci-fi", "drama"},
     "rating": 9.2, "duration_min": 118, "actors": ["M. Ferguson", "O. Isaac"]},
    {"title": "Two Left Shoes", "year": 2011, "genres": {"comedy"},
     "rating": 6.0, "duration_min": 95, "actors": ["A. Novak", "K. Lee"]},
    {"title": "Red Harbor", "year": 2018, "genres": {"action", "thriller"},
     "rating": 7.3, "duration_min": 129, "actors": ["P. Diaz", "T. Chalamet"]},
]

def average_rating(movies: list) -> float:
    s = 0
    count = 0
    for movie in movies:
        if "rating" in movie:
            s += movie["rating"]
            count += 1

    if count == 0:
        raise ValueError
        
    return round(s/count, 1)

def catalog_age_stats(movies: list, current_year: int=2026) -> tuple:
    oldest = newest = None
    count = 0
    age_sum = 0
    for movie in movies:
        if "year" in movie:
            age = current_year - movie["year"]
            if age < 0:
                raise ValueError
            if count == 0:
                oldest = newest = age
            else:
                if oldest < age:
                    oldest = age
                if newest > age:
                    newest = age
            age_sum += age
            count += 1

    if count == 0:
        raise ValueError
        
    return oldest, newest, ceil(age_sum/count)

def duration_in_hours(minutes: int) -> str:
    if minutes < 0:
        raise ValueError
    return f"{minutes // 60}ч {minutes % 60}м"

def rating_tier(rating: float) -> str:
    if rating >= 9:
        return "шедевр"
    elif rating >= 7:
        return "хорошо"
    else:
        return "средне" if rating >= 5 else "слабо"

def decade_label(year: int) -> str:
    match year:
        case _ if year > 2020:
            return "новые"
        case _ if 2015 <= year <= 2020:
            return "недавние"
        case _:
            return "старые"
            
def count_long_movies(movies: list, threshold: int=120) -> int:
    count = 0
    for movie in movies:
        dur = movie.get("duration_min", -1)
        if dur > threshold:
            count += 1
            
    return count
    
    
def print_not_comedy_titles(movies: list):
    print("Не комедии:")
    for movie in movies:
        genres = movie.get("genres", set())
        if "comedy" in genres:
            continue
        print(movie.get("title", "Нет названия"))
            
def first_masterpiece(movies: list) -> dict:
    for movie in movies:
        if movie.get("rating", -1) > 9:
            print(f"Найден шедевр: {movie.get("title", "Нет названия")}")
            break
    else:
        print("Шедевров не найдено")

def main():
    print("Hello from hw1!")
    print(f"{average_rating(movies)=}")
    print(f"{catalog_age_stats(movies)=}")
    print("Durations:")
    for movie in movies:
        print(f"{movie["title"]} {duration_in_hours(movie["duration_min"])}")
    print(f"{rating_tier(10)=}")
    print(f"{decade_label(1969)=}")
    print_not_comedy_titles(movies)
    first_masterpiece(movies)
    first_masterpiece([
    {"title": "The Dune Chronicles", "year": 2021, "genres": {"sci-fi", "drama"},
     "rating": 8.6, "duration_min": 155,
     "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"]}
     ])
    print(f"Длинных фильмов: {count_long_movies(movies)}")


if __name__ == "__main__":
    main()
