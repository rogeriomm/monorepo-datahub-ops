#/usr/bin/env zsh


VERSION="4.1"

if [ ! -d "spark" ]; then
    git clone https://github.com/apache/spark.git spark-$VERSION
fi

cd spark-$VERSION
git checkout branch-$VERSION


export MAVEN_OPTS="-Xss64m -Xmx2g -XX:ReservedCodeCacheSize=1g"
./build/mvn -DskipTests clean package
