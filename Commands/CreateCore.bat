curl "http://localhost:8984/solr/admin/cores?action=CREATE&name=%1&instanceDir=%~dp0..\%2&config=%~dp0..\%2\conf\solrconfig.xml&schema=%~dp0..\%2\conf\schema.xml&dataDir=%~dp0..\%2\data"
