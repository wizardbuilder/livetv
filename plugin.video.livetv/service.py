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
lastActivityTime = 0
Mwindow = None

if __name__ == '__main__':
	while (not xbmc.abortRequested):
		currentTime = int(time.time())
		# Add on 10 seconds to detect sleep
		if (lastActivityTime == 0) or ((lastActivityTime + 10) < currentTime):
			if Mwindow not in [None, ""]:
				del Mwindow
			url = False
			if gd.user == '' or gd.passw == '':
				Mwindow = signin.SignInDialog()
				print 'domodal:1'
				Mwindow.doModal()

				print ('doModal:user:'+gd.user)
				print ('doModal:passw:'+gd.passw)
				if Mwindow.playlisturl:
					url = Mwindow.playlisturl
			elif not (gd.user == '' or gd.passw == '') and not gd.auto.lower() == "true":
				Mwindow = signin.SignInDialog()
				print 'domodal:2'
				Mwindow.doModal()
				if Mwindow.playlisturl:
					url = Mwindow.playlisturl
			else:
				data = []
				data_dict = {}
				data_dict["username"] = gd.user
				data_dict["password"] = gd.passw
				data.append(data_dict)
				response = signin.send2remote(mode="signin", data=data)
				if not response["response"] == "success":
					Mwindow = signin.SignInDialog()
					print 'domodal:3'
					Mwindow.doModal()
					#if Mwindow.playlisturl:
					#	url = Mwindow.playlisturl
				else:
					#print "exp_date:" + response["exp_date"]
					if int(response["exp_date"]) < 2145826800:
						now = time.time()
						subscriptions = response["subscriptions"]
						if int(response["exp_date"]) > now:
							lefttext = ''
							for key in subscriptions:
								value = subscriptions[key]
								tdelta = datetime.datetime.fromtimestamp(int(value))-datetime.datetime.fromtimestamp(now)
								if tdelta.days <= 7:
									name = key
									if name in gd.bouquet:
										name = gd.bouquet[name]
									lefttext = lefttext+"\n"+name+':'+str(tdelta.days+1)
							if lefttext != '':
								#xbmcgui.Dialog().ok(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8013), '',text,'')
								text = xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8016)
								license = signin.LicenseDialog(text%lefttext, xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8019), xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8020))
								license.doModal()
								choice = license.status#choice = xbmcgui.Dialog().yesno(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8017), text%(tdelta.days+1), nolabel=xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8020),yeslabel=xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8019))
								del license
								if choice is 1:
									Mwindow = signin.SignInDialog()
									print 'domodal:4'
									Mwindow.doModal()
									#if Mwindow.playlisturl:
									#	url = Mwindow.playlisturl
								else:
									break
						else:
							license = signin.LicenseDialog(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8018), xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8019), xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8021))
							license.doModal()
							choice = license.status#choice = xbmcgui.Dialog().yesno(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8017), xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8018), nolabel=xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8021),yeslabel=xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8019))
							del license
							if choice is 1:
								Mwindow = signin.SignInDialog()
								print 'domodal:5'
								Mwindow.doModal()
								#if Mwindow.playlisturl:
								#	url = Mwindow.playlisturl
							else:
								xbmc.executebuiltin('XBMC.shutdown()')
								break
					else:
						break
					#url = response["url"]

			# Make sure the last loop is recorded
			lastActivityTime = currentTime

			#if url:
			#	break

		#xbmc.sleep(100)
		#Mwindow.checkDisplayStatus()
	#if Mwindow is not None:
	#	Mwindow.close()
	#	del Mwindow
