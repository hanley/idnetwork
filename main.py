import StringIO
import json
import logging
import random
import urllib
import urllib2
import math

# for sending images
from PIL import Image
import multipart

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2

TOKEN = 'xxxx'

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'


# ================================

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)


# ================================

def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()

def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False

# ================================

class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))


class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        update_id = body['update_id']
        message = body['message']
        message_id = message.get('message_id')
        date = message.get('date')
        text = message.get('text')
        fr = message.get('from')
        chat = message['chat']
        chat_id = chat['id']

        if not text:
            logging.info('no text')
            return

        def reply(msg=None, img=None):
            if msg:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'text': msg.encode('utf-8'),
                    'disable_web_page_preview': 'true',
                    'reply_to_message_id': str(message_id),
                })).read()
            elif img:
                resp = multipart.post_multipart(BASE_URL + 'sendPhoto', [
                    ('chat_id', str(chat_id)),
                    ('reply_to_message_id', str(message_id)),
                ], [
                    ('photo', 'image.jpg', img),
                ])
            else:
                logging.error('no msg or img specified')
                resp = None

            logging.info('send response:')
            logging.info(resp)
        tmptext = text.lower()
        if text.startswith('/'):
            if text == '/start':
                reply('Bot enabled')
                setEnabled(chat_id, True)
            elif text == '/help':
                reply('Type to find out ip info => ip XX.XX.XX.XX/XX')
            elif text == '/stop':
                reply('Bot disabled')
                setEnabled(chat_id, False)
            elif text == '/image':
                img = Image.new('RGB', (512, 512))
                base = random.randint(0, 16777216)
                pixels = [base+i*j for i in range(512) for j in range(512)]  # generate sample image
                img.putdata(pixels)
                output = StringIO.StringIO()
                img.save(output, 'JPEG')
                reply(img=output.getvalue())
            elif tmptext.startswith('/dns',0,4):
                dns = tmptext.split(" ")
                try:
                    resource_url = 'http://api.statdns.com/'+dns[1]+'/a'
                    resp1 = json.loads(urllib2.urlopen(resource_url).read())
                    reply(resp1['answer'][1]['rdata'])
                except urllib2.HTTPError, err:
                    logging.error(err)
                    back = str(err)
            else:
                reply('What command?')

        # CUSTOMIZE FROM HERE

        elif 'who are you' in text.lower():
            reply('idnetwork kit, created by hanleyloo')
        elif 'what time' in text.lower():
            reply('look at the top-right corner of your screen!')
        elif tmptext.startswith('ip',0,2):
            sm = text.split("/")
            if len(sm)== 2:
                    if int(sm[1]) < 31:
                        ip = sm[0].split(" ")
                        if len(ip) == 2:
                            ip = ip[1].split(".")
                            if len(ip) == 4:
								snm_1 = 0
								snm_2 = 0
								snm_3 = 0
								snm_4 = 0
								tmpvar = int(sm[1])
								if tmpvar >= 8:
									snm_1 = 255
									tmpvar-=8
								else:
									if tmpvar >= 8:
										snm_1 = 255 
									bitpat=0xff00 
									while tmpvar > 0:
										bitpat=bitpat >> 1
										tmpvar = tmpvar - 1
									snm_1 = bitpat & 0xff
								if tmpvar >= 8:
									snm_2 = 255
									tmpvar-=8
								else:
									if tmpvar >= 8:
										snm_2 = 255 
									bitpat=0xff00 
									while tmpvar > 0:
										bitpat=bitpat >> 1
										tmpvar = tmpvar - 1
									snm_2 = bitpat & 0xff
								if tmpvar >= 8:
									snm_3 = 255
									tmpvar-=8
								else:
									if tmpvar >= 8:
										snm_3 = 255 
									bitpat=0xff00 
									while tmpvar > 0:
										bitpat=bitpat >> 1
										tmpvar = tmpvar - 1
									snm_3 = bitpat & 0xff
								if tmpvar >= 8:
									snm_4 = 255
									tmpvar-=8
								else:
									if tmpvar >= 8:
										snm_4 = 255 
									bitpat=0xff00 
									while tmpvar > 0:
										bitpat=bitpat >> 1
										tmpvar = tmpvar - 1
									snm_4 = bitpat & 0xff
								tmpvar = int(sm[1])
								numofaddr = math.pow(2,32 - tmpvar) - 2
								tmpvar = int(ip[0])
								tmpsnm = ~snm_1
								bcast_1 = int(tmpvar | (tmpsnm & 0xff))          
								tmpvar = int(ip[1])
								tmpsnm = ~snm_2
								bcast_2 = int(tmpvar | (tmpsnm & 0xff))          
								tmpvar = int(ip[2])
								tmpsnm = ~snm_3
								bcast_3 = int(tmpvar | (tmpsnm & 0xff))          
								tmpvar = int(ip[3])
								tmpsnm = ~snm_4
								bcast_4 = int(tmpvar | (tmpsnm & 0xff))   
								tmpvar = int(ip[0])
								nwadr_1 = tmpvar & snm_1
								tmpvar = int(ip[1])
								nwadr_2 = tmpvar & snm_2
								tmpvar = int(ip[2])
								nwadr_3 = tmpvar & snm_3
								tmpvar = int(ip[3])
								nwadr_4 = tmpvar & snm_4
								firstadr_1 = nwadr_1
								firstadr_2 = nwadr_2
								firstadr_3 = nwadr_3
								firstadr_4 = int(nwadr_4) + 1
								lastadr_1 = bcast_1
								lastadr_2 = bcast_2
								lastadr_3 = bcast_3
								lastadr_4 = int(bcast_4) - 1
								tmpip1 = "{0:08b}".format(int(ip[0]))
								tmpip2 = "{0:08b}".format(int(ip[1]))
								tmpip3 = "{0:08b}".format(int(ip[2]))
								tmpip4 = "{0:08b}".format(int(ip[3]))
								#str(bin(int(ip[0])))[2:]
								tmp = 'IP:'+ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+ip[3]+'\n'+'SM:'+str(snm_1)+'.'+str(snm_2)+'.'+str(snm_3)+'.'+str(snm_4)+'\n'+'Usable hosts:(2 to the power of (32 bits - '+str(int(sm[1]))+'='+str(32-int(sm[1]))+')) - 2 ='+str(int(numofaddr))+'\n'+'Total address:'+str(int(numofaddr)+2)+'\n'+' IP :'+str(tmpip1)+'.'+str(tmpip2)+'.'+str(tmpip3)+'.'+str(tmpip4)+'\n'+'SM :'+str(bin(snm_1))[2:]+'.'+str(bin(snm_2))[2:]+'.'+str(bin(snm_3))[2:]+'.'+str(bin(snm_4))[2:]+'\n'+'NW:'+str("{0:08b}".format(nwadr_1))+'.'+str("{0:08b}".format(nwadr_2))+'.'+str("{0:08b}".format(nwadr_3))+'.'+str("{0:08b}".format(nwadr_4))+'\n'+'BR :'+str("{0:08b}".format(bcast_1))+'.'+str("{0:08b}".format(bcast_2))+'.'+str("{0:08b}".format(bcast_3))+'.'+str("{0:08b}".format(bcast_4))+'\n'+'network:'+str(nwadr_1)+'.'+str(nwadr_2)+'.'+str(nwadr_3)+'.'+str(nwadr_4)+'\n'+'broadcast:'+str(bcast_1)+'.'+str(bcast_2)+'.'+str(bcast_3)+'.'+str(bcast_4)+'\n'+'1st:'+str(firstadr_1)+'.'+str(firstadr_2)+'.'+str(firstadr_3)+'.'+str(firstadr_4)+' Last:'+str(lastadr_1)+'.'+str(lastadr_2)+'.'+str(lastadr_3)+'.'+str(lastadr_4)+'\n'+'Wildcard Mask :'+str(~snm_1 & 0xff)+'.'+str(~snm_2 & 0xff)+'.'+str(~snm_3 & 0xff)+'.'+str(~snm_4 & 0xff)
                            else:
								tmp = 'Type to find out ip info => ip XX.XX.XX.XX/XX'
                        else:
							tmp = 'Type to find out ip info => ip XX.XX.XX.XX/XX'
                    elif int(sm[1]) == 31:
						tmp = sm[0]+'\n'+'SM:255.255.255.254'+'\n'+'Usable hosts:(2 to the power of (32 bits - 31)) - 2 = 0'+'\n'+'Num of address:Nil'
                    elif int(sm[1]) == 32:
						tmp = sm[0]+'\n'+'SM:255.255.255.255'+'\n'+'Usable hosts:(2 to the power of (32 bits - 32)) - 2 = NA'+'\n'+'Num of address:NA'
            else:
                tmp = 'Type to find out ip info => ip XX.XX.XX.XX/XX'
            reply(tmp)
        else:
            if getEnabled(chat_id):
                try:
                    resp1 = json.load(urllib2.urlopen('http://www.simsimi.com/requestChat?lc=en&ft=1.0&req=' + urllib.quote_plus(text.encode('utf-8'))))
                    back = resp1.get('res').get('msg')
                except urllib2.HTTPError, err:
                    logging.error(err)
                    back = str(err)
                if not back:
                    reply('okay...')
                elif 'I HAVE NO RESPONSE' in back:
                    reply('you said something with no meaning')
                else:
                    reply(back)
            else:
                logging.info('not enabled for chat_id {}'.format(chat_id))


app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
