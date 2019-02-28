-- :name get-course-in-group
-- :doc Get course by id
SELECT name FROM courses WHERE gid=:gid AND id=:cid;

-- :name get-courses-by-group-id
-- :doc Get course by id
-- :command :query
SELECT * FROM courses WHERE gid=:gid 

-- :name create-course
-- :doc Creates a new course
-- :command :insert
INSERT INTO courses (name, gid) VALUES (:name, :gid)

-- :name get-last-course-added-by-name
-- :doc Gets the most recently added course by name
-- :command :query
SELECT * FROM courses WHERE name=:name ORDER BY id DESC LIMIT 1
