import sublime, sublime_plugin
import urllib
import threading

class ValidateManifestCall(threading.Thread):
	def __init__(self, url, manifest, timeout):
		api_path = '/api/1/manifests/validate'

		self.url = url + api_path
		self.manifest = manifest
		self.timeout = timeout
		threading.Thread.__init__(self)

	def run(self):
		urllib.request.install_opener( urllib.request.build_opener( urllib.request.ProxyHandler()) )
		try:
			data = self.manifest
			req = urllib.request.Request(self.url, data=data, headers={'Content-Type':'application/x-yaml'})
			resp = urllib.request.urlopen(req)
			self.result = resp.read()
			print(self.result)	
			self.status = True
			return
		except urllib.error.HTTPError as e:
			print(e.read())
			err = '%s: HTTP error %s contacting API' % (__name__, str(e))	
		self.status = False

class ValidateCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		manifest = self.view.substr(sublime.Region(0, self.view.size())).encode('UTF-8')
		thread = ValidateManifestCall('http://localhost:9000',manifest, 5)
		thread.start()

def handle_threads(self, edit, threads, braces, offset=0, i=0, dir=1):  
    next_threads = []  
    for thread in threads:  
        if thread.is_alive():  
            next_threads.append(thread)  
            continue  
        if thread.result == False:  
            continue  
        offset = self.replace(edit, thread, braces, offset)  
    threads = next_threads  