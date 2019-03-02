(ns frolf.main)

(use 'ring.adapter.jetty)
(use 'frolf.web)
(use 'frolf.database)


(def app
  (-> handler
      (parse-json-body)
      (frolf-request)))

(defn -main [& args]
  (if (some #(= % "--setup") args)
    (setup-database))
  (if (some #(= % "--fake") args)
    (fake-data))

  (println "### Starting Server " args "###")
  (println "### Closing Server ###"))

(def system {})

(defn start-server []
  (def system (assoc system :server (run-jetty app {:port 3000, :join? false}))))

(defn stop-server []
  (.stop (system :server))
  (def system (dissoc system :server)))
