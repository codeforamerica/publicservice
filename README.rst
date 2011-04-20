==============================
Setting up the DC Foodshed App
==============================

The Public Service Recognition App uses a number of existing projects,
such as Bobo, Chameleon,Geomodel, and Buildout.

The site can currently be seen at http://public-service.appspot.com

See http://bobo.digicool.com/ for information on bobo.

See http://chameleon.repoze.org/ for information on Chameleon.

See http://code.google.com/p/geomodel/ for information on Geomodel.

See http://www.buildout.org/ for information on Buildout.


Running the application out of the box
--------------------------------------

Build and run the application::

  $ python2.5 bootstrap.py --distribute
  $ ./bin/buildout
  $ ./bin/dev_appserver parts/publicservice

Then access the application using a web browser with the following URL::

  http://localhost:8080/

To add a quote, go to http://localhost:8080/addform

After adding a quote, the user is redirected to an individual page for the
quote of the form /q/id, where 'id' is a number.

Uploading and managing
----------------------

To upload application files, run::

  $ ./bin/appcfg update parts/publicservice

For a more detailed documentation follow this url::

  http://code.google.com/appengine/docs/python/tools/uploadinganapp.html

