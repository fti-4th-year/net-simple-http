#!/usr/bin/python

import sys
import os
import subprocess

line = sys.stdin.readline()
(method, uri, version) = line.strip().split(' ')
#print (method, uri, version)

headers = dict()
while True:
	line = sys.stdin.readline()
	if len(line) <= 2:
		break
	(key, value) = line.strip().split(':', 1)
	headers[key] = value
#print headers

def is_exec(path):
	return "executable" in subprocess.check_output(["file", "-Lb", path])

def get_mime(path):
	return subprocess.check_output(["file", "-Lib", path]).strip()

def get_content(path):
	file_handle = open(path, 'r')
	data = file_handle.read()
	file_handle.close()
	return data

path = uri
query = ''
if '?' in uri:
	(path, query) = uri.split('?', 1)
path = path.strip('/')
path_info = ''
while True:
	if os.path.isfile(path):
		print 'HTTP/1.1 200 OK'
		data = ''
		mime = ''
		if is_exec(path):
			env = os.environ
			env['QUERY_STRING'] = query
			env['PATH_INFO'] = path_info
			env['REQUES_METHOD'] = method
			proc = subprocess.Popen(['./' + path], stdout=subprocess.PIPE, env=env)
			data = proc.stdout.read()
			mime = 'text/plain; charset=utf-8'
		else:
			data = get_content(path)
			mime = get_mime(path)
		print 'Content-Type: ' + mime
		print 'Content-Length: ' + str(len(data))
		print 'Connection: close'
		print 
		print data
		break
	else:
		if '/' in path:
			plist = path.rsplit('/', 1)
			path = plist[0]
			path_info = plist[1] + '/' + path_info
			continue
		else:
			print 'HTTP/1.1 404 Not Found'
			print 
			print '404 Not Found'
		break
