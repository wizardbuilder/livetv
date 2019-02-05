# -*- coding: utf-8 -*-
import sys
import time
import xbmc
import xbmcaddon
import xbmcgui, datetime
import signin
from gd import gd

##################################
# Main of the Service
##################################
url = False
Mwindow = None

# Check every xxx seconds. This will force a check to the server for authentication
check_frequency = 43200  # 43200 = 12 hours
start_delay = 15
kill_service = False
firstTime = True
nextCheckTime = 0

def action_login(response):
    # print ('LiveTV: action_login')
    # print "exp_date:" + response["exp_date"]
    # if exp_date is less than GMT: Wednesday, 30 December 2037 23:00:00
    if int(response["exp_date"]) < 2145826800:
        now = time.time()
        subscriptions = response["subscriptions"]
        if int(response["exp_date"]) > now:
            clickflixaccess = False
            lefttext = ''
            for key in subscriptions:
                if gd.clickflix_addon_exists and int(key) in gd.clickflix_enabled_bouquet:
                    clickflixaccess = True
                value = subscriptions[key]
                tdelta = datetime.datetime.fromtimestamp(int(value)) - datetime.datetime.fromtimestamp(now)
                if tdelta.days <= 7:
                    name = key
                    if name in gd.bouquet:
                        name = gd.bouquet[name]
                    lefttext = lefttext + "\n" + name + ':' + str(tdelta.days + 1)
            if gd.clickflix_addon_exists and clickflixaccess:
                response = signin.setClickflixCredentials(response["email"], gd.passw)
                if not response:
                    return False
            if lefttext != '':
                # xbmcgui.Dialog().ok(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8013), '',text,'')
                text = xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8016)
                license = signin.LicenseDialog(text % lefttext,
                                               xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8019),
                                               xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8020))
                license.doModal()
                choice = license.status  # choice = xbmcgui.Dialog().yesno(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8017), text%(tdelta.days+1), nolabel=xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8020),yeslabel=xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8019))
                del license
                if choice is 1:
                    Mwindow = signin.SignInDialog()
                    print 'LiveTV:4'
                    Mwindow.doModal()
                    # if Mwindow.playlisturl:
                    #	url = Mwindow.playlisturl
                    return False
            return True
        else:
            license = signin.LicenseDialog(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8018),
                                           xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8019),
                                           xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8021))
            license.doModal()
            choice = license.status  # choice = xbmcgui.Dialog().yesno(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8017), xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8018), nolabel=xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8021),yeslabel=xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8019))
            del license
            if choice is 1:
                Mwindow = signin.SignInDialog()
                print 'LiveTV:5'
                Mwindow.doModal()
                # if Mwindow.playlisturl:
                #	url = Mwindow.playlisturl
                return False
            else:
                xbmc.executebuiltin('XBMC.shutdown()')
                kill_service = True
                return True
    else:
        return True

if __name__ == '__main__':
    monitor = xbmc.Monitor()
    while not monitor.abortRequested():
        # First time
        if firstTime:
            currentTime = int(time.time())
            nextCheckTime = currentTime
            # Add startup delay. This allows kodi start up functions
            if monitor.waitForAbort(start_delay):
                break
            firstTime = False

        currentTime = int(time.time())
        if currentTime > nextCheckTime:
            # print ('LiveTV: Check for credentials')
            if Mwindow not in [None, ""]:
                del Mwindow
                Mwindow = None
            url = False
            if gd.user == '' or gd.passw == '':
                Mwindow = signin.SignInDialog()
                print 'LiveTV:1'
                Mwindow.doModal()

                # print ('LiveTV:user:'+gd.user)
                # print ('LiveTV:passw:'+gd.passw)
                if Mwindow.playlisturl:
                    url = Mwindow.playlisturl
            elif not (gd.user == '' or gd.passw == '') and not gd.auto.lower() == "true":
                Mwindow = signin.SignInDialog()
                print 'LiveTV:2'
                Mwindow.doModal()
                if Mwindow.playlisturl:
                    url = Mwindow.playlisturl
            if gd.user != '' and gd.passw != '':
                # print ('LiveTV: Signing in:')
                data = []
                data_dict = {}
                data_dict["username"] = gd.user
                data_dict["password"] = gd.passw
                data.append(data_dict)
                response = signin.send2remote(mode="signin", data=data)
                if not response["response"] == "success":
                    Mwindow = signin.SignInDialog()
                    print 'LiveTV:3'
                    Mwindow.doModal()
                # if Mwindow.playlisturl:
                #	url = Mwindow.playlisturl
                else:
                    result = False
                    try:
                        result = action_login(response);
                    except:
                        print ('LiveTV: Something went wrong trying to action login... trying again')
                    # print ('LiveTV: result:')
                    if result:
                        break

            nextCheckTime = nextCheckTime + check_frequency
        else:
            if kill_service:
                # print ('LiveTV: kill_service')
                break

            if monitor.waitForAbort(5):
                break