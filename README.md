# coffee-gelee
A file uploading forum made in python.

A file upload forum made in python. It has posts, users, authentication, all you can ask for.

Except maybe a few pivotal functionalities but whatever.
It also needs fixing. If you're reading this readme, then there's some serious problems regarding the download and upload functions.
To the trained eye, you might notice a slight problem with the media folder.. (hint: it's meant to be named "media"). So 
don't upload anything to this website until that feature is done.

Here's how the permissions work:

* Users can read all but "special" posts that only higher up people can read
* Normal people can post and can only edit their own posts, but not set "special" status
* Staff obviously get access to all
* There are categories you can assign them to

You're free to study/use the code. Don't see why you would but you can.

Things to do:
* Fix the download/upload problem (it's pathing. A lot of it)
* Add tags
* Add more user permissions
* Diminish dependance on the admin interface (right now, its the only way to add/take away permissions.)
* Further separate view logic from template logic. 
* Finish the damn thing.

To use it, you need python and django. Simply write manage.py runserver (in the root folder) and visit it in 127.0.0.1:8000 (you can change the port
in settings).
