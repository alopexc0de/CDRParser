# -*- coding: utf-8 -*-

import tempfile
import hashlib
import ftplib
import os

m = hashlib.md5()
hashes = []

config = {
	'ftp': {
		'host': '',
		'port': 21,
		'tls': False,
		'username': '',
		'password': '',
		'path': '/'
	},
	'savedir': 'download' # Relative to this script or absolute path to download files to 
}

savedir = os.path.abspath(config['savedir']) # Find the path of the savedir
print 'cleaning {}'.format(savedir)
for files in os.walk(savedir): # Deletes all files (but not directories) from the savedir
	for f in files:
		for i in f:
			try:
				os.unlink(os.path.join(savedir, i))
			except OSError, e: # Replace with WindowsError if running from a Windows box
				print e
				pass

# Configure the FTP client if using TLS connections
if config['ftp']['tls']:
	ftp = ftplib.FTP_TLS()
else:
	ftp = ftplib.FTP()

def ftpConnect():
	print 'Connecting to the FTP Server'
	# Establish FTP connection to server
	ftp.connect(config['ftp']['host'], config['ftp']['port'])
	print ftp.getwelcome()

	print 'Logging into {} with username {}'.format(config['ftp']['host'], config['ftp']['username'])
	ftp.login(config['ftp']['username'], config['ftp']['password'])

	if config['ftp']['path']:
		print 'Changing directory to {}'.format(config['ftp']['path']) 
		ftp.cwd(config['ftp']['path'])

	print 'Getting list of files from server'
	filelst = ftp.nlst()
	return filelst

def fileDL(filelst):
	print 'Downloading files from server'
	tmpfilelst = []
	# Download all the files
	for i in filelst:
		tmpfile = tempfile.mkstemp(dir=savedir) # The file will not be deleted when this script runs because we created the file directly instead of using TemporaryFile()
		tmpfilelst.append(tmpfile)
		with open(tmpfile[1], 'wb') as tmpfile: # tmpfile is a tuple, second half contains filename. Open as binary file
			# retrlines does not add newline characters per line that it downloads and seriously screws up CSV
			print ftp.retrlines('RETR ' + i, lambda s, w = tmpfile.write: w(s+'\n')) # This lambda adds a newline to each line so it can be processed by CSV
	return tmpfilelst

def makeHash(thedir):
	# Computes the MD5 for all files in a given directory and returns a list of lists containing the hash and path to file
	tohash = []
	thehashes = {}
	for root, dirs, files in os.walk(thedir, topdown=False):
		for thefile in enumerate(files):
			tohash += [os.path.abspath('{0}/{1}'.format(thedir,thefile[1]))]

	for path in tohash:
		thehashes[hashlib.md5(open(path, 'rb').read()).hexdigest()] = path

	return thehashes


tmpfilelst = fileDL(ftpConnect())
ftphash = makeHash(savedir)

savedhash = makeHash(savedir)

# These hashes aren't used for anything right now, but could be used in the future
# to remove the need to download all the files again every time this script runs and only save
# files that have either changed or are new
print ftphash
print savedhash
