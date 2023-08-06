This package is used to store files in mongodb
### filestostorage

##### Required Packages
`$ pip install pymongo`
For connecting python to mongodb
`$ pip install gridfs-fuse`
For performing read/write operations on mongodb
#### Installation
`$ pip install filestostorage`

Project is still under development  :)
Currently supported for storing files in mongodb

#### Usage




##### Import statement:
import filestostorage as ft

##### Mongo Connection
Create a Database object
db = ft.mongo_conn()

db = ft.mongo_conn("mongodb+srv://{username}:{password}@{cluster_name}.mongodb.net/test?retryWrites=true&w=majority")
##### Upload File
To upload file use the below command
ft.upload_file("FILE PATH","FILENAME",db)

ft.upload_file("/Users/Desktop/test/image1.jpeg","file_name",db)
##### Download File
To download_files use the below command:
ft.download_file("DOWNLOAD LOCATION","FILE NAME",db)

ft.download_file("/Users/Desktop/myimage.jpeg","name",db)
 In 2nd parameter use the same file name which was used while uploading the file
 
##### Overall


import filestostorage as fstr

db = fstr.mongo_conn()   #connect to database via url

fstr.upload_file("file_path","file_name",db) #command to upload file

fstr.download_file("download_location","file_name(same as upload)",db)#command to download file