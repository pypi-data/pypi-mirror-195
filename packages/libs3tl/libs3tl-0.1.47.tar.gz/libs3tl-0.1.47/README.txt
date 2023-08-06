
### step class ###
step class consist common functions which can be inherited by other classes – setTaskID, setUUID,setTaskExecutionID,startRedisConn,setLogger,loadParams,connectToAPIForKey,createAndGetResponseFromURL,getLogger,exceptionTraceback,getRelativeFile;

### extract class###
extract class consist of init method which sets all loadParams and log files .. also contains super class startup which can be defined from client extract ..

### ML class ###
Ml class consist of init method which sets all loadParams and log file ,startMLSubscriber to subscribr to the incoming data ;

### Transform class ###
Transform class consist of init method which sets all loadParams and log file ,startTRSubscriber to subscribr to the incoming data ,

### Load Class ###
Load class consist of init method which sets all loadParams and log file, loadsubscribers to subscribe to incoming data from redis queue and client logic to load final data needs to be added in client load file;

### Connectors Added ###
AzBlob Read (Azure Blob) 
Using this connector you can read file from AzBlob; 
for Azure Blob Read connection , create sorce folder inside params and add spec.json with connection configs ;

AzBlob Write(Azure Blob)
Using this connector you can write file to AzBlob; 
for Azure Blob Write connection , create destination folder inside params and add spec.json with connection configs ;

SFTP Read 
Using this connector you can read file from SFTP server ; 
for SFTP connection , create source folder inside params and add spec.json with connection configs ;

SFTP Write 
Using this connector you can read file to SFTP server for SFTP Write connection ,
create destination folder inside params and add spec.json with connection configs ;

Postgres Read 
Source connector for PostgreSQL database using SQLAlchemy,
it consist check()-this method will check connection setup with postgress database. 
The read() method takes an optional query parameter, and executes the query on the connected database,discover(): This discover() function is used to discover the tables in the database.

Postgres Write 
Using this connector you can read file to Postgres database, consist of check(),
read() in addition it contains create_table() function is used to create a new table in the database.
It compiles the Table object provided into a SQL,alter_table(): function is used to alter a table in the database,write(): function is used to write data to the database.
It takes in the table object and a list of dictionaries

IPFS source 
you can use this connector to read file from any IPFS http url; 
this connector contains check() used to check connection ,read function which will return data in bytes format;

IPFS destination 
this connector helps you to upload any file on customIPFS node;
write function in this connector uses file and target location as input and will return json consisting contentId ,name and size of file;