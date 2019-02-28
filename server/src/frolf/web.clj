(ns frolf.web
  (:require [cheshire.core :refer :all]))

(use 'frolf.routing)
(use 'frolf.core)

(j-route-init)

;;;;; Web utils ;;;;;

(defn json-response
  ([res]
   (json-response (or (res :status) 200) (res :body)))
  ([status body]
   {:status status
    :headers {"Content-Type" "application/json"}
    :body (generate-string body)}))


(defn http-request-error-responder [e status msg]
  (if (= status (-> e ex-data :status))
    (json-response status {:error (or (-> e ex-data :usr-msg) msg)})))

(defn frolf-request [handler]
  (fn [request]
    (try
      (if-let [res (handler request)]
        (json-response res)
        (json-response 204 {}))
      (catch clojure.lang.ExceptionInfo e
        (println (str "### Error: " (.getMessage e) " ###"))
        (or (http-request-error-responder e 501 "Method not yet implemented")
            (http-request-error-responder e 400 "Bad request")
            (http-request-error-responder e 401 "Authentication failed")
            (http-request-error-responder e 404 "Authentication Denied")
            (http-request-error-responder e 409 "Resource Conflict")
            (json-response 500 {:error "Internal Server Error, this should really be handled better"})))
      (catch Exception e
        (println e)
        (json-response 500 {:error "Internal Server Error"})))))

(defn parse-json-body [handler]
  (fn [request]
    (handler (assoc request :json (parse-string (slurp (request :body)))))))

(defn endpoint [handler request jsons]
  (let [parsed (map #((request :json) %) jsons)]
    (if (some #(= nil %) parsed)
      (throw (ex-info "Could not find json variables" {:status 400 :info {:wanted jsons, :got parsed}}))
      (apply handler parsed))))

(defn secure-endpoint [handler request jsons]
  "this parses and validates the token. if valid, calls the handler, passes in the id first, then any other params from jsons"
  (let [tok ((request :json) "tok")]
    (if-let [tok (validate-token tok)]
      (endpoint handler (assoc-in request [:json :id] tok) (into [:id] jsons))
      (throw (ex-info "Invalid token" {:status 401 :usr-msg "Token could not be validated"})))))

;;;;; Endpoints ;;;;;
(get #"api/version"
  (fn api-version [request]
    "Returns the version"
    (json-response {:body {:version "Version 1.0"}})))

(put #"api/group"
  (fn api-group [request]
    "Creates new group"
    (endpoint create-group request ["group" "pass"])))

(post #"api/group/signin"
  (fn api-group-signin [request]
    "Sign in to group"
    (endpoint signin-group request ["group" "pass"])))

(post #"api/group/courses"
  (fn api-group-courses [request]
    "Gets list of courses for a group"
    (secure-endpoint courses-by-group request [])))

(post #"api/group/users"
  (fn api-group-users [request]
    "Gets list of users for a group"
    (secure-endpoint users-by-group request [])))

(post #"api/user"
  (fn api-user-num [request]
    "Gets a user"
    (secure-endpoint user-by-id request ["user"])))

(post #"api/course"
  (fn api-course-num [request]
    "Gets a course"
    (secure-endpoint course-by-id request ["course"])))

(post #"api/game"
  (fn api-game [request]
    "Gets a game"
    (secure-endpoint game-by-id request ["game"])))

(put #"api/user"
  (fn api-user [request]
    "Adds a user"
    (secure-endpoint new-user request ["name"])))

(put #"api/course"
  (fn api-course [request]
    "Adds a course"
    (secure-endpoint new-course request ["name" "pars"])))

(put #"api/game"
  (fn api-game [request]
    "Adds a game"
    (secure-endpoint new-game request ["time" "cid" "players" "scores"])))

(get #".*"
  (fn [request]
    (println "404" request)
    {:status 200
      :headers {"Content-Type" "text/html"}
      :body "<p>404 page not found</p>"}))
