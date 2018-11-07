

import urllib, urllib2, re, cookielib, string, os, sys, time, json, base64, xbmc, xbmcplugin
import datetime, time, xbmcaddon, xbmcgui
import mknet, plugintools

import signin
from gd import gd

selfIcon        = xbmc.translatePath(gd.selfAddon.getAddonInfo("icon"))
fanart          = xbmc.translatePath(os.path.join("special://home/addons/" + gd.addon_id , "fanart.jpg"))
icon            = xbmc.translatePath(os.path.join("special://home/addons/" + gd.addon_id, "icon.png"))
art 		    = xbmc.translatePath(os.path.join("special://home/addons/" + gd.addon_id + "/resources/art/"))

cache_json      = os.path.join(gd.datapath, "cache.json")
vidcont = gd.selfAddon.getSetting("output_format")

def getinfo(url):
    response = gd.net.http_GET(url)
    return json.loads(response.content)

def process_category(category_name, categories=None, counting=False):
    #if not categories:
    #    categories = {"All":{"count":1}}
    categories.update(make_cat_dicts(category_name, categories))
    return categories

def search_category_dictionary_for_full_id(cat_dict, full_id, counting=False):
    found = False
    for key, value in cat_dict.iteritems():
        if "full_id" in value:
            if value["full_id"] == full_id:
                if counting:
                    value["count"] += 1
                found = True
                break
        if "subcategories" in value and value["subcategories"]:
            sub_search = search_category_dictionary_for_full_id(value["subcategories"], full_id, counting)
            if sub_search:
                value["subcategories"].update(sub_search)
                if counting:
                    value["count"] += 1
            if sub_search:
                found = True
                break
    if not found:
        cat_dict = False
    return cat_dict

def get_sub_categories(cat_dict, full_id):
    found = False
    for key, value in cat_dict.iteritems():
        if "full_id" in value:
            if value["full_id"] == full_id:
                found = value
                break
        if "subcategories" in value and value["subcategories"]:
            sub_search = get_sub_categories(value["subcategories"], full_id)
            if sub_search:
                found = sub_search
                break
    return found

def clean_category_name_to_list(category_name):
    # Strip any whitespace from categories
    return_list = []
    cats = category_name.split(",")
    for cat in cats:
        return_list.append(cat.rstrip().strip())
    return return_list

def make_cat_dicts(category_name, categories=None):
    if not categories:
        categories = {}
    cats = reversed(clean_category_name_to_list(category_name))
    for cat in cats:
        full_cat = cat
        sub_cats = cat.split("->")
        sub_cats_dicts = {}
        master_cat_name = sub_cats[0].rstrip().strip()
        if not master_cat_name in categories:
            categories[master_cat_name] = sub_cats_dicts
        sub_cats_rev = sub_cats[::-1]
        for x, item  in enumerate(sub_cats_rev):
            cat_name = item.rstrip().strip()
            y=x
            full_id = cat_name
            while True:
                if y == len(sub_cats)-1:
                    break 
                y+=1
                full_id = sub_cats_rev[y].rstrip().strip()+ " -> " + full_id
            if x == len(sub_cats)-1:
                sub_cats_dicts = {"count":0, "full_id":full_id, "subcategories":sub_cats_dicts}
            else:
                sub_cats_dicts = {cat_name:{"count":0, "full_id":full_id, "subcategories":sub_cats_dicts}}
        if categories[master_cat_name]:
            x = sub_cats_dicts["subcategories"]
            categories[master_cat_name]["subcategories"].update(x)
        else:
            categories[master_cat_name] = sub_cats_dicts
    return categories

