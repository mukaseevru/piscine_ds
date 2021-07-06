from collections import Counter, defaultdict
import re
from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup as bs
import sys


class InvalidCsv(Exception):
    pass


class CsvParser:
    def __init__(self, filename, sep=',', header=True):
        self.filename = filename
        self.sep = sep
        self.header = header
        self.columns = []
        self.count_features = None

    def open_csv(self):
        with open(self.filename) as fd:
            if self.header:
                self.columns = next(fd).strip('\n').split(',')
                self.count_features = len(self.columns)
            else:
                self.columns = range(int(1e6))
            for row in fd:
                yield row.strip()

    def read_csv(self):
        for row in self.open_csv():
            row_dict = {}
            flag = False
            column_idx = 0
            for obj in row.strip('\n').split(self.sep):
                try:
                    row_dict[self.columns[column_idx]] = row_dict.get(
                        self.columns[column_idx], '') + obj.strip('"')
                except IndexError:
                    print('Invalid CSV')
                    sys.exit()

                if obj.count('"') == 1:
                    flag = not flag

                if flag:
                    row_dict[self.columns[column_idx]] += self.sep
                else:
                    column_idx += 1
            if self.count_features is None:
                self.count_features = len(row_dict)
            if len(row_dict) != self.count_features:
                print('Invalid CSV')
                sys.exit()
            yield row_dict


