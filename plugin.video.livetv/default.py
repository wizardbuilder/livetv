
bypass_url = False
#bypass_url = 'http://82.197.194.46:8000/panel_api.php?username=ThP6KSNMeK&password=hzAlDAJc0N'

import urllib,urllib2,re,cookielib,string,os,sys,time,json,base64, xbmc
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

def populate_and_play(url, name):
    info = getinfo(url)
    #print info
    if info["user_info"]['auth'] == 1:
        username = info["user_info"]["username"]
        password = info["user_info"]["password"]
        channels = []
        #dict = {23:{'num':7}, 43:{'num':3}, 2:{'num':9}}
        for x in info["available_channels"]:
            channels.append(info["available_channels"][x])
        channels = sorted(channels, key=lambda k: k['num'])
        channels_ini = open(os.path.join(gd.datapath, "addons.ini"), "w")
        channels_ini.write("[plugin.video.livetv]\n")
        available_channels = []
        for chan in channels:
            title = chan["name"]
            if title == name:
                plot      = chan["name"]
                if not "http" in info["server_info"]["url"]:
                    url   = "http://"+info["server_info"]["url"]+":"+info["server_info"]["port"]+"/live/"+username+"/"+password+"/"+chan["stream_id"]+vidcont
                else: url = info["server_info"]["url"]+":"+info["server_info"]["port"]+"/live/"+username+"/"+password+"/"+chan["stream_id"]+vidcont
                thumbnail = chan["stream_icon"]
                fanart    = ''
                itemurl = '%s?action=%s&title=%s&url=%s&thumbnail=%s&plot=%s' % ( sys.argv[ 0 ] , "play" , urllib.quote_plus( title ) , urllib.quote_plus(url) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ))
                plugintools.play_resolved_url( itemurl )
            chan_title = title.split(': ')
            if len(chan_title) > 1: chan_title = chan_title[1]
            else: chan_title = chan_title[0]
            if not '----' in chan_title:
                channels_ini.write("%s=plugin://plugin.video.iptv/?name=%s&mode=play\n" % (chan_title, urllib.quote_plus( title )))
                available_channels.append(chan_title)
        with open(channels_json, 'w') as outfile:
            json.dump(available_channels, outfile)
        channels_ini.close()

def process_category(category_name, categories=None, counting=False):
    if not categories:
        categories = {"All":{"count":1}}
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

def populate(url, use_cache=False, category="main"):
    if bypass_url: url = bypass_url
    if use_cache:
        if os.path.exists(cache_json):
            try:
                with open(cache_json, 'r') as infile:
                    info = json.load(infile)
            except:
                use_cache = False
        else:
            use_cache = False
    if not use_cache:
        info = getinfo(url)
    if info["user_info"]['auth'] == 1:
        with open(cache_json, 'w') as outfile:
            json.dump(info, outfile)
        username   = info["user_info"]["username"]
        password   = info["user_info"]["password"]
        channels   = []
        categories = {"All":{"count":1}}
        cat_list   = []
        for key, value in info["categories"].iteritems():
            for x in value:
                #{"category_id": "1","category_name": "Dutch, Sport","parent_id": 0}
                category_name = x["category_name"] # "Dutch, Sport"
                categories = process_category(category_name, categories=categories)
        #dict = {23:{'num':7}, 43:{'num':3}, 2:{'num':9}}
        for x in info["available_channels"]:
            channels.append(info["available_channels"][x])
        channels = sorted(channels, key=lambda k: k['num'])
        ################ Display items: ################
        if category == "All":
            channels_ini = open(os.path.join(gd.datapath, "addons.ini"), "w")
            channels_ini.write("[plugin.video.livetv]\n")
            available_channels = []
        # Sort categories
        for chan in channels:
            category_name = chan["category_name"]
            if category_name:
                res = search_category_dictionary_for_full_id(categories, category_name, counting=True) # Search through dicts and add counters for every channel with this category
                if res: # Incase result was 'None'
                    categories = res
        added = []
        for chan in channels:
            # Display channels
            if category and not category == "All":
                category_name = chan["category_name"]
                if category_name:
                    category_name = clean_category_name_to_list(category_name)
                if not category_name:
                    continue # Skip this item
                if category_name and not category in category_name:
                    if not category == "main": # Main items (top level categories) are handled further down to avoid any unnecessary conflicts
                        # Display subcategories
                        sub_categories = get_sub_categories(categories, category) # Extract this category dictionary based on it's 'full_id'
                        for key in reversed(sub_categories["subcategories"].keys()): # Iterate this way in order to reverse the dictionary
                            value = sub_categories["subcategories"][key]
                            full_id = key
                            if not full_id == "All":
                                full_id = value["full_id"] # Pull full name out of dict ie. "Dutch -> Sport"
                            if not key in added: # Only display one 
                                added.append(key)
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
                    continue # Skip this item
            title     = chan["name"]
            plot      = chan["name"]
            if not "http" in info["server_info"]["url"]:
                url   = "http://"+info["server_info"]["url"]+":"+info["server_info"]["port"]+"/live/"+username+"/"+password+"/"+chan["stream_id"]+vidcont
            else: url = info["server_info"]["url"]+":"+info["server_info"]["port"]+"/live/"+username+"/"+password+"/"+chan["stream_id"]+vidcont
            thumbnail = chan["stream_icon"]
            fanart    = ''
            plugintools.add_item( action="play" , title=title , plot=plot , url=url ,thumbnail=thumbnail , fanart=fanart , isPlayable=True, folder=False )
            chan_title = title.split(': ')
            if len(chan_title) > 1: chan_title = chan_title[1]
            else: chan_title = chan_title[0]
            if category == "All" and not '----' in chan_title:
                channels_ini.write("%s=plugin://plugin.video.livetv/?name=%s&mode=play\n" % (chan_title, urllib.quote_plus( title )))
                available_channels.append(chan_title)
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
        elif not category:
            # Write channels list to file
            with open(channels_json, 'w') as outfile:
                json.dump(available_channels, outfile)
        if category == "All":
            channels_ini.close()