def populate(url, category, use_cache=False, extra=None):
    print '-------------------populate-------------------'
    print 'url:'+url
    print 'category:'+category
    content = {}
    if use_cache:
        if os.path.exists(cache_json):
            try:
                with open(cache_json, 'r') as infile:
                    content = json.load(infile)
                    if url in content:
                        info = content[url]
                    else:
                        use_cache = False        
            except:
                use_cache = False
        else:
            use_cache = False
    if not use_cache:
        info = getinfo(url)
        content[url] = info
        with open(cache_json, 'w') as outfile:
            json.dump(content, outfile)
    if info["user_info"]['auth'] == 1:
        username = info["user_info"]["username"]
        password = info["user_info"]["password"]
        cat_list = []
        categories = {}
        for key, value in info["categories"].iteritems():
            for x in value:
                category_name = x["category_name"] # "Dutch, Sport"
                categories = process_category(category_name, categories=categories)
        channels = []
        for x in info["available_channels"]:
            channels.append(info["available_channels"][x])
        channels = sorted(channels, key=lambda k: k['num'])
        for chan in channels:
            category_name = chan["category_name"]
            if category_name:
                res = search_category_dictionary_for_full_id(categories, category_name, counting=True) # Search through dicts and add counters for every channel with this category
                if res: # Incase result was 'None'
                    categories = res
        if category == "main":
            # Display categories
            for key, value in categories.iteritems():
                full_id = key
                if not full_id == "All":
                    full_id = value["full_id"]
                if value["count"] > 0:
                    title  = key
                    thumb  = ""
                    fanart = ""
                    item   = {
                        "url":urllib.quote_plus(url),
                        "category":full_id
                    }
                    action = "category."+base64.urlsafe_b64encode(json.dumps(item))
                    plugintools.add_item( action=action , title=title , thumbnail=thumb , fanart=fanart , isPlayable=False, folder=True )
            if extra:
                if len(extra) > 0:
                    for cat, value in extra.iteritems():
                        action = value['action']+'.'+base64.urlsafe_b64encode(url.replace('panel_api.php', 'xmltv.php'))
                        print 'url:'+url
                        print 'epgurl:'+action
                        plugintools.add_item( action=action, title=value['title'] )
            plugintools.close_item_list()
            return
        channels_ini = open(os.path.join(gd.datapath, "addons.ini"), "w")
        channels_ini.write("[plugin.video.livetv]\n")
        available_channels = []
        epg_json = []
        channel_json = {}
        print 'channels:'+json.dumps(channels)
        for channel in channels:
            if channel['category_name'] != category:
                continue
            title = channel["name"]
            plot = channel["name"]
            if not "http" in info["server_info"]["url"]:
                url = "http://"+info["server_info"]["url"]+":"+info["server_info"]["port"]+"/live/"+username+"/"+password+"/"+channel["stream_id"]+vidcont
            else:
                url = info["server_info"]["url"]+":"+info["server_info"]["port"]+"/live/"+username+"/"+password+"/"+channel["stream_id"]+vidcont
            thumbnail = channel["stream_icon"]
            fanart = ''
            plugintools.add_item( action="play" , title=title , plot=plot , url=url ,thumbnail=thumbnail , fanart=fanart , isPlayable=True, folder=False )
            chan_title = title.split(': ')
            if len(chan_title) > 1:
                chan_title = chan_title[1]
            else:
                chan_title = chan_title[0]
            if category != 'Uitbreiden?':
                channels_ini.write("%s=plugin://plugin.video.livetv/?name=%s&mode=play\n" % (chan_title, urllib.quote_plus( title )))
                available_channels.append(chan_title)
                channel_json['id'] = channel["stream_id"]
                channel_json['name'] = channel["name"]
                channel_json['streamUrl'] = url
                channel_json['logo'] = channel["stream_icon"]
                epg_url = "http://"+info["server_info"]["url"]+":"+info["server_info"]["port"]+"/player_api.php?"+"username="+username+"&password="+password+"&action=get_short_epg&stream_id="+channel["stream_id"]#+"&limit=20"
                print "epgurl:"+epg_url
                u = urllib2.urlopen(epg_url, timeout=3000)
                xml = u.read()
                u.close()
                context = json.loads(xml)
                channel_json['epg_listings'] = context['epg_listings']
                print channel_json
                epg_json.append(channel_json.copy())
                print 'epg_json:'
                print epg_json
        channels_ini.close()
        plugintools.close_item_list()
        with open(os.path.join(gd.datapath, "epg.json"), 'w') as outfile:
            json.dump(epg_json, outfile)
            outfile.close()
        if category != 'Uitbreiden?':
            xbmc.executebuiltin('XBMC.RunScript(script.tvguide)')
            sys.exit()

