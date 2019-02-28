(ns frolf.main)

(use 'ring.adapter.jetty)
(use 'frolf.web)
(use 'frolf.database)

(defn -main [& args]
  (println "### Starting Server " args "###")

  (if (some #(= % "--setup") args)
    (setup-database))
  (if (some #(= % "--fake") args)
    (fake-data))

  (def app
    (-> handler
        (parse-json-body)
        (frolf-request)))

  (run-jetty app {:port 3000})
  (println "### Closing Server ###"))
