#!/usr/bin/env python
#
#    #######################################################################
#
#    Author Josh.5  https://github.com/josh5
#
#    ########################################################################

import xbmc, xbmcaddon

# Plugin Info
ID               = 'script.service.patchbot17'
ADDON            = xbmcaddon.Addon( ID )
ADDON_ID         = ADDON.getAddonInfo('id')
ADDON_NAME       = ADDON.getAddonInfo('name')
ADDON_ICON       = ADDON.getAddonInfo('icon')
ADDON_VERSION    = ADDON.getAddonInfo('version')
ADDON_DATA       = xbmc.translatePath( "special://profile/addon_data/%s/" % ID )
ADDON_DIR        = ADDON.getAddonInfo( "path" )
KODI_HOME        = xbmc.translatePath("special://home")

if __name__ == '__main__':
    from resources import main
