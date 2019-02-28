-- :name get-user-in-group
-- :doc Get user by id
SELECT name FROM users WHERE gid=:gid AND id=:uid;

-- :name get-users-by-group-id
-- :doc Get users by group id
-- :command :query
SELECT * FROM users WHERE gid=:gid 

-- :name create-user
-- :doc Creates a new user
-- :command :insert
INSERT INTO users (name, gid) VALUES (:name, :gid)
