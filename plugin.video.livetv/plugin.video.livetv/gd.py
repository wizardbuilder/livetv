import xbmc, xbmcaddon, xbmcplugin, os, mknet

def _getInput(default_text='', heading='', hidden=False):
	keyb = xbmc.Keyboard(default_text, heading, hidden)
	keyb.doModal()
	if (keyb.isConfirmed()):
		result = keyb.getText()
	else:
		result = False


class gd:
	addon_id		= "plugin.video.livetv"
	selfAddon		= xbmcaddon.Addon(id=addon_id)
	user			= selfAddon.getSetting("hqusername")
	passw			= selfAddon.getSetting("hqpassword")
	datapath		= xbmc.translatePath(selfAddon.getAddonInfo("profile"))
	addonDir		= xbmc.translatePath(selfAddon.getAddonInfo("path"))

	# Make any missing dirs
	if not os.path.exists(datapath):
		os.makedirs(datapath)


	epg_file			= os.path.join(os.path.abspath(datapath), "guide.xmltv")
	channels_json		= os.path.join(datapath, "channels.json")
	
	cookie_file			= os.path.join(datapath, "iptvx9.lwp")
	net					= mknet.Net()
	BASE_URL			= "https://easyuse.tv/x9iptv"
	CAT_URL			= "https://easyuse.tv/wp-json/iptv/v1/categories"
	#BASE_URL			= 'http://192.168.1.25'		   # For testing on local
	user = selfAddon.getSetting("hqusername")
	passw = selfAddon.getSetting("hqpassword")
	auto = selfAddon.getSetting("autologin")

	bouquet = {
		'2':'Easy2Use Basic',
		'3':'Test account',
		'5':'Adult/Erotiek module',
		'7':'Sport pakket',
		'8':'Sky channel pakket',
		'9':'Film1 pakket',
		'10':'Wereld pakket',
		'11':'sport pakket voor',
		'17':'firmware upgrade X9'
	}

	try:
		clickflix_addon_exists = True
		clickflix_addon_id = 'plugin.video.vip-easy2use.tv'
		CLICKFLIX_URL = "https://app.clickflix.tv/mani/ajax/?do=check_amember"
		clickflix_enabled_bouquet = [2,3,10]
		clickflix_addon = xbmcaddon.Addon(id='plugin.video.vip-easy2use.tv')
		clickflix_addon_data = xbmc.translatePath(clickflix_addon.getAddonInfo("profile"))
		EMBY_URL  = "movies.clickflix.tv"
		EMBY_PORT = "80"
	except:
		clickflix_addon_exists = False

	@classmethod
	def get3Settings(cls):
		cls.user	= cls.selfAddon.getSetting("hqusername")
		cls.passw   = cls.selfAddon.getSetting("hqpassword")
		cls.auto	= cls.selfAddon.getSetting("autologin")
