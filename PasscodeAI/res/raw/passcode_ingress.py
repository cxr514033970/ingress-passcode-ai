#coding=utf-8
import urllib,urllib2,re,json
'''
简单实现ingress自动提交passcode,大神勿喷
小孩 QQ:9456590
'''

class Ingress:

	def __init__(self, email = None, password = None):
		self.email=email
		self.password=password


	def login(self):
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
		urllib2.install_opener(self.opener)
		# Define URLs
		self.ingress_url='http://www.ingress.com/intel'
		self.loing_page_url = 'https://accounts.google.com/ServiceLogin?service=grandcentral'
		self.authenticate_url = 'https://accounts.google.com/ServiceLoginAuth'
		self.passcode_url = 'http://www.ingress.com/rpc/dashboard.redeemReward'

		#Load longin url
		print 'Search url...'
		ingress_page_contents = self.opener.open(self.ingress_url).read()
		loing_page_url=re.findall('<a href="(.*?)" class="button_link"',ingress_page_contents,re.I)

		ltmpl_shdf=re.findall('ltmpl=(.*?)&shdf=(.*)',loing_page_url[0],re.I)
		login_page_contents = self.opener.open(loing_page_url[0]).read()

		print 'Search GALX...'
		# Find GALX value
		galx_match_obj = re.search(r'name="GALX"\s*value="([^"]+)"', login_page_contents, re.IGNORECASE)
		galx_value = galx_match_obj.group(1) if galx_match_obj.group(1) is not None else ''

		login_params = urllib.urlencode({
					'Email' : self.email,
					'Passwd' : self.password,
					'continue' : 'https://appengine.google.com/_ah/conflogin?continue=http://www.ingress.com/intel',
					'GALX' : galx_value,
					'signIn' : 'Sign in',
					'service' : 'ah',
					'shdf' : ltmpl_shdf[0][1],
					'ltmpl' : ltmpl_shdf[0][0]

				})
		#Lgoin Ingress
		print 'Login...'
		self.opener.open(self.authenticate_url, login_params)
		ingress_page_contents = self.opener.open(self.ingress_url).read()

		toekn = re.search("name='csrfmiddlewaretoken'.*?value='(.*?)'", ingress_page_contents)
		if not toekn:
			self.logged_in = False
			print 'Login failed'
		else:
			self.logged_in = True
			self.toekn = toekn.group(1)
			print 'Login Success,toekn:'+self.toekn

	def send_passcode(self,passcode):
		data_json = json.dumps({"passcode":passcode,"method":"dashboard.redeemReward"}) 
		req = urllib2.Request(self.passcode_url, data=data_json)
		req.add_header('Referer','http://www.ingress.com/intel')
		req.add_header('X-CSRFToken',self.toekn)
		req.add_header('Connection','keep-alive')
		req.add_header('X-Requested-With','XMLHttpRequest')
		response=urllib2.urlopen(req)
		the_page = response.read()
		print the_page


if "__main__" == __name__:
	Ingress_APP=Ingress('','')
	Ingress_APP.login()
	Ingress_APP.send_passcode('7vh3ultrap2s6y')