def populate_links(category):
    info = {}
    with open(cache_json, 'r') as infile:
        info = json.load(infile)
    for chan in channels:
        title     = chan["name"]
        plot      = chan["name"]
        if not "http" in info["server_info"]["url"]:
            url   = "http://"+info["server_info"]["url"]+":"+info["server_info"]["port"]+"/live/"+username+"/"+password+"/"+chan["stream_id"]+vidcont
        else: url = info["server_info"]["url"]+":"+info["server_info"]["port"]+"/live/"+username+"/"+password+"/"+chan["stream_id"]+vidcont
        thumbnail = chan["stream_icon"]
        fanart    = ''
        plugintools.add_item( action="play" , title=title , plot=plot , url=url ,thumbnail=thumbnail , fanart=fanart , isPlayable=True, folder=False )
        chan_title = title.split(': ')
        if len(chan_title) > 1: chan_title = chan_title[1]
        else: chan_title = chan_title[0]
        if not '----' in chan_title:
            channels_ini.write("%s=plugin://plugin.video.iptv/?name=%s&mode=play\n" % (chan_title, urllib.quote_plus( title )))
            available_channels.append(chan_title)
    with open(channels_json, 'w') as outfile:
        json.dump(available_channels, outfile)

def get_epg_sources():
    url = gloabaldata.BASE_URL+"/iptv-epg-sources.php"
    response = net.http_GET(url)
    #return ["http://epg.kodi-forum.nl/tvguide.xml", "http://epg.serbianforum.org/epg.xml.gz"]
    return json.loads(response.content)

