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
import cgi
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import db
import webapp2
import BeautifulSoup
from assignment4_3 import *
from google.appengine.api.datastore_errors import *
class MainHandler(webapp2.RequestHandler):
    def get(self):
		MAIN_PAGE_HTML = """\
		<!DOCTYPE html>
		<html>
		    <head>
		        <title> Query eval </title>
		        <style>
		            body {background-color:white;}
		        </style>
		        <script language="javascript">
		            <!--

		                var state = 'none';
		                function validate(form) {
							if (document.form1.col[0].checked){
								document.form1.sell.value = "all";
								return true;
							}
							var total="";
							for(var i=0; i < document.form1.col.length; i++){
								if(document.form1.col[i].checked)
									total +=document.form1.col[i].value + " ";
							}
							if( total === "" ){
								document.form1.sell.value = "NONE";
								return false;
							}
							else{
								document.form1.sell.value = total;
								return true;
							}
						}
		                function showhide(layer_ref) {

		                    if (state == 'block') {
		                        state = 'none';
		                    }
		                    else {
		                        state = 'block';
		                    }
		                    if (document.all) { //IS IE 4 or 5 (or 6 beta)
		                        eval( "document.all." + layer_ref + ".style.display = state");
		                    }
		                    if (document.layers) { //IS NETSCAPE 4 or below
		                        document.layers[layer_ref].display = state;
		                    }
		                    if (document.getElementById &&!document.all) {
		                        hza = document.getElementById(layer_ref);
		                        hza.style.display = state;
		                    }
		                }
		            //-->
		        </script> 
		    </head>
		    <body>
		        <form name="form1" method="post" action="/GetDetails" onsubmit="return validate(this)">
		            <h1><p style="font-family:Helvetica;background-color:grey;text-align:center;"><u>DEVICE DATABASE</u></p> </h1>
		            <br/>
		            <div align = "center" style="font-family:verdana;;background-color:grey;">
						<h3><span onclick="showhide('col');">Colums</span></h3>
						<div id="col" style="display: none;">
                        <table border = 1>
                        <tr><td>model</td><td colspan=2>isTouchEnabled</td></tr>
                        <tr><td>displayDensity</td><td colspan=2>isMultiTouchEnabled</td></tr>
                        <tr><td>displaySize</td><td colspan=2>operatingSystem</td></tr>
                        <tr><td>is3GEnabled</td><td colspan=2>secondaryCamera</td></tr>
                        <tr><td>height</td><td>width</td><td>length</td></tr>
                        </table>
                        </div>
						<h3><span>Query here</span></h3>
		                <div id="que">
		                    <input type = "text" name = "query" value = "" size = "50"/><!--<input type = "text" name = 'query1'>-->
		                <input type = "submit" name = "mine" value = "submit"/>
		                </div>
		                </form>
		                <h3><span onclick="showhide('exmp');">Example Queries</span></h3>
		                <div id="exmp" style="display: none;">
		                <ul>
		                <li>select * from Phone</li>
		                <li>select * from Phone where width > 60.0</li>
		                <li>select * from Phone where is3GEnabled = True And displaySize = 5.0</li>
		                </ul>
		                </div>
		<!--                 <input type = "submit" name = "mine" value = "submit"/> -->
		<!--             </form> -->
		            </div>
		        
		        <footer>
		        <hr/>
				<img style = "position:relative;top:50%; left:45%;"src="https://developers.google.com/appengine/images/appengine-noborder-120x30.gif"alt="Powered by Google App Engine" />
		        </footer>
		  </body>
		</html>

		"""
		self.response.write(MAIN_PAGE_HTML)
class SetDetails(webapp2.RequestHandler):
	def get(self):
		try:
			k = 0
			self.response.write("<html><body onload a()><center><h1>Completed crawling</h1>")
			f = open("very_long_list.txt","r")
			FOOTER = """		</center><footer>
			        			<img style = "position:relative;top:50%; left:45%;"src="https://developers.google.com/appengine/images/appengine-noborder-120x30.gif"alt="Powered by Google App Engine" />
								</footer></body></html>
			"""
			self.response.write("<table>")

			for i in f.readlines():
				'''k = k+1
				if k <= 647:
					continue'''
				p = PhoneDetails(i)
				p.findAll()
				self.writeToDatastore(p)
				self.response.write("<tr><td>"+str(i)+"</td></tr>")
			self.response.write("</table>")
			f.close()
			self.response.write("</center></html></body>")
		except URLError as e:
			self.response.write("<b>Unable to establish network connection:</b> "+str(e))
			self.response.write(FOOTER)
			
	def writeToDatastore(self, phone):
		print phone.model
		p = Phone(model = phone.model)
		p.SetValues(phone)
		p.put()

