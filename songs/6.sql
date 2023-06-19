-- Lists the names of songs that are by Post Malone.

SELECT name FROM songs where artist_id = (SELECT id FROM artists WHERE name = "Post Malone");