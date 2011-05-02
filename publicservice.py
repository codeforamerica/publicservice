from google.appengine.api import users
from google.appengine.ext import db
from geo.geomodel import GeoModel
import bobo
import chameleon.zpt.loader

import urllib2
import os
import random

import simplejson as json
from decimal import Decimal

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

template_path = os.path.join(os.path.dirname(__file__), 'templates')

template_loader = chameleon.zpt.loader.TemplateLoader(
        template_path,
        auto_reload=os.environ.get('SERVER_SOFTWARE', '').startswith('Dev'))
        
master = template_loader.load('master.html')

def getrandomquote():
    rand_num = random.random()
    randomquote = Quotes.all().order('rand').filter('rand >=', rand_num).get()
    if randomquote is None:
        randomquote = Quotes.all().order('-rand').filter('rand <', rand_num).get()
    if randomquote is None: return randomquote
    elif randomquote.safe is False: randomquote = getrandomquote()
    else: return randomquote


@bobo.query('/')
def index():
    template = template_loader.load('index.html')
    quote_url = '/'
    quote = getrandomquote()
    if quote is not None:
        quote_url = '/q/'+str(quote.key().id())
    return template(master=master, quote=quote, quote_url=quote_url)

@bobo.query('/q/:quote_id')
def quote(quote_id):
    template = template_loader.load('quote.html')
    quote = Quotes.get_by_id(int(quote_id))
    if quote and quote.location=='0.0,0.0':
        address = quote.city+', '+quote.state
        address = address.replace(' ', '+')
        url="http://maps.google.com/maps/api/geocode/json?address=%s&sensor=false" % address

        response = urllib2.urlopen(url)
        jsongeocode = response.read()
        geocode = json.loads(jsongeocode)
        quote.location.lat = geocode['results'][0]['geometry']['location']['lat']
        quote.location.lon = geocode['results'][0]['geometry']['location']['lng']
        quote.put()
    if quote and quote.safe:
        return template(master=master, quote=quote)
    else:
         return bobo.redirect('/')

@bobo.query('/addform')
def addform():
    template = template_loader.load('addform.html')
    return template(master=master)

@bobo.post('/add')
def add(quote, name, city, state, lat, lon):
    rand = random.random()
    new_quote = Quotes(quote=quote, name=name, city=city,
                       state=state, rand=rand, location=lat+','+lon)
    new_quote.put()
    return bobo.redirect('/q/'+str(new_quote.key().id()))
