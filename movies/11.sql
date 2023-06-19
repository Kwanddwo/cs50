-- list the titles of the five highest rated movies (in order) that Chadwick Boseman starred in, starting with the highest rated.

SELECT title FROM (stars JOIN ratings ON stars.movie_id = ratings.movie_id JOIN movies ON ratings.movie_id = movies.id) WHERE person_id = (SELECT id FROM people WHERE name = "Chadwick Boseman") ORDER BY rating DESC LIMIT 5;