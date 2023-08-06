This package is used to store files in mongodb

Install the requirements files
Packages used :
******pymongo*******  
pip install pymongo
******gridfs******
pip install gridfs-fuse


import statement:
import filestoexplore as ft

Now add your mongourl to a variable
db = ft.mongo_conn()

To upload_files use the below command
ft.upload_file(Filepath,filename with extension,database object)

"ft.upload_file("/Users/Desktop/test/image1.jpeg","name",db)"

To download_files use the below command:
ft.download_file(downloadpath,filename with extension,database object)

"ft.download_file("/Users/Desktop/myimage.jpeg","name",db)"
 and in 2nd parameter use the same file name which was used while uploading the files