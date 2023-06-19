-- Determine the number of movies with an IMDb rating of 10.0.

SELECT COUNT(*) FROM movies WHERE id IN (SELECT movie_id FROM ratings where rating = 10.0);