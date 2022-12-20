setlocal enableextensions
set name=%DATE:/=_%
cd C:\Program Files\MongoDB\Tools\100\bin
mongodump -h localhost:27017 -d development -o C:/Users/Administrator/Desktop/mongodb_automatic_Backup/%name%
