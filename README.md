# Note

### There are a lot of different sites in the world. This site is unique. We have implemented very nice techniques

### Main page
When you open our site you can see 5 big buttons that represent instruments. 
By clicking on 1 of them you can see the list of songs that have chords or tabs and can be played on that instrument
On the top of our main page you can also see search-bar. If you type there song name or artist, our site will show you all songs that suit for that request.

### Filters 
We also have filters on our site. You can choose whether you want: instrument or few, type of notes.

### Create button
If you want to share chords or tabs, you can go to the top-right side of our page and click on "Add song" button.
As a result, you will be able to type song name, author and chords or tabs. After that you choose appropriate instrument and submit everything.

### About us 
About us page info about our project, developers, and our images.


@Backend info

## MongoDB
To work with our database we have installed(pip install pymongo) pymongo library.
To operate with our data we have created a mongo client.
We have two main classes that work with our database: Filter, Search

### Filter
Filter class contains get_filetered_songs method, that sort our songs by instrument and returns DateSort() method, that takes sorted collections as argument.

### DateSort
DateSort class contains sort_by_dates method, that sort our songs in ascending or descending way using PyMongo library methods ASCENDING and DESCENDING.
This method takes output of Filter.get_filtered_songs() method, and returns ilst of songs, that are sorted in proper sequence.

![image](https://user-images.githubusercontent.com/116728854/230791992-88c2518c-07c9-4893-aa39-4e8c4ea47b99.png)


### Search 
This class is used to start searching for songs by instrument and by type of notes(it can be chords, tabs or both).
If request is given, we search for songs which title or author matching the request.
If we have not found any data function returns None, else it returns list of songs, each song is a dictionary.
This class contains find() method, that finds songs by text, author or title. Uses SearchAlgorithm class.

![image](https://user-images.githubusercontent.com/116728854/230792539-edbfe4f0-8106-412c-aa38-1ae5997d7750.png)



### SearchAlgorithm
This class is used to find songs by title, author, text, that can contain mistakes using MongoDB(PyMongo), difflib, re.
Contains one_word_req, lots_word_req, find_match methods. 
Find_match method starts one_word_req() and lots_word_req() method.
Main algorithms work in the next way:
Algorithm counts number of words, that were requested, and compare these words to the same length title, author, text(for each song), or if legth differ, splits text for many parts to check each one.

![image](https://user-images.githubusercontent.com/116728854/230792309-e35caff2-cfa8-42be-88e7-1b74eb7dc484.png)
![image](https://user-images.githubusercontent.com/116728854/230792328-dbd41e5a-48f6-4f87-83e5-dc2f47e7a6cc.png)



## Flask
To work with flask we are installing next libraries (except for filters and secrets):

![image](https://user-images.githubusercontent.com/116728854/228357477-63ddc060-e59e-4dd8-986d-edf4929259ba.png)

Firstly, we are creating secret key for the Flask application.
After we implement search() function which submits chosen filters to class Search.
welcome() function simply opens main page.
about() function opens page with information about the site.
create() function is adding songs in the database. All fields(title, author, instrument) are required, except for the checkbox 'I want_tabs!'.
object_detail() function finds an object in the database and renders a song page with its details

If you want to visit our site you will have to run program app.py, and then click on the link that will pop up in the terminal.

### Project was made by Olena Azarova, Anastasiia Pelekh, David Ilnytskyy, Vitaliy Paliychuk and Sofia Shuliak. 
### We hope you like it!
