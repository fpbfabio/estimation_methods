echo "usage ./create_core.sh <<core name>> <<core_path>>"
curl "http://localhost:8984/solr/admin/cores?action=CREATE&name=$1&instanceDir=$2&config=$2/conf/solrconfig.xml&schema=$2/conf/schema.xml&dataDir=$2/data"

