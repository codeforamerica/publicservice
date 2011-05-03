from google.appengine.ext import db
from google.appengine.api import urlfetch

from geo.geomodel import GeoModel
import bobo
import chameleon.zpt.loader

from decimal import Decimal
import os
import random
import simplejson as json

# The main class for storing quotes and their associated geolocation info
class Quotes(GeoModel):
    """A location-aware class for quotes.
    """
    quote = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    city = db.StringProperty(required=True)
    state = db.StringProperty(required=True)
    rand = db.FloatProperty()
    timestamp = db.DateTimeProperty(auto_now=True)
    flag = db.BooleanProperty(default=False)
    hidden = db.BooleanProperty(default=False)
    safe = db.BooleanProperty(default=True)
    errormsg = db.StringProperty()

    def _get_latitude(self):
      return self.location.lat if self.location else None

    def _set_latitude(self, lat):
      if not self.location:
        self.location = db.GeoPt()

      self.location.lat = lat

    latitude = property(_get_latitude, _set_latitude)

    def _get_longitude(self):
      return self.location.lon if self.location else None

    def _set_longitude(self, lon):
      if not self.location:
        self.location = db.GeoPt()

      self.location.lon = lon

    longitude = property(_get_longitude, _set_longitude)

# All templates are in the 'templates' directory
template_path = os.path.join(os.path.dirname(__file__), 'templates')

# Use chameleon as the template rendering engine. When running locally, auto
# -reload the templates if they change.
template_loader = chameleon.zpt.loader.TemplateLoader(
        template_path,
        auto_reload=os.environ.get('SERVER_SOFTWARE', '').startswith('Dev'))

# The 'master' template, that contains the basic HTML structure used by other
# templates.
master = template_loader.load('master.html')


# App Engine doesn't make it easy to get a random object from the datastore,
# this is a hack around the problem borrowed from
# http://stackoverflow.com/questions/3450926/how-to-get-something-random-in-datastore-appengine
def getrandomquote():
    rand_num = random.random()
    randomquote = Quotes.all().order('rand').filter('rand >=', rand_num).get()
    if randomquote is None:
        randomquote = Quotes.all().order('-rand').filter('rand <', rand_num).get()
    if randomquote is None: return randomquote
    # extra filter (not really used yet) so we can remove quotes from rotation,
    # without actually deleting them. TODO: Need to think through the workflow.
    elif randomquote.safe is False or randomquote.hidden is True or randomquote.flag is True:
        randomquote = getrandomquote()
    else: return randomquote

# Main site URL
@bobo.query('/')
def index():
    template = template_loader.load('index.html')
    quote_url = '/'
    quote = getrandomquote()
    if quote is not None:
        quote_url = '/q/'+str(quote.key().id())
    return template(master=master, quote=quote, quote_url=quote_url)

# The individual quote page
@bobo.query('/q/:quote_id')
def quote(quote_id):
    template = template_loader.load('quote.html')
    quote = Quotes.get_by_id(int(quote_id))
    # post-hoc attempt at geocoding based on the city and state
    if quote and quote.location=='0.0,0.0':
        address = quote.city+', '+quote.state
        address = address.replace(' ', '+')
        url="http://maps.google.com/maps/api/geocode/json?address=%s&sensor=false" % address
        try:
            # some queries to Google aren't returning data, or are timing out,
            # which causes the errors we'd been seeing. Wrapping a try around
            # it insulates us from the error.
            response = urlfetch.fetch(url, deadline=10)
            jsongeocode = response.content
            geocode = json.loads(jsongeocode)
            quote.location.lat = geocode['results'][0]['geometry']['location']['lat']
            quote.location.lon = geocode['results'][0]['geometry']['location']['lng']
            quote.put()
        except: pass
    # Test if the quote exists, and if it is marked as 'safe' (the default). 
    if quote and quote.safe:
        return template(master=master, quote=quote)
    # Otherwise, redirect to the homepage.
    else:
         return bobo.redirect('/')

# An 'add' form for quotes. Superseded by the form on the front page.
@bobo.query('/addform')
def addform():
    template = template_loader.load('addform.html')
    return template(master=master)

# URL for quote submissions, Post-only 
@bobo.post('/add')
def add(quote, name, city, state, lat, lon, errormsg):
    rand = random.random()
    # Note: we're not doing any server-side validation (other than that
    # enforced by the data model), so we're a bit over-reliant on the 
    # client side validation. A user who has JS turned off and submits bad
    # data would see an unfriendly error message.
    new_quote = Quotes(quote=quote, name=name, city=city,
                       state=state, rand=rand, location=lat+','+lon,
                      errormsg=errormsg)
    new_quote.put()
    # after crrating the quote, redirect to the new quote's page. 
    return bobo.redirect('/q/'+str(new_quote.key().id()))
