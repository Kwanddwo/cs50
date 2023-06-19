-- List the titles of all movies in which both Johnny Depp and Helena Bonham Carter starred.

SELECT title FROM movies WHERE id IN
(SELECT stars.movie_id FROM (people JOIN stars ON people.id = stars.person_id) WHERE name = "Johnny Depp" INTERSECT
SELECT stars.movie_id FROM (people JOIN stars ON people.id = stars.person_id) WHERE name = "Helena Bonham Carter");