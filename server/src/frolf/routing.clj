(ns frolf.routing)

(def j-api-methods '(get put delete post))

;; TODO fix this macro to generate the route maps in j-route-init
(defmacro make-route-maps []
  (list 'apply 'map 'list (reduce (fn [acc m] (conj acc (list 'def (symbol (eval (str m "-routes"))) '{}))) () j-api-methods)))

(defmacro j-route-init []
  '(do
      (def get-routes {})
      (def put-routes {})
      (def delete-routes {})
      (def post-routes {})

      (defn uri-matches [route uri]
        (re-matches route uri))

      (defn handler [request]
        (let [routes (cond (= (request :request-method) :get) get-routes
                          (= (request :request-method) :put) put-routes
                          (= (request :request-method) :delete) delete-routes
                          (= (request :request-method) :post) post-routes)]
          (let [route (some #(if (uri-matches % (request :uri)) % nil) (keys routes))]
            (apply (routes route) request (drop 2 (re-matches route (request :uri)))))))))


(defn j-api [routes uri handler]
  (list 'def routes (list 'assoc routes (re-pattern (str #"()/?" uri)) handler)))

(defmacro get [uri handler]
  (j-api 'get-routes uri handler))

(defmacro put [uri handler]
  (j-api 'put-routes uri handler))

(defmacro delete [uri handler]
  (j-api 'delete-routes uri handler))

(defmacro post [uri handler]
  (j-api 'post-routes uri handler))

