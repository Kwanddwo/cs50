-- list the names of all people who starred in a movie in which Kevin Bacon also starred.
-- Kevin Bacon was born in 1958
-- Kevin Bacon should not be on the list

SELECT name FROM people WHERE id IN (SELECT person_id FROM stars WHERE movie_id IN (SELECT movie_id FROM stars WHERE person_id = (SELECT id FROM people WHERE name = "Kevin Bacon" AND birth = 1958))) and name != "Kevin Bacon"