
cd /programs/test_seed/c/
make
cp ./random_c /web-app/bin/test_seed/random_c

cd /programs/test_seed/clojure/
lein uberjar
cp ./target/uberjar/random_clojure.jar /web-app/bin/test_seed/random_clojure.jar


cd /programs/test_seed/java/
mvn package
cp ./target/random_java.jar /web-app/bin/test_seed/random_java.jar

cp /programs/test_seed/python/random_py.py /web-app/bin/test_seed/random_py.py



cd /programs/benchmark/c/
make
mkdir /web-app/bin/programs/c/
cp ./bank_konto_c /web-app/bin/programs/c/bank_konto_c


cd /programs/benchmark/python/
mkdir /web-app/bin/programs/python/
cp ./* /web-app/bin/programs/python/

cd /programs/benchmark/java
mvn package
mkdir /web-app/bin/programs/java/
cp ./target/java_single_process.jar /web-app/bin/programs/java/java_threads.jar


cd /programs/benchmark/clojure/
lein uberjar
mkdir /web-app/bin/programs/clojure/
cp ./target/uberjar/bank_konto.jar /web-app/bin/programs/clojure/bank_konto.jar
