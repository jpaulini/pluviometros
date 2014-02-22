#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api.urlfetch import fetch
try:
    import simplejson as json
except:
    from django.utils import simplejson as json

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(
            """<!DOCTYPE html>
            <html>
            <head>
            <meta charset="ISO-8859-1">
            <link type="text/css" href="css/style.css" rel="stylesheet" media="all" />
            <title>Pluviometros</title>
            <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false&language=es"></script>
            <script type="text/javascript" src="js/modernizr-1.7.min.js"></script>
            <script type="text/javascript">{var map=Object(); var canvas=Object();}</script>
            <script type="text/javascript" src="js/json2.js"></script>
            <script type="text/javascript" src="js/estaciones.js"></script>
            <script type="text/javascript" src="js/canvas.js"></script>
            <script type="text/javascript" src="js/map.js"></script>

            </head>
            <body>
            <input type="button" value="MapValues" id="getValues" />
            <table align="center">
                <td><div id="map" 
                    style="border-style: solid; border-width: inherit; border-color: #002D5E; width:700px; height:700px">
                </div></td>
                <td>
                <canvas id="canvas" width="700" height="700">
                Sorry. If you are seeing this message, your browser does not support Canvas Tag.
                </canvas>
                </td>
            </table>
            <footer>
            <!--Aqui va la carga de los datos al mapa  -->
            </footer>
            </body>
            </html>""")

class RGHandler(webapp.RequestHandler):
    def get(self):
        content=fetch("http://geointa.inta.gov.ar/dlluvias/estaciones.inta")
        self.response.out.write(json.dumps(json.loads(content.content)))



application = webapp.WSGIApplication([('/', MainHandler),('/srv1', RGHandler)],
                                         debug=True)
