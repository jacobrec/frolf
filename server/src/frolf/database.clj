(ns frolf.database
  (:require [hugsql.core :as hugsql]))

(def info (clojure.edn/read-string (slurp ".password")))

(def db { :subprotocol "mysql"
          :subname "//127.0.0.1:3306/golf?useSSL=false"
          :user (info :username)
          :password (info :password)})


(hugsql/def-db-fns "frolf/sql/setup.sql")

(hugsql/def-db-fns "frolf/sql/games.sql")
(hugsql/def-db-fns "frolf/sql/users.sql")
(hugsql/def-db-fns "frolf/sql/groups.sql")
(hugsql/def-db-fns "frolf/sql/holes.sql")
(hugsql/def-db-fns "frolf/sql/courses.sql")
(hugsql/def-db-fns "frolf/sql/scores.sql")

(defn setup-database []
  (println "Created database")
  ;; clear old tables
  (clear-table-users db)
  (clear-table-groups db)
  (clear-table-courses db)
  (clear-table-holes db)
  (clear-table-games db)
  (clear-table-scores db)
  ;; clear old joins
  (clear-table-usergame db)

  ;; create tables
  (create-table-users db)
  (create-table-groups db)
  (create-table-courses db)
  (create-table-holes db)
  (create-table-games db)
  (create-table-scores db)
  ;; create joins
  (create-table-usergame db))

(defn add-course [gid name pars]
  ;; TODO: check for identical courses, and just add this to the group
  (create-course db {:name name, :gid gid})
  (let [id ((first (get-last-course-added-by-name db {:name name})) :id)]
    (reduce (fn [i par]
              (create-hole db {:hole i, :cid id, :par par})
              (+ 1 i))
            1 pars)))

(defn add-user [gid name]
  (create-user db {:name name, :gid gid}))

(defn add-game [gid cid players scores time]
  (create-game db {:gid gid, :cid cid, :time time})
  (let [gameId 0] ;; TODO get actual game id
    (doseq [i (range (count players))]
      (let [pid (nth players i), score (nth scores i)]
        (doseq [j (range (count score))]
          (create-score db {:pid pid, :gid gameId, :hole (+ j 1), :score (nth score j)}))))))
     

(defn fake-data []
  (add-group db {:group "frolf" :pass "pass"})
  (add-group db {:group "test" :pass "test"})
  (add-course 1 "Rundle" '(3 3 3 3 3 3 4 3 3 3 3 3 3 3 3 3 3 4))
  (add-course 2 "Rundle" '(3 3 3 3 3 3 4 3 3 3 3 3 3 3 3 3 3 4))
  (add-course 1 "Leduc"  '(3 3 3 3 3 3 4 3 3))
  (add-user 1 "Jacob")
  (add-user 1 "Peter")
  (add-user 1 "Isaac")
  (add-user 1 "Graham")
  (add-user 1 "Ben")
  (add-user 2 "Testy McTestface")
  (add-user 2 "Testy McTesterson")
  (add-user 2 "Testy Tersteresta")
  (add-game 1 3 '(1 2) ; gid 1 is frolf, course 3 is Leduce, user 1 is Jacob, user 2 is Peter
            '((3 3 3 3 3 3 4 3 3) (4 4 4 4 4 4 5 4 4))
            (System/currentTimeMillis)))
