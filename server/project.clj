(defproject frolf "0.1.0"
  :description "A scorekeeping application for frisbee golf"
  :url "http://example.com/FIXME"
  :license {:name "GNU Affero General Public License"
            :url "https://www.gnu.org/licenses/agpl.txt"}
  :dependencies [[org.clojure/clojure "1.10.0"]
                 [ring "1.7.1"]
                 [mysql/mysql-connector-java "8.0.15"]
                 [cheshire "5.8.1"]
                 [com.layerware/hugsql "0.4.9"]
                 [com.layerware/hugsql-adapter-clojure-java-jdbc "0.4.9"]
                 [com.layerware/hugsql-adapter-clojure-jdbc "0.4.9"]]
  :ring {:handler frolf.main/app}
  :main frolf.main
  :repl-options {:init-ns frolf.main}
  :plugins [[cider/cider-nrepl "0.21.1"]])
