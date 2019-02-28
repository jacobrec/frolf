-- :name get-game
-- :doc Get game by id
-- :command :query
SELECT * from games WHERE id=:id

-- :name create-game
-- :doc Creates a game
-- :command :insert
INSERT INTO games (gid, cid, time) VALUES (:gid, :cid, :time)
