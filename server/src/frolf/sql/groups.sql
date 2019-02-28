-- :name get-group
-- :doc Get group by id
-- :command :query
SELECT * from groups WHERE id=:id;

-- :name get-group-by-username
-- :doc Get group by username
-- :command :query
SELECT * from groups WHERE name=:name;

-- :name add-group
-- :doc Adds a new group
-- :command :insert
INSERT INTO groups (name, pass) VALUES (:group, :pass);