def main_list(params):
    url = False
    if gd.user == '' or gd.passw == '':
        My_Window = signin.SignInDialog()
        My_Window.doModal()
        if My_Window.playlisturl:
            url = My_Window.playlisturl
    elif not (gd.user == '' or gd.passw == '') and not gd.auto.lower() == "true":
        My_Window = signin.SignInDialog()
        My_Window.doModal()
        if My_Window.playlisturl:
            url = My_Window.playlisturl
    else:
        data = []
        data_dict = {}
        data_dict["username"] = gd.user
        data_dict["password"] = gd.passw
        data.append(data_dict)
        response = signin.send2remote(mode="signin", data=data)
        if not response["response"] == "success":
            My_Window = signin.SignInDialog()
            My_Window.doModal()
            if My_Window.playlisturl:
                url = My_Window.playlisturl
        else:
            if response["exp_date"] is not None:
                now = time.time()
                if int(response["exp_date"]) > now:
                    tdelta = datetime.datetime.fromtimestamp(int(response["exp_date"]))-datetime.datetime.fromtimestamp(now)
                    #if tdelta.days <= 7:
                    #    text = 'Your license is left [COLOR red][B]'+str(tdelta.days)+'[/B][/COLOR] days. Purchase your valid license.'
                    #    choice = xbmcgui.Dialog().yesno('License warnning', text, nolabel='No, yet',yeslabel='Yes, go to login.')
                    #    if choice is 1:
                    #        My_Window = signin.SignInDialog()
                    #        My_Window.doModal()
                    #        if My_Window.playlisturl:
                    #            url = My_Window.playlisturl
                else:
                    text = '[COLOR red][B]Your license already expired[/B][/COLOR]. Would you like to purchase your valid license? Otherwise you have to shutdown.'
                    choice = xbmcgui.Dialog().yesno('License warnning', text, nolabel='No, shutdown',yeslabel='Yes, go to login.')
                    if choice is 1:
                        My_Window = signin.SignInDialog()
                        My_Window.doModal()
                        if My_Window.playlisturl:
                            url = My_Window.playlisturl
                    else:
                        xbmc.executebuiltin('XBMC.shutdown()')
            url = response["url"]
    if url:
        if params.get("mode") == "play":
            populate_and_play(url, params.get("name"))
        else:
            if gd.selfAddon.getSetting("use_tv_guide").lower() == "true":
                initial_dl = False
                # Get channel list first (or generate one if doesnt exist)
                if os.path.exists(channels_json):
                    with open(channels_json, 'r') as infile:
                        available_channels = json.load(infile)
                else:
                    populate(url)
                    with open(channels_json, 'r') as infile:
                        available_channels = json.load(infile)
                print "RUNNING GUIDE..."
                from resources.libs import custom_xmltv
                #import datetime, time
                basePath = os.path.join(gd.datapath, "xmltv_files")
                if not os.path.exists(basePath):
                    os.makedirs(basePath)
                # Get guide sources from remote url
                #guide_sources = ["http://epg.kodi-forum.nl/tvguide.xml"]
                guide_sources = get_epg_sources()
                for guide in guide_sources:
                    dest = os.path.join(basePath, guide.split('/')[-1])
                    if not os.path.exists(dest):
                        initial_dl = True
                if os.path.exists(epg_file) and not initial_dl:
                    data = custom_xmltv.get_cur_xmltv_data(file=epg_file)
                    print "CURRENT XMLTV:"
                    print data
                    if data:
                        try:
                            datestamp_now = datetime.datetime.now()
                            datestamp_now = int(time.mktime(datestamp_now.timetuple()))
                            datestamp_then = datetime.datetime.strptime(data["date"], "%Y%m%d%H%M%S")
                            datestamp_then = int(time.mktime(datestamp_then.timetuple()))
                            has_been_a_few_days = (datestamp_now - datestamp_then) > 600000
                            if has_been_a_few_days:
                                print "has_been_a_few_days"
                                initial_dl = True
                        except:
                            print "Exception...Set this to initial download!"
                            initial_dl = True
                    else: print "NO DATA"; initial_dl = True
                else: initial_dl = True
                if initial_dl: 
                    print "RUNNING initial_dl..."
                    xbmc.executebuiltin('Notification(IPTV,%s,5000,%s)' % (xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7119), selfIcon))
                    data, channels, programmes = custom_xmltv.process_files(sources=guide_sources, base=basePath, refresh_local="true", channel_filter=available_channels)
                    custom_xmltv.write_final_xmltv(channels, programmes, file=epg_file)
                #xbmc.executebuiltin('RunScript(script.iptv-guide)')
                # Run this as a execute builtin to create a subprocess
                if not initial_dl:
                    has_been_a_day = True
                    data = custom_xmltv.get_cur_xmltv_data(file=epg_file)
                    if data:
                        refresh_local  = "false"
                        datestamp_now  = datetime.datetime.now()
                        datestamp_now  = int(time.mktime(datestamp_now.timetuple()))
                        datestamp_then = datetime.datetime.strptime(data["date"], "%Y%m%d%H%M%S")
                        datestamp_then = int(time.mktime(datestamp_then.timetuple()))
                        has_been_a_day = (datestamp_now - datestamp_then) > 86400
                    if has_been_a_day: refresh_local = "true"
                    guide_sources      = urllib.quote_plus(base64.b64encode(json.dumps(guide_sources)))
                    basePath           = urllib.quote_plus(base64.b64encode(basePath))
                    refresh_local      = urllib.quote_plus(base64.b64encode(refresh_local))
                    available_channels = urllib.quote_plus(base64.b64encode(json.dumps(available_channels)))
                    #AlarmClock(name,command,time[,silent,loop])
                    alarm_name = "IPTV - Run XMLTV update"
                    cmd = "AlarmClock(%s,XBMC.RunPlugin(plugin://plugin.video.iptv/?action=updatexmltv&guide_sources=%s&basePath=%s&refresh_local=%s&available_channels=%s),1,True)"
                    cmd = cmd % (alarm_name, guide_sources, basePath, refresh_local, available_channels)
                    xbmc.executebuiltin('CancelAlarm(%s,True)' % alarm_name)
                    xbmc.executebuiltin(cmd)
                exit()
            else:
                populate(url)

def run():
    plugintools.log("IPTV Client")
    # Get params
    openlist = True
    params = plugintools.get_params()
    if params.get("action") is None:
        main_list(params)
    elif params.get("action") == "play":
        plugintools.play_resolved_url( params.get("url") )
    elif params.get("action") == "updatexmltv":
        print "RUNNING updatexmltv"
        guide_sources      = json.loads(base64.b64decode(params.get("guide_sources")))
        basePath           = base64.b64decode(params.get("basePath"))
        refresh_local      = base64.b64decode(params.get("refresh_local"))
        available_channels = json.loads(base64.b64decode(params.get("available_channels")))
        from resources.libs import custom_xmltv
        data, channels, programmes = custom_xmltv.process_files(sources=guide_sources, base=basePath, refresh_local=refresh_local, channel_filter=available_channels)
        custom_xmltv.write_final_xmltv(channels, programmes, file=epg_file)
    elif params.get("action").split(".")[0] == "category":
        print 'params.get("action").split("category.")[1]'
        cat_dict = params.get("action").split("category.")[1].rstrip().strip()
        print cat_dict
        print base64.urlsafe_b64decode(cat_dict)
        details  = json.loads(base64.urlsafe_b64decode(cat_dict))
        url      = urllib.unquote_plus(details["url"])
        category = details["category"]
        populate(url, use_cache=True, category=category)
    else:
        pass
    if openlist:
        plugintools.close_item_list()


################### RUN ###################

run()