class Movies(CsvParser):
    """
    Analyzing data from movies.csv
    """

    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        super().__init__(path_to_the_file)

    def is_valid_file(self):
        return set(self.columns) == set('movieId,title,genres'.split(','))

    def read_csv(self):
        for film_info in super(Movies, self).read_csv():
            if not self.is_valid_file():
                print(f'Invalid parse CSV {self.filename}')
                sys.exit()
            yield film_info

    def get_first_film_info(self):
        for film_info in super(Movies, self).read_csv():
            return film_info

    def dist_by_release(self):
        """
        The method returns a dict where the keys are years and the values are counts.
        You need to extract years from the titles. Sort it by counts descendingly.
        """
        release_years = Counter()
        for film_info in self.read_csv():
            try:
                year = int(re.findall(r'\((\d{4})\)', film_info['title'])[-1])
            except IndexError:
                continue
            release_years[year] += 1
        return dict(release_years.most_common())

    def dist_by_genres(self):
        """
        The method returns a dict where the keys are genres and the values are counts.
     Sort it by counts descendingly.
        """
        genres = Counter()
        for film_info in self.read_csv():

            for genre in self._get_film_genre(film_info):
                genres[genre] += 1
        return dict(genres.most_common())

    @staticmethod
    def _get_film_genre(film_info: dict):
        if film_info['genres'] == '(no genres listed)':
            return []
        return film_info['genres'].split('|')

    def most_genres(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """
        movies = Counter()
        for film_info in self.read_csv():
            movies[film_info['title']] = len(self._get_film_genre(film_info))
        return dict(movies.most_common()[:n])


def mean(values):
    if len(values) == 0:
        return float('nan')
    return sum(values) / len(values)


def median(values):
    if len(values) == 0:
        return float('nan')
    items = sorted(values)
    if len(items) % 2 == 1:
        return items[len(items) // 2]
    return (items[len(items) // 2 - 1] + items[len(items) // 2]) / 2


def var(values):
    if not len(values):
        return float('nan')
    mean_value = mean(values)
    squared_diff = [(value - mean_value) ** 2 for value in values]
    return sum(squared_diff) / len(squared_diff)


class Ratings(CsvParser):
    """
    Analyzing data from ratings.csv
    """

    def __init__(self, path_to_the_file, path_to_movies_file):
        """
        Put here any fields that you think you will need.
        """
        super().__init__(path_to_the_file)
        self.filename_movies = path_to_movies_file

    def get_users(self):
        return Ratings.Users(self, self.filename_movies)

    def get_movies(self):
        return Ratings.Movies(self, self.filename_movies)

    def is_valid_file(self):
        return set(self.columns) == set('userId,movieId,rating,timestamp'.split(','))

    def read_csv(self):
        for film_info in super(Ratings, self).read_csv():
            if not self.is_valid_file():
                print(f'Invalid parse CSV {self.filename}')
                sys.exit()
            yield film_info

    class Movies(Movies):
        def __init__(self, rating, movies_filename):
            super().__init__(movies_filename)
            self.rating = rating
            self.movies_id2name = {}

        def init_mapping_movies(self):
            for film_info in self.read_csv():
                self.movies_id2name[film_info['movieId']] = film_info['title']

        def dist_by_year(self):
            """
            The method returns a dict where the keys are years and the values are counts.
            Sort it by years ascendingly. You need to extract years from timestamps.
            """
            ratings_by_year = Counter()
            for film_info in self.rating.read_csv():
                ratings_by_year[datetime.fromtimestamp(int(film_info['timestamp'])).year] += 1
            return dict(ratings_by_year.most_common()[::-1])

        def dist_by_rating(self):
            """
            The method returns a dict where the keys are ratings and the values are counts.
            Sort it by ratings ascendingly.
            """
            ratings_distribution = Counter()
            for film_info in self.rating.read_csv():
                ratings_distribution[float(film_info['rating'])] += 1
            return dict(ratings_distribution.most_common()[::-1])

        def top_by_num_of_ratings(self, n):
            """
            The method returns top-n movies by the number of ratings.
            It is a dict where the keys are movie titles and the values are numbers.
            Sort it by numbers descendingly.
            """
            self.init_mapping_movies()
            if n == -1:
                n = len(self.movies_id2name)
            top_movies = Counter()
            for film_info in self.rating.read_csv():
                top_movies[self.movies_id2name[film_info['movieId']]] += 1
            return dict(top_movies.most_common()[:n])

        def top_by_ratings(self, n, metric='average'):
            """
            The method returns top-n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sort it by metric descendingly.
            The values should be rounded to 2 decimals.
            """
            assert metric in ('average', 'median')
            top_movies = self._groupby_rating_by_film()
            if n == -1:
                n = len(self.movies_id2name)
            if metric == 'average':
                top_movies = [(title, mean(ratings))
                              for title, ratings in top_movies.items()]
            else:
                top_movies = [(title, median(ratings))
                              for title, ratings in top_movies.items()]

            return dict(
                map(lambda x: (x[0], round(x[1], 2)),
                    sorted(top_movies, key=lambda x: x[1], reverse=True)[:n]))

        def _groupby_rating_by_film(self):
            self.init_mapping_movies()
            top_movies = defaultdict(list)
            for film_info in self.rating.read_csv():
                top_movies[self.movies_id2name[film_info['movieId']]].append(
                    float(film_info['rating']))
            return top_movies

        def top_controversial(self, n):
            """
            The method returns top-n movies by the variance of the ratings.
            It is a dict where the keys are movie titles and the values are the variances.
          Sort it by variance descendingly.
            The values should be rounded to 2 decimals.
            """
            if n == -1:
                n = len(self.movies_id2name)
            top_movies = self._groupby_rating_by_film()
            top_movies = [(title, var(ratings))
                          for title, ratings in top_movies.items()]

            return dict(
                map(lambda x: (x[0], round(x[1], 2)),
                    sorted(top_movies, key=lambda x: x[1], reverse=True)[:n]))

    class Users(Movies):
        """
        In this class, three methods should work.
        The 1st returns the distribution of users by the number of ratings made by them.
        The 2nd returns the distribution of users by average or median ratings made by them.
        The 3rd returns top-n users with the biggest variance of their ratings.
        Inherit from the class Movies. Several methods are similar to the methods from it.
        """

        def _groupby_rating_by_film(self):
            self.init_mapping_movies()
            top_movies = defaultdict(list)
            for film_info in self.rating.read_csv():
                top_movies[film_info['userId']].append(
                    float(film_info['rating']))
            return top_movies

        def dist_by_rating(self):
            ratings_distribution = Counter()
            for film_info in self.rating.read_csv():
                ratings_distribution[film_info['userId']] += 1
            return dict(ratings_distribution.most_common()[::-1])

        def dict_by_ratings(self, metric='average'):
            return super().top_by_ratings(-1, metric)

        def top_controversial(self, n):
            return super().top_controversial(n)


class Tags(CsvParser):
    """
    Analyzing data from tags.csv
    """

    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        super().__init__(path_to_the_file)

    def is_valid_file(self):
        return set(self.columns) == set('userId,movieId,tag,timestamp'.split(','))

    def read_csv(self):
        for tags in super(Tags, self).read_csv():
            if not self.is_valid_file():
                print(f'Invalid parse CSV {self.filename}')
                sys.exit()
            tags['tag'] = tags['tag'].lower()
            yield tags

    def most_words(self, n):
        """
        The method returns top-n tags with most words inside. It is a dict
        where the keys are tags and the values are the number of words inside the tag.
        Drop the duplicates. Sort it by numbers descendingly.
        """
        big_tags = Counter()
        for tags in self.read_csv():
            tags_list = self.get_tags(tags)
            big_tags[" ".join(tags_list)] = len(tags_list)
        return dict(big_tags.most_common(n))

    def longest(self, n):
        """
        The method returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
        """
        big_tags = Counter()
        for tags in self.read_csv():
            for tag_list in self.get_tags(tags):
                big_tags[tag_list] = len(tag_list)
        return list(dict(big_tags.most_common(n)).keys())

    def most_words_and_longest(self, n):
        """
        The method returns the intersection between top-n tags with most words inside and
        top-n longest tags in terms of the number of characters.
        Drop the duplicates. It is a list of the tags.
        """
        big_tags = list(set(self.most_words(n)) & set(self.longest(n)))
        return big_tags

    def most_popular(self, n):
        """
        The method returns the most popular tags.
        It is a dict where the keys are tags and the values are the counts.
        Drop the duplicates. Sort it by counts descendingly.
        """
        big_tags = Counter()
        for tags in self.read_csv():
            for tag_list in self.get_tags(tags):
                big_tags[tag_list] += 1
        return dict(big_tags.most_common(n))

    def tags_with(self, word):
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        """
        word = str(word).lower()
        tags_with = set()
        for tags in self.read_csv():
            tag_list = tags['tag']
            if self.contains_tag(str(tag_list), word):
                tags_with.add(str(tag_list))
        return sorted(tags_with)

    @staticmethod
    def get_tags(tags: dict):
        return tags['tag'].split(' ')

    @staticmethod
    def contains_tag(tag_list, word):
        for tag in tag_list.split(" "):
            if tag == word:
                return True
        return False


class Links(CsvParser):
    """
    Analyzing data from links.csv
    """

    def __init__(self, path_to_the_file):
        self.data = []
        super().__init__(path_to_the_file)
        self.data = list(super().read_csv())
        self.global_dict = {}

    def get_imdb(self, list_of_movies, list_of_fields):
        """
        The method returns a list of lists [movieId, field1, field2, field3, ...]
            for the list of movies given as the argument (movieId).
        For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
        The values should be parsed from the IMDB webpages of the movies.
        Sort it by movieId descendingly.
        """
        result = []

        def parse_movie(imdbId):

            def get_info(soap_tag):
                info = str(soap_tag)
                i = 0
                l = len(info)
                while i < l and info[i] != '>':
                    i += 1
                start = i + 1
                while i < l and info[i] != '<':
                    i += 1
                return (info[start:i] if i < l else info).strip()

            link = f'https://www.imdb.com/title/tt{imdbId}/'
            raw_0 = requests.get(link).text

            content = bs(raw_0, features="html.parser")
            raw_1 = content.find(
                'script', attrs={'type': "application/ld+json"})

            dict_info = json.loads(raw_1.contents[0])
            raw_2 = content.find_all('div', attrs={'class': "txt-block"})
            for e in raw_2:
                pair = [el for el in e.contents if el != '\n'][:2]
                dict_info[get_info(pair[0])] = get_info(pair[1])
            return dict_info

        list_of_movies = sorted(list_of_movies, reverse=True)
        for movie in list_of_movies:
            imdb = None
            for row in self.data:
                movie_id = row['movieId']
                imdb_id = row['imdbId']
                if movie == movie_id:
                    imdb = imdb_id
            if imdb is None:
                print(f'Incorrect movie_id: {movie}')
                sys.exit()
            dict_info = parse_movie(imdb)
            dict_v = {movie: ""}

            for field in list_of_fields:
                field_to_lower = field
                try:
                    self.global_dict[movie] = {"director": dict_info["director"]["name"],
                                               "title": dict_info["name"]}
                except KeyError:
                    sys.exit()
                if field_to_lower in dict_info.keys():
                    by_key = dict_info[field_to_lower]
                    try:
                        if isinstance(by_key, list):
                            for key in by_key:
                                if "name" in key:
                                    dict_v[key["name"]] = ""
                        elif isinstance(by_key, dict):
                            dict_v[dict_info[field_to_lower]["name"]] = ""
                        else:
                            dict_v[by_key] = ""
                    except KeyError:
                        print("Key error on filed " + field_to_lower)
                        sys.exit()
            result.append(list(dict_v.keys()))
        return result

    def top_directors(self, n):
        """
        The method returns a dict with top-n directors where the keys are directors and
        the values are numberы of movies created by them. Sort it by numbers descendingly.
        """
        top_directors = Counter()
        for k, v in self.global_dict.items():
            top_directors[v["director"]] += 1
        return top_directors.most_common(n)

    def most_expensive(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their budgets. Sort it by budgets descendingly.
        """
        pass

    def most_profitable(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the difference between cumulative worldwide gross and budget.
        Sort it by the difference descendingly.
        """
        pass

    def longest(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their runtime. If there are more than one version – choose any.
        Sort it by runtime descendingly.
        """
        pass

    def top_cost_per_minute(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles
            and the values are the budgets divided by their runtime.
        The budgets can be in different currencies – do not pay attention to it.
        The values should be rounded to 2 decimals. Sort it by the division descendingly.
        """
        pass


class Tests:
    def setup_class(self):
        self.movies = Movies('movies.csv')
        self.rating = Ratings('ratings.csv', 'movies.csv')
        self.tags = Tags('tags.csv')
        self.links = Links('links.csv')

    def test_movies_dist_by_release(self):
        result = self.movies.dist_by_release()
        assert (isinstance(result, dict) and
                (set(map(type, result.values())) == {int} and
                 set(map(type, result.keys())) == {int}) and
                sorted(result.values(), reverse=True) == list(result.values()))

    def test_movies_dist_by_genres(self):
        result = self.movies.dist_by_genres()
        assert (isinstance(result, dict) and
                (set(map(type, result.values())) == {int} and
                 set(map(type, result.keys())) == {str}) and
                sorted(result.values(), reverse=True) == list(result.values()))

    def test_movies_most_genres(self):
        result = self.movies.most_genres(10)
        assert (isinstance(result, dict) and
                (set(map(type, result.values())) == {int} and
                 set(map(type, result.keys())) == {str}) and
                sorted(result.values(), reverse=True) == list(result.values()))

    def test_rating_dist_by_year(self):
        result = self.rating.get_movies().dist_by_year()
        assert (isinstance(result, dict) and
                (set(map(type, result.values())) == {int} and
                 set(map(type, result.keys())) == {int}) and
                sorted(result.values(), reverse=False) == list(result.values()))

    def test_rating_dist_by_rating(self):
        result = self.rating.get_movies().dist_by_rating()
        assert (isinstance(result, dict) and
                (set(map(type, result.values())) == {int} and
                 set(map(type, result.keys())) == {float}) and
                sorted(result.values(), reverse=False) == list(result.values()))

    def test_rating_top_by_num_of_ratings(self):
        result = self.rating.get_movies().top_by_num_of_ratings(10)
        assert (isinstance(result, dict) and
                (set(map(type, result.values())) == {int} and
                 set(map(type, result.keys())) == {str}) and
                sorted(result.values(), reverse=True) == list(result.values()))

    def test_rating_top_by_ratings(self):
        for metric in ['average', 'median']:
            result = self.rating.get_movies().top_by_ratings(500, metric)
            assert (isinstance(result, dict) and
                    (set(map(type, result.values())) == {float} and
                     set(map(type, result.keys())) == {str}) and
                    sorted(result.values(), reverse=True) == list(result.values()))

    def test_rating_top_controversial(self):
        result = self.rating.get_movies().top_controversial(10)
        assert (isinstance(result, dict) and
                (set(map(type, result.values())) == {float} and
                 set(map(type, result.keys())) == {str}) and
                sorted(result.values(), reverse=True) == list(result.values()))

    def test_tags_most_words(self):
        result = self.tags.most_words(10)
        assert (isinstance(result, dict) and
                (set(map(type, result.values())) == {int} and
                 set(map(type, result.keys())) == {str}) and
                sorted(result.values(), reverse=True) == list(result.values()))

    def test_tags_longest(self):
        big_tags = Counter()
        for tag_s in self.tags.read_csv():
            for tag_list in self.tags.get_tags(tag_s):
                big_tags[tag_list] = len(tag_list)
        result = self.tags.longest(10)
        print(sorted(dict(big_tags).items(), reverse=True, key=lambda x: x[1])[:10])
        assert (isinstance(result, list) and
                set(map(type, result)) == {str} and
                [el[0] for el in sorted(dict(big_tags).items(),
                                        reverse=True, key=lambda x: x[1])[:10]] == list(result))

    def test_tags_most_words_and_longest(self):
        result = self.tags.most_words_and_longest(1000)
        assert (isinstance(result, list) and
                set(map(type, result)) == {str})

    def test_tags_most_popular(self):
        result = self.tags.most_popular(10)
        assert (isinstance(result, dict) and
                (set(map(type, result.values())) == {int} and
                 set(map(type, result.keys())) == {str}) and
                sorted(result.values(), reverse=True) == list(result.values()))

    def test_tags_with(self):
        result = self.tags.tags_with('Netflix')
        assert (isinstance(result, list) and
                set(map(type, result)) == {str} and
                sorted(result, reverse=False) == list(result))

    def test_get_imdb(self):
        result = self.links.get_imdb(['1', '2', '3', '4', '5'], ['director', 'name', 'genre', 'actor'])
        assert (isinstance(result, list) and
                set(map(type, result)) == {list} and
                sorted(result, reverse=True, key=lambda x: x[0]) == list(result))

    def test_top_directors(self):
        self.links.get_imdb(['1', '2', '3', '4', '5'], ['director', 'name', 'genre', 'actor'])
        result = self.links.top_directors(3)
        assert (isinstance(result, list) and
                set(map(type, result)) == {tuple} and
                sorted(result, reverse=True, key=lambda x: x[1]) == list(result))
