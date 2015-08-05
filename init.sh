#!/bin/bash
GREEN='\033[0;32m'
NO_COLOR='\033[0m'

SOLR_VERSION=4.10.4

rm -f database.db

echo -e "${GREEN}Synchronize database...${NO_COLOR}"
python ./app/manage.py syncdb --noinput

echo -e "${GREEN}Downloading SOLR ${SOLR_VERSION}...${NO_COLOR}"
wget https://archive.apache.org/dist/lucene/solr/$SOLR_VERSION/solr-$SOLR_VERSION.tgz
rm -rf solr-$SOLR_VERSION
tar xzf solr-$SOLR_VERSION.tgz

echo -e "${GREEN}Preparing schema.xml...${NO_COLOR}"
python ./app/manage.py build_solr_schema > solr-$SOLR_VERSION/example/solr/collection1/conf/schema.xml

echo -e "${GREEN}Enabling \"More Like This\" feature...${NO_COLOR}"
sed -ri 's$</config>$  <requestHandler name="/mlt" class="solr.MoreLikeThisHandler" />\n</config>$g' solr-$SOLR_VERSION/example/solr/collection1/conf/solrconfig.xml

echo -e "${GREEN}Waitinig for SOLR to start...${NO_COLOR}"
cd solr-$SOLR_VERSION/example/
java -jar start.jar 2>&1 &
SOLR_PID=$!

trap ctrl_c INT
function ctrl_c() {
    echo -e "${GREEN}\nKilling SOLR...${NO_COLOR}"
    kill -9 $SOLR_PID
    echo -e "${GREEN}done${NO_COLOR}"
}
cd -

sleep 10

echo -e "${GREEN}Initilize a SOLR index...${NO_COLOR}"
python ./app/manage.py update_index

echo -e "${GREEN}Almost ready...${NO_COLOR}"
python ./app/manage.py runserver