def getExtraCategories():
	url = gd.BASE_URL+"/iptv-api3.php"
	post_data = {}
	post_data["extra"]   = ''
	post_data["username"] = gd.selfAddon.getSetting("hqusername")
	post_data["password"] = gd.selfAddon.getSetting("hqpassword")
	response = gd.net.http_POST(url,post_data)
	print "Returned response from server:"+response.content
	try:
		return json.loads(response.content)
	except:
		return {"response": "errors", "errors": []}

def main_list(params):
    url = None
    extra_cat = None
    if gd.user == '' or gd.passw == '':
        SignDialog = signin.SignInDialog()
        SignDialog.doModal()
        if SignDialog.playlisturl:
            url = SignDialog.playlisturl
    elif not (gd.user == '' or gd.passw == '') and not gd.auto.lower() == "true":
        SignDialog = signin.SignInDialog()
        SignDialog.doModal()
        if SignDialog.playlisturl:
            url = SignDialog.playlisturl
            extra_cat = SignDialog.extra_cat
    else:
        data = []
        data_dict = {}
        data_dict["username"] = gd.user
        data_dict["password"] = gd.passw
        data.append(data_dict)
        response = signin.send2remote(mode="signin", data=data)
        if not response["response"] == "success":
            SignDialog = signin.SignInDialog()
            SignDialog.doModal()
            if SignDialog.playlisturl:
                url = SignDialog.playlisturl
                extra_cat = SignDialog.extra_cat
        else:
            if int(response["exp_date"]) is not 0:
                now = time.time()
                if int(response["exp_date"]) > now:
                    tdelta = datetime.datetime.fromtimestamp(int(response["exp_date"]))-datetime.datetime.fromtimestamp(now)
                    #if tdelta.days <= 7:
                    #    text = 'Your license is left [COLOR red][B]'+str(tdelta.days)+'[/B][/COLOR] days. Purchase your valid license.'
                    #    choice = xbmcgui.Dialog().yesno('License warnning', text, nolabel='No, yet',yeslabel='Yes, go to login.')
                    #    if choice is 1:
                    #        SignDialog = signin.SignInDialog()
                    #        SignDialog.doModal()
                    #        if SignDialog.playlisturl:
                    #            url = SignDialog.playlisturl
                else:
                    license = signin.LicenseDialog(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8018), xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8019), xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8021))
                    license.doModal()
                    choice = license.status#choice = xbmcgui.Dialog().yesno(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8017), xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8018), nolabel=xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8021),yeslabel=xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8019))

                    #text = '[COLOR red][B]Your license already expired[/B][/COLOR]. Would you like to purchase your valid license? Otherwise you have to shutdown.'
                    #choice = xbmcgui.Dialog().yesno('License warnning', text, nolabel='No, shutdown',yeslabel='Yes, go to login.')
                    if choice is 1:
                        SignDialog = signin.SignInDialog()
                        SignDialog.doModal()
                        if SignDialog.playlisturl:
                            url = SignDialog.playlisturl
                            extra_cat = SignDialog.extra_cat
                    else:
                        xbmc.executebuiltin('XBMC.shutdown()')
            url = response["url"]
            extra_cat = response["extra"]
    if url:
        populate(url, 'main', extra_cat)

def run():
    plugintools.log("IPTV Client")
    params = plugintools.get_params()
    if params.get("action") is None:
        main_list(params)
    elif params.get("action") == "play":
        plugintools.play_resolved_url( params.get("url") )
    elif params.get("action").split(".")[0] == "category":
        cat_dict = params.get("action").split("category.")[1].rstrip().strip()
        details  = json.loads(base64.urlsafe_b64decode(cat_dict))
        url = urllib.unquote_plus(details["url"])
        category = details["category"]
        print 'category:'+category
        populate(url, category, True)
    else:
        pass
    plugintools.close_item_list()


################### RUN ###################

run()
