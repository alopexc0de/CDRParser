# -*- coding: utf-8 -*-

from bottle import SimpleTemplate, static_file, response, request, route, run
import tempfile
import json
import csv
import os

config = {
	'page': 'Company name here',
	'hostport': 8080,
	'savedir': 'download'
}

__syntax = '<% %> % [[ ]]' # Replace bottle's default template key with [[]] - {{}} is used by Angular and will conflict
__indextemplate = SimpleTemplate(name='index', lookup=['views'], syntax=__syntax) # Basic configuration of template to use views/index.tpl and custom syntax above

savedir = os.path.abspath(config['savedir']) # Find absolute path to savedir
bigData = []

def parseFiles():
	print 'Parsing the CSV files to save only the columns we want:\n Connect/Disconnect Times, Call Origin, Username, Calling Number, Called Number'
	for i in os.walk(savedir, topdown=False): 
		for d in i[2]: # For each file inside the savedir
			with open(os.path.join(savedir, d), 'r') as reader: # Open the file as read-only
				read = csv.reader(reader) # Read it as a CSV file
				for r in read:
					try:
						row = { 
							"connect": r[9],
							"disconnect": r[10],
							"origin": r[13],
							"username": r[20],
							"calling": r[21],
							"called": r[22]
						}
						# Store the row in a dictionary and append that row to the bigData list
						bigData.append(row)
					except IndexError, e: # Out of range 
						# This is usually caused by log entries that only have r[0] (UNIX timestamp)
						print r
				reader.close() # Close the files when we don't need them anymore

@route('/') # Simple site, no links or other routes other than the index
def index():
	parseFiles() # Be Greedy. This reparses all of the files in savedir on every page load
	# Return the rendered template and pass bigData and page variables
    return __indextemplate.render(bigData=json.dumps(bigData), page=config['page'])


if __name__ == '__main__':
	rootdir = os.path.dirname(__file__) # Find the path to this script
	rootdir = os.path.join(rootdir, 'static') 
	@route('/static/<filename:path>') # Setup a route for static files - Files changed here don't require a server restart
	def static(filename):
		return static_file(filename, root=rootdir) # Serve the files up without having bottle touch them

	run(host='0.0.0.0', port=config['hostport'], debug=True, reloader=True) # reloader will restart the server if it detects any changes to this file