#Google datastore entity that represents a phone
class Phone(db.Model):
	model = db.StringProperty(required = True)
	isTouchEnabled = db.BooleanProperty(indexed = True)
    	displayDensity = db.FloatProperty()
    	isMultiTouchEnabled = db.BooleanProperty(indexed = True)
    	displaySize = db.FloatProperty()
    	secondaryCamera = db.BooleanProperty(indexed = True)
    	operatingSystem = db.StringProperty()
    	is3GEnabled = db.BooleanProperty(indexed = True)
    	height = db.FloatProperty()
    	width = db.FloatProperty()
    	length = db.FloatProperty()
	def SetValues(self, phone):
	    self.model = phone.model
	    self.isTouchEnabled = phone.isTouchEnabled
	    self.displayDensity = float(phone.displayDensity)
	    self.isMultiTouchEnabled = phone.isMultiTouchEnabled
	    self.displaySize = float(phone.displaySize)
	    self.operatingSystem = phone.operatingSystem
	    self.is3GEnabled = phone.is3GEnabled
	    self.secondaryCamera = phone.secondaryCamera
	    self.height = float(phone.height)
	    self.width = float(phone.width)
	    self.length = float(phone.length)
class Guestbook(webapp2.RequestHandler):
    def post(self):
        self.response.write('<html><body>You wrote:<pre>')
        self.response.write(cgi.escape(self.request.get('query')))
        self.response.write('</pre></body></html>')

class index(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><head><title>Index Page</title></head><body>')
        self.response.write('<h1>SELECT AN OPERATION</h1>')
        self.response.write('<ul><li><a href = "/crawler">Crawl Data</a></li>')
        self.response.write('<li><a href = "/index">Query Eval Engine</a></li></ul>')
        self.response.write('</html></body>')
class GetDetails(webapp2.RequestHandler):
	def post(self):
		try:
			sellect = cgi.escape(self.request.get('sell'))
			query = self.request.get('query')
			#query1 = cgi.escape(self.request.get('query1'))
			CURRENT_PAGE = """<!DOCTYPE html>
							<html>
							    <head>
							        <title> Result Page</title>
							        <style>
							            table{
							                border-collapse:collapse;
							            }
							            th{
							                background:grey;
							                padding:15px;
							            }
							            tr:nth-child(even) {background: white}
							            tr:nth-child(odd) {background: grey}
							            td{
							                text-align:center;
							                padding:15px;
							            }
							            body {
							                background-color:white;
							            }
							        </style>
							    </head>
							<body><center>
							    <h1>
							        <p style=\"font-family:verdana;background-color:grey;text-align:center;\">
							            <u>DEVICE DATABASE</u>
							        </p>
							    </h1>
			"""
			FOOTER = """		</center><footer>
			        			<img style = "position:relative;top:50%; left:45%;"src="https://developers.google.com/appengine/images/appengine-noborder-120x30.gif"alt="Powered by Google App Engine" />
								</footer></body></html>
			"""
			self.response.write(CURRENT_PAGE)
			self.response.write("<pre >Query: "+query+"</pre>")
			self.response.write("<table>")
			'''if query1:
				q = db.GqlQuery(query,query1)
			else:'''
			q = db.GqlQuery(query)
			aaaa=0
			self.response.write("<tr><th>SlNo</th><th>Model</th><th>displayDensity</th><th>isMultiTouchEnabled</th><th>displaySize</th><th>operatingSystem</th><th>is3GEnabled</th><th>secondaryCamera</th><th>height</th><th>width</th><th>length</th></tr>")
			for p in q.run():
				aaaa=aaaa+1
				self.response.write("<tr><td>"+str(aaaa)+".</td><td>"+str(p.model)+"</td><td>"+str(p.displayDensity)+"</td><td>"+str(p.isMultiTouchEnabled)+"</td><td>"+str(p.displaySize)+"</td><td>"+str(p.operatingSystem)+"</td><td>"+str(p.is3GEnabled)+"</td><td>"+str(p.secondaryCamera)+"</td><td>"+str(p.height)+"</td><td>"+str(p.width)+"</td><td>"+str(p.length)+"</td></tr>")
			self.response.write("</table>")
			self.response.write(FOOTER)
		except URLError as e:
			self.response.write("<b>Unable to establish network connection:</b> "+str(e))
			self.response.write(FOOTER)
		except BadQueryError as e:
			self.response.write("<b>Bad query:</b> "+str(e))
			self.response.write(FOOTER)


app = webapp2.WSGIApplication([('/',index),('/index', MainHandler),('/crawler',SetDetails),('/GetDetails',GetDetails)], debug=True)
'''
		except Exception as e:
			self.response.write("<b>Unknown Error:</b> "+str(e))
			self.response.write(FOOTER)'''