=================================
Setting up the Public Service App
=================================

The Public Service Recognition App uses a number of existing projects,
such as Bobo, Chameleon, and Geomodel.

The site can currently be seen at http://public-service.appspot.com

See http://bobo.digicool.com/ for information on bobo.

See http://chameleon.repoze.org/ for information on Chameleon.

See http://code.google.com/p/geomodel/ for information on Geomodel.


Running the application out of the box
--------------------------------------

Build and run the application::

  $ google_appengine/dev_appserver publicservice

Then access the application using a web browser with the following URL::

  http://localhost:8080/

To add a quote, go to http://localhost:8080/addform

After adding a quote, the user is redirected to an individual page for the
quote at a URL of the form /q/id, where 'id' is a number.

Uploading and managing
----------------------

To upload application files, run::

  $ google_appengine/appcfg update publicservice

For a more detailed documentation follow this url::

  http://code.google.com/appengine/docs/python/tools/uploadinganapp.html

