-- :name create-score
-- :doc Creates a score
-- :command :insert
INSERT INTO scores (pid, gid, hole, score) VALUES (:pid, :gid, :hole, :score)
