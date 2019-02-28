-- :name create-hole
-- :doc Get creates a hole
-- :command :insert
INSERT INTO holes (cid, par, num) VALUES (:cid, :par, :hole)

-- :name get-holes-for-course
-- :doc Gets all the holes for a course
-- :command :query
SELECT par from holes WHERE cid=:cid ORDER BY num
