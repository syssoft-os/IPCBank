(ns bank.core
  (:gen-class))

(defn create-account [n]
  (vec (repeatedly n #(atom (+ 450 (rand-int 100))))))

(defn transfer [accounts account-from account-to amount]
  (dosync
   (let [from-account (nth accounts account-from)
         to-account (nth accounts account-to)]
     (if (>= @from-account amount)
       (do
         (swap! from-account - amount)
         (swap! to-account + amount))
       () ; else
       ))))

(defn sum [accounts]
  (apply + (map deref accounts)))

(defn client [accounts num-transfers]
  (dotimes [_ num-transfers]
    (let [account-from (rand-int (count accounts))
          account-to (rand-int (count accounts))
          amount (rand-int 100)]
      (transfer accounts account-from account-to amount))))

(defn server [num-accounts num-clients num-transfers]
  (let [start-time (System/currentTimeMillis)
        accounts (create-account num-accounts)
        initial-sum (sum accounts)
        client-futures (vec (repeatedly num-clients #(future (client accounts num-transfers))))]
    (println "Initial sum of account balances: " initial-sum)
    (doseq [f client-futures] (deref f))
    ;(println "Final account balances:")
    ;(doseq [account accounts]
    ;  (println @account))
    (println "Sum of account balances: " (sum accounts))
    (let [end-time (System/currentTimeMillis)
          total-time (-> (- end-time start-time) (float) (/ 1000))]
      (println (str "Total execution time: " total-time " seconds")))
    ))

(defn -main [& args]
  (let [num-accounts (-> (System/getenv "NUM_ACCOUNTS") (or "1000") (Long/parseLong))
        num-clients (-> (System/getenv "NUM_CLIENTS") (or "100") (Integer/parseInt))
        num-transfers (-> (System/getenv "NUM_TRANSFERS") (or "1000000") (Long/parseLong))]
    (server num-accounts num-clients num-transfers)
    (shutdown-agents)))
