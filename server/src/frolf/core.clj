(ns frolf.core)

(use 'frolf.database)
(use 'frolf.web)

;;;; Security ;;;;

(defn hash-password [password]
  password)

(defn check-password [password hash]
  (= (hash-password password) hash))

(defn validate-token [tok]
  (if-let [tok (. Integer parseInt tok)] ; this throws an error for non numbers
    tok))

(defn generate-token [gid]
  gid)

;;;; Endpoints ;;;;

(defn signin-group [group password]
  (let [val (get-group-by-username db {:name group})]
    (if (empty? val)
      (throw (ex-info "No group in database" {:status 401 :usr-msg "Group does not exist"}))
      (if (check-password password ((first val) :pass))
        {:body {:tok (generate-token ((first val) :id))}}
        (throw (ex-info "Password could not be validated" {:status 401 :usr-msg "Incorrect Password"}))))))

(defn create-group [group password]
  (let [val (get-group-by-username db {:name group})]
    (if (empty? val)
      (do (add-group db {:group group :pass (hash-password password)})
        (signin-group group password))
      (throw (ex-info "Group already exists" {:status 409 :usr-msg "Group already exists"})))))

(defn courses-by-group [gid]
  "returns all courses matching that gid"
  (let [val (get-courses-by-group-id db {:gid gid})]
    {:body {:holes val}}))

(defn users-by-group [gid]
  "returns all courses matching that gid"
  (let [val (get-users-by-group-id db {:gid gid})]
    {:body {:users val}}))

(defn user-by-id [gid uid]
  "returns the user matching that uid"
  (let [val (get-user-in-group db {:uid uid, :gid gid})]
    (if (empty? val)
      nil
      {:body {:users val}})))

(defn course-by-id [gid cid]
  "returns the course matching that uid"
  (let [val (get-course-in-group db {:cid cid, :gid gid})]
    (if (empty? val)
      nil
      {:body {:courses val}})))

(defn game-by-id [gid id]
  "returns the course matching that uid"
  (let [val (get-game db {:id id})]
    (if (empty? val)
      nil
      {:body {:game val}})))

(defn new-user [gid name]
  (add-user gid name)
  nil)

(defn new-course [gid name pars]
  (add-course gid name pars)
  nil)

(defn new-game [gid time cid players scores]
  (add-game gid cid name scores time)
  nil)
