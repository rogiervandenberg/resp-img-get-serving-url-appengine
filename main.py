#!/usr/bin/python
#
#
# Copyright 2014 Justin Ribeiro. All Rights Reserved.
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

"""Do One Thing: Bring me a serving url for resp pictures"""

__author__ = 'justin@justinribeiro.com (Justin Ribeiro) / github@rogiervandenberg.nl (Rogier van den Berg)'

import json
import random
import string
import ConfigParser
import logging

from flask import Flask
from flask import request

from google.appengine.ext import blobstore
from google.appengine.api import images

resppicturehereicome = Flask('resp-picture-here-i-come')
resppicturehereicome.secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits)
                                for x in xrange(32))

@resppicturehereicome.route('/serveurl', methods=['POST'])
def serveurl():

	config = ConfigParser.RawConfigParser(allow_no_value=True)
	config.read('config.ini')
	
	try:
		if config.get("auth", "key") == request.form['key']:
			image = request.form['image']
			bucket = request.form['bucket']

			logging.info('Create Serving URL for ' + image)

			filename = (bucket + "/" +image)
			gskey = blobstore.create_gs_key("/gs/" + filename)
			servingImage = images.get_serving_url(gskey)
			return(servingImage)
		else:
			return json.dumps({'error': 'No valid key provided'}), 401, {'ContentType':'application/json'}
	except:
		return json.dumps({'error': 'Not all necessary input provided'}), 500, {'ContentType':'application/json'}

	
		
	

	
