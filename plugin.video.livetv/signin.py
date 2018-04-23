import xbmcgui, xbmc, os, xbmcaddon, mknet, json, time, datetime
from gd import gd

ACTION_PREVIOUS_MENU = 10
ACTION_BACK = 92

class LicenseDialog(xbmcgui.WindowDialog):
	def __init__(self, text1, text2, text3):
      
		self.image_dir			= xbmc.translatePath(os.path.join(gd.selfAddon.getAddonInfo("path"), "resources", "media"))
		self.qrcode		  = self.image_dir+"/red-sign-up-free1.png"
		self.image_background	 = self.image_dir+"/BG.png"
		self.focus_background	 = self.image_dir+"/sign_in.png"
		# save window resolution to arrange the text fields an QR code
		screenx = 1280#self.getWidth()
		screeny = 720#self.getHeight()
		# Show Dialog with Dropbox Authorization URL

		res_qr_code = [screeny/4, screeny/4] # TODO: the image is displayed bigger than the desired size. Find out why.
		self.imgbackground = xbmcgui.ControlImage(0, 0, screenx, screeny, self.image_background)
		self.addControl(self.imgbackground)

		image = xbmcgui.ControlImage(screenx/2-res_qr_code[0]/2, screeny/2-res_qr_code[1]/2, res_qr_code[0], res_qr_code[1], self.qrcode)
		self.addControl(image)

		# Print the Information text below the QR code
		self.addControl(xbmcgui.ControlLabel(x=20, y=20, width=screenx, height=25, label=xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8017), textColor="0xC0FF0000"))
		self.addControl(xbmcgui.ControlLabel(x=0, y=screeny/2+res_qr_code[1]/2+50, width=screenx, height=25, label=text1, textColor='0xFFFFFFFF', alignment=6))
		deltax = 200
		self.okbutton = xbmcgui.ControlButton(x=deltax/2, y=screeny-100, width=screenx/2-deltax, height=50, label=text2, textColor='0xFFFFFFFF',alignment=6,focusTexture=self.focus_background)
		self.cancelbutton = xbmcgui.ControlButton(x=deltax/2+screenx/2, y=screeny-100, width=screenx/2-deltax, height=50, label=text3, textColor='0xFFFFFFFF',alignment=6,focusTexture=self.focus_background)
		self.addControl(self.okbutton)
		self.addControl(self.cancelbutton)
		self.setFocus(self.cancelbutton)

		self.okbutton.controlUp(self.cancelbutton)
		self.okbutton.controlDown(self.cancelbutton)
		self.okbutton.controlLeft(self.cancelbutton)
		self.okbutton.controlRight(self.cancelbutton)
		self.cancelbutton.controlUp(self.okbutton)
		self.cancelbutton.controlDown(self.okbutton)
		self.cancelbutton.controlLeft(self.okbutton)
		self.cancelbutton.controlRight(self.okbutton)

		self.status = 0

	def onControl(self, control):
		if control == self.okbutton:
			self.status = 1
		else:
			self.status = 0
		self.close()

class SignInDialog(xbmcgui.WindowDialog):

	def __init__(self, *args, **kwargs):
		### Define Window Dimentions
		# print self.getWidth()
		# print self.getHeight()
		self.playlisturl = False
		self.screenx = 1280
		self.screeny = 720
		self.winset  = 1
		self.busy	= False
		### Set Locations
		self.image_dir			= xbmc.translatePath(os.path.join(gd.selfAddon.getAddonInfo("path"), "resources", "media"))
		self.image_busy1		  = self.image_dir+"/Busy_Animation_outer.png"
		#self.image_background	 = self.image_dir+"/bg_screen1.jpg"
		self.image_background	 = self.image_dir+"/BG.png"
		#self.image_header_bg	  = self.image_dir+"/header-bg1.png"
		#self.image_header		 = self.image_dir+"/header1.png"
		#self.image_window		 = self.image_dir+"/ContentPanel_invert.png"
		#self.image_body_content   = self.image_dir+"/bg_screen_rounded_long2.png"
		#self.image_form1_bg	   = self.image_dir+"/form_3tier_bg.png"
		#self.image_form2_bg	   = self.image_dir+"/form_1tier_bg1.png"
		#self.image_signup_form_bg = self.image_dir+"/form_signup_bg1.png"
		self.image_s_button	   = self.image_dir+"/button_small1.png"
		#self.image_s_button_selc  = self.image_dir+"/button_small_selected1.png"
		self.image_s_button_selc  = self.image_dir+"/sign_in.png"
		self.image_s_button_signup  = self.image_dir+"/sign_up.png"
		self.image_l_button_selc  = self.image_dir+"/button_large_selected1.png"
		#self.image_txt_input	  = self.image_dir+"/text_input.png"
		#self.image_txt_input_selc = self.image_dir+"/text_input_selected.png"
		#self.image_txt_input	  = self.image_dir+"/frame.png"
		self.image_txt_input_user = self.image_dir+"/user_frame.png"
		self.image_txt_input_user_email = self.image_dir+"/user_email.png"
		self.image_txt_input_user_pass = self.image_dir+"/user_password.png"

		#self.image_firstname = self.image_dir+"/FIRSTNAME.png"
		#self.image_lastname = self.image_dir+"/LASTNAME.png"
		#self.image_chooseusername = self.image_dir+"/CHOOSEUSERNAME.png"
		#self.image_mailaddress = self.image_dir+"/YOUREMAILADDRESS.png"
		self.image_password = self.image_dir+"/PASSWORD.png"
		self.image_confirmpassword = self.image_dir+"/CONFIRMPASSWORD.png"

		self.image_txt_input_selc = self.image_dir+"/frame_border.png"

		self.user_image_for_text_box = self.image_dir+"/user.png"
		
		self.image_txt_input_err  = self.image_dir+"/text_input_error.png"
		self.image_input_err_star = self.image_dir+"/red_star.png"
		self.image_radio_off	  = self.image_dir+"/state_empty.png"
		self.image_radio_off	  = self.image_dir+"/state_cross.png"
		self.image_radio_on	   = self.image_dir+"/state_on.png"
		self.image_radio_on	   = self.image_dir+"/state_tick.png"
		self.image_point_right	= self.image_dir+"/point-right-arrow-red.png"
		self.image_point_left	 = self.image_dir+"/point-left-arrow-red.png"
		self.image_point_up = self.image_dir+"/arrow_sign_up.png"
		### Get remote data
		self.remote_data		  = send2remote()
		#self.image_form2_qrcode   = self.remote_data["qrcode"]
		#self.text_signup_url	  = self.remote_data["signupurl"]
		self.text_signup_url	  = 'http://easyuse.tv'
		#self.image_form2_qrcode   = self.image_dir+"/red-sign-up-free1.png"
		#self.image_form2_qrcode   = ""
		#self.text_signup_url	  = ""
		### Read Settings
		self.hqusername = gd.selfAddon.getSetting("hqusername")
		self.hqpassword = gd.selfAddon.getSetting("hqpassword")
		self.autologin  = gd.selfAddon.getSetting("autologin")
		### Create Window
		self.buildElements()
		self.setActions()
		self.setWinState()

	def buildElements(self): 
		self.firstWindow  = []
		self.secondWindow = []
		self.formerror	= []
		### Build Window Elements
		## Images
		# Background
		self.imgbackground = xbmcgui.ControlImage(0, 0, self.screenx, self.screeny, self.image_background)
		self.addControl(self.imgbackground)
		#self.imgheaderbg = xbmcgui.ControlImage(0, 0, self.screenx, 90, self.image_header_bg)
		#self.addControl(self.imgheaderbg)
		# Main Window
		WINDOW_W = int((self.screenx/1.2))
		WINDOW_H = int((self.screeny/1.1))
		WINDOW_X = int((self.screenx/2)-(WINDOW_W/2))
		WINDOW_Y = int((self.screeny/2)-(WINDOW_H/2))
		#self.imgwindow = xbmcgui.ControlImage(WINDOW_X, WINDOW_Y, WINDOW_W, WINDOW_H, self.image_window)
		#self.addControl(self.imgwindow)
		#self.imgheader = xbmcgui.ControlImage(WINDOW_X, 0, WINDOW_W, 120, self.image_header)
		#self.addControl(self.imgheader)
		# Body Content
		BODY_W = int((WINDOW_W/1.2))
		BODY_H = int((WINDOW_H/1.2))
		BODY_X = int((self.screenx/2)-(BODY_W/2))
		BODY_Y = int((self.screeny/2)-(BODY_H/2))+40
		#self.imgbody = xbmcgui.ControlImage(BODY_X, BODY_Y, BODY_W, BODY_H, self.image_window)
		#self.imgbody.setColorDiffuse('0xC0CCCCCC')
		#self.addControl(self.imgbody)
		#self.firstWindow.append(self.imgbody)
		# Login Form
		FORM1_W = int((BODY_W/1.6))
		FORM1_H = 220
		FORM1_X = int((self.screenx/2)-(FORM1_W/2))
		FORM1_Y = int((self.screeny/2)-(FORM1_H/2))-100
		#self.imgloginform = xbmcgui.ControlImage(FORM1_X, FORM1_Y, FORM1_W, FORM1_H, self.image_form1_bg)
		#self.addControl(self.imgloginform)
		#self.firstWindow.append(self.imgloginform)
		# New Signup Form Button
		FORM2_W = int((BODY_W-60))
		FORM2_H = 265
		FORM2_X = int(BODY_X+30)
		FORM2_Y = int((self.screeny/2)-(FORM2_H/2))+155
		#self.imgnewsignupformbutton = xbmcgui.ControlImage(FORM2_X, FORM2_Y, FORM2_W, FORM2_H, self.image_form2_bg)
		#self.addControl(self.imgnewsignupformbutton)
		#self.firstWindow.append(self.imgnewsignupformbutton)
		# QR code image
		W = 180
		H = 180
		X = int(FORM2_X+(FORM2_W/4)+(FORM2_W/2)-(W/2))
		Y = int((FORM2_Y+65))
		#self.imgqrcode = xbmcgui.ControlImage(X, Y, W, H, self.image_form2_qrcode)
		#self.addControl(self.imgqrcode)
		#self.firstWindow.append(self.imgqrcode)
		# animate arrow left code image
		W = 40
		H = 40
		X = int(FORM2_X+(FORM2_W/4)-(W/2))-100
		Y = int((FORM2_Y+170))
		#self.imgpointright = xbmcgui.ControlImage(X, Y, W, H, self.image_point_right)
		#self.addControl(self.imgpointright)
		#self.imgpointright.setAnimations([
			#("conditional", "effect=fade start=%d end=%d time=500 delay=500 condition=Control.IsVisible(%d)" % (0, 100, self.imgpointright.getId())), 
			#("conditional", "effect=fade start=%d end=%d time=500 delay=500 condition=Control.IsEnabled(%d)" % (0, 100, self.imgpointright.getId())), 
			#("conditional", "effect=fade start=%d end=%d time=500 condition=!Control.IsEnabled(%d)" % (100, 0, self.imgpointright.getId())), 
			#("conditional", "effect=slide start=%d,%d time=500 tween=cubic easing=in delay=10 pulse=true condition=Control.IsVisible(%d)" % (35, 0, self.imgpointright.getId()))])
		#self.firstWindow.append(self.imgpointright)
		#upward arrow below signin
		W = 40
		H = 30
		X = int(FORM2_X+(FORM2_W/4)+(W/2))+190
		Y = int((FORM2_Y+130))
		self.imgpointUp = xbmcgui.ControlImage(X, Y, W, H, self.image_point_up)
		self.addControl(self.imgpointUp)
		self.firstWindow.append(self.imgpointUp)
		W = 200
		H = 40
		X = int(FORM2_X+(FORM2_W/4)+(W/2))+30
		Y = int((FORM2_Y+170))
		self.free_signup_label = xbmcgui.ControlLabel(X, Y, W, H, '', textColor='0xFFEEEEEE', alignment=2|4)
		self.addControl(self.free_signup_label)
		self.free_signup_label.setLabel(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8022))
		self.firstWindow.append(self.free_signup_label)
		
		# animate arrow right code image
		#W = 40
		#H = 40
		#X = int(FORM2_X+(FORM2_W/4)+(W/2))+120
		#Y = int((FORM2_Y+170))
		#self.imgpointleft = xbmcgui.ControlImage(X, Y, W, H, self.image_point_left)
		#self.addControl(self.imgpointleft)
		#self.imgpointleft.setAnimations([
			#("conditional", "effect=fade start=%d end=%d time=500 delay=500 condition=Control.IsVisible(%d)" % (0, 100, self.imgpointleft.getId())), 
			#("conditional", "effect=fade start=%d end=%d time=500 delay=500 condition=Control.IsEnabled(%d)" % (0, 100, self.imgpointleft.getId())), 
			#("conditional", "effect=fade start=%d end=%d time=500 condition=!Control.IsEnabled(%d)" % (100, 0, self.imgpointleft.getId())), 
			#("conditional", "effect=slide start=%d,%d time=500 tween=cubic easing=in delay=10 pulse=true condition=Control.IsVisible(%d)" % (-35, 0, self.imgpointleft.getId()))])
		#self.firstWindow.append(self.imgpointleft)
		#self.imgpointright.setVisible(False)
		#self.imgpointleft.setVisible(False)
		#self.imgpointright.setVisible(True)
		#self.imgpointleft.setVisible(True)
		# # Body Content2
		# BODY2_W = int((WINDOW_W/1.17))
		# BODY2_H = int((WINDOW_H/1.16))
		# BODY2_X = int((self.screenx/2)-(BODY2_W/2))
		# BODY2_Y = int((self.screeny/2)-(BODY2_H/2))+40
		# self.imgbody2 = xbmcgui.ControlImage(BODY2_X, BODY2_Y, BODY2_W, BODY2_H, self.image_window)
		# self.imgbody2.setColorDiffuse('0xC0CCCCCC')
		# self.addControl(self.imgbody2)
		# self.imgbody2.setVisible(False)
		# self.secondWindow.append(self.imgbody2)
		# Signup Form
		FORM3_W = int((WINDOW_W/1.2))
		FORM3_H = int((WINDOW_H/1.2))
		FORM3_X = int((self.screenx/2)-(FORM3_W/2))
		FORM3_Y = int((self.screeny/2)-(FORM3_H/2))+40
		#self.imgsignup = xbmcgui.ControlImage(FORM3_X, FORM3_Y, FORM3_W, FORM3_H, self.image_signup_form_bg)
		#self.addControl(self.imgsignup)
		#self.secondWindow.append(self.imgsignup)
		# Busy
		W = 100
		H = 100
		X = self.screenx-100
		Y = self.screeny-100
		self.imgBusyOuter = xbmcgui.ControlImage(X, Y, W, H, self.image_busy1, aspectRatio=0)
		self.addControl(self.imgBusyOuter)
		self.imgBusyOuter.setAnimations([
			('conditional', 'effect=fade start=%d end=%d time=500 condition=Control.IsVisible(%d)' % (0, 100, self.imgBusyOuter.getId())), 
			('conditional', 'effect=fade start=%d end=%d time=500 condition=Control.IsEnabled(%d)' % (0, 100, self.imgBusyOuter.getId())), 
			('conditional', 'effect=fade start=%d end=%d time=500 condition=!Control.IsEnabled(%d)' % (100, 0, self.imgBusyOuter.getId())), 
			('conditional', 'effect=rotate start=%d end=%d center=auto time=2500 loop=true condition=Control.IsVisible(%d)' % (0, 360, self.imgBusyOuter.getId()))])
		self.imgBusyOuter.setVisible(False)

		## Text Boxes
		# Form1 Label
		W = FORM1_W
		H = 45
		X = int((self.screenx/2)-(W/2))
		Y = int((FORM1_Y))
		#old code
		#self.form1_header = xbmcgui.ControlLabel(X, Y, W, H, '', textColor='0xFFEEEEEE', alignment=2|4)
		#self.addControl(self.form1_header)
		#self.form1_header.setLabel(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7000), shadowColor='0xFF333333')
		#self.firstWindow.append(self.form1_header)
		#end
		# Username Text
		W = 150
		H = 45
		X = int((FORM1_X+40))
		Y = int((FORM1_Y+45))
		#self.username_label = xbmcgui.ControlTextBox(X, Y, W, H, textColor="0xFF777777")
		#self.addControl(self.username_label)
		#self.username_label.setText(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7001))
		#self.firstWindow.append(self.username_label)
		# Password Text
		W = 150
		H = 45
		X = int((FORM1_X+40))
		Y = int((FORM1_Y+105))
		#self.password_label = xbmcgui.ControlTextBox(X, Y, W, H, textColor="0xFF777777")
		#self.addControl(self.password_label)
		#self.password_label.setText(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7002))
		#self.firstWindow.append(self.password_label)
		# Form2 Label
		W = FORM2_W
		H = 45
		X = int(FORM2_X+(FORM2_W/2)-(W/2))
		Y = int((FORM2_Y)+2)
		#self.form2_header = xbmcgui.ControlLabel(X, Y, W, H, '', textColor='0xFFEEEEEE', alignment=2|4)
		#self.addControl(self.form2_header)
		#self.form2_header.setLabel(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7003), shadowColor='0xFF333333')
		#self.firstWindow.append(self.form2_header)
		# Create new account
		W = 450
		H = 80
		X = int(FORM2_X+(FORM2_W/4)-(W/2))+30
		Y = int((FORM2_Y+70))
		#self.click_for_new_account_form_text = xbmcgui.ControlLabel(X, Y, W, H, '', textColor="0xFF777777", alignment=2|4)
		#self.addControl(self.click_for_new_account_form_text)
		#self.click_for_new_account_form_text.setLabel(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7004))
		#self.firstWindow.append(self.click_for_new_account_form_text)
		# Create free account
		#W = 300
		#H = 80
		#X = int(FORM2_X+(FORM2_W/4)-(W/2))+430
		#Y = int((FORM2_Y+120))
		#self.click_for_new_accounttrial_form_text = xbmcgui.ControlLabel(X, Y, W, H, '', textColor="0xFF777777", alignment=2|4)
		#self.addControl(self.click_for_new_accounttrial_form_text)
		#self.click_for_new_accounttrial_form_text.setLabel(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8012))
		#self.firstWindow.append(self.click_for_new_accounttrial_form_text)
		# Sign up url
		W = 450
		H = 45
		X = int(FORM2_X+(FORM2_W/4)-(W/2))+50
		Y = int((FORM2_Y+215))
		#self.signup_url_text = xbmcgui.ControlLabel(X, Y, W, H, '', textColor="0xFF777777", alignment=2|4)
		#self.addControl(self.signup_url_text)
		#self.signup_url_text.setLabel('[I]'+self.text_signup_url+'[/I]')
		#self.firstWindow.append(self.signup_url_text)
		# Unique code Text
		W = 370
		H = 45
		X = int((FORM3_X)+100)
		Y = int((FORM3_Y)+10)
		#self.unique_code_label = xbmcgui.ControlLabel(X, Y, W, H, '', textColor="0xFF777777", alignment=1)
		#self.addControl(self.unique_code_label)
		#self.unique_code_label.setLabel(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7005))
		#self.secondWindow.append(self.unique_code_label)
		# First & Last name Text
		W = 370
		H = 45
		X = int((FORM3_X)+10)
		Y = int((FORM3_Y)+110)
		# old code
		#self.name_label = xbmcgui.ControlLabel(X, Y, W, H, '', textColor="0xFF777777", alignment=1)
		#self.addControl(self.name_label)
		#self.name_label.setLabel(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7006))
		#self.secondWindow.append(self.name_label)
		#end
		# Email address Text
		W = 370
		H = 75
		X = int((FORM3_X)+10)
		Y = int((FORM3_Y)+152)
		#old code
		#self.email_label = xbmcgui.ControlLabel(X, Y, W, H, '', textColor="0xFF777777", alignment=1)
		#self.addControl(self.email_label)
		#self.email_label.setLabel(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7007))
		#self.secondWindow.append(self.email_label)
		#end
		# Email address long text
		# W = 370
		# H = 50
		# X = int((FORM3_X)+10)
		# Y = int((FORM3_Y)+178)
		# self.email_long_text = xbmcgui.ControlTextBox(X, Y, W, H, textColor="0xFF777777")
		# self.addControl(self.email_long_text)
		# self.email_long_text.setText('(an email confirmation will be sent to this address)')
		# self.secondWindow.append(self.email_long_text)
		# Create username text
		W = 370
		H = 75
		X = int((FORM3_X)+10)
		Y = int((FORM3_Y)+270)
		#old
		#self.create_username_label = xbmcgui.ControlLabel(X, Y, W, H, '', textColor="0xFF777777", alignment=1)
		#self.addControl(self.create_username_label)
		#self.create_username_label.setLabel(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7008))
		#self.secondWindow.append(self.create_username_label)
		#end
		# Create username long text
		# W = 370
		# H = 40
		# X = int((FORM3_X)+10)
		# Y = int((FORM3_Y)+295)
		# self.create_username_long_text = xbmcgui.ControlTextBox(X, Y, W, H, textColor="0xFF777777")
		# self.addControl(self.create_username_long_text)
		# self.create_username_long_text.setText('(should consist of more than 6 characters and may contain only letters, numbers and underscores)')
		# self.secondWindow.append(self.create_username_long_text)
		# # Create password text
		W = 370
		H = 45
		X = int((FORM3_X)+10)
		Y = int((FORM3_Y)+370)
		#old
		#self.create_password_label = xbmcgui.ControlLabel(X, Y, W, H, '', textColor="0xFF777777", alignment=1)
		#self.addControl(self.create_password_label)
		#self.create_password_label.setLabel(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7009))
		#self.secondWindow.append(self.create_password_label)
		#end
		# Create password long text
		# W = 370
		# H = 75
		# X = int((FORM3_X)+10)
		# Y = int((FORM3_Y)+395)
		# self.create_password_long_text = xbmcgui.ControlTextBox(X, Y, W, H, textColor="0xFF777777")
		# self.addControl(self.create_password_long_text)
		# self.create_password_long_text.setText('(must consist of more than 6 characters)')
		# self.secondWindow.append(self.create_password_long_text)
		# Confirm new password text
		W = 370
		H = 20
		X = int((FORM3_X)+10)
		Y = int((FORM3_Y)+440)
		#old
		#self.confirm_password_label = xbmcgui.ControlLabel(X, Y, W, H, '', textColor="0xFF777777", alignment=1)
		#self.addControl(self.confirm_password_label)
		#self.confirm_password_label.setLabel(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7010))
		#self.secondWindow.append(self.confirm_password_label)
		#end
		## Buttons
		# Auto login radiobutton
		W = 270
		H = 45
		X = int((FORM1_X+10))
		Y = int((FORM1_Y+165))
		#self.autologin_toggle_button = xbmcgui.ControlRadioButton(X, Y, W, H, label='', textColor="0xFF777777", _alignment=0|4, 
			#focusTexture=self.image_l_button_selc, 
			#noFocusTexture='', 
			#focusOnTexture=self.image_radio_on, 
			#noFocusOnTexture=self.image_radio_on, 
			#focusOffTexture=self.image_radio_off, 
			#noFocusOffTexture=self.image_radio_off, 
			#textOffsetX=17)
		#self.autologin_toggle_button.setLabel(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7015))
		#self.addControl(self.autologin_toggle_button)
		#if self.autologin.lower() == "true":
			#self.autologin_toggle_button.setSelected(True)
		#self.firstWindow.append(self.autologin_toggle_button)
		# Login button
		#W = 100
		#H = 45
		#X = int((FORM1_X+400))
		#Y = int((FORM1_Y+165))

		W = 200
		H = 45
		X = int((FORM1_X+200))
		Y = int((FORM1_Y+250))
		# ControlButton(x, y, width, height, label[, focusTexture, noFocusTexture, textOffsetX, textOffsetY,
		#			   alignment, font, textColor, disabledColor, angle, shadowColor, focusedColor])
		#self.login_button = xbmcgui.ControlButton(X, Y, W, H, label='', textColor="0xFF777777", focusTexture=self.image_s_button_selc, noFocusTexture=self.image_s_button, alignment=2|4)
		#self.login_button.setLabel(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7011))
		#self.addControl(self.login_button)
		#self.firstWindow.append(self.login_button)
		self.login_button = xbmcgui.ControlButton(X, Y, W, H, label='', textColor="0xFF777777", focusTexture=self.image_s_button_selc, noFocusTexture=self.image_s_button_selc, alignment=2|4)
		self.login_button.setLabel(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7011))
		self.addControl(self.login_button)
		self.firstWindow.append(self.login_button)
		# New Account form button
		#old signup button
		#W = 130
		#H = 45
		#X = int(FORM2_X+(FORM2_W/2)-(W/2))
		#X = int(FORM2_X+(FORM2_W/4)-(W/2))+30
		#Y = int((FORM2_Y+170))
		#self.new_acct_button = xbmcgui.ControlButton(X, Y, W, H, label='', textColor="0xFF777777", focusTexture=self.image_s_button_selc, noFocusTexture=self.image_s_button, alignment=2|4)
		#self.new_acct_button.setLabel(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7012))
		#self.addControl(self.new_acct_button)
		#self.firstWindow.append(self.new_acct_button)

		#new sign up button
		W = 200
		H = 45
		#X = int(FORM2_X+(FORM2_W/2)-(W/2))
		X = int((FORM1_X+200))
		Y = int((FORM1_Y+300))
		self.new_acct_button = xbmcgui.ControlButton(X, Y, W, H, label='', textColor="0xFF777777", focusTexture=self.image_s_button_signup, noFocusTexture=self.image_s_button_signup, alignment=2|4)
		self.new_acct_button.setLabel(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7012))
		self.addControl(self.new_acct_button)
		self.firstWindow.append(self.new_acct_button)
		
		# cancel form button
		#old code
		#W = 110
		#H = 45
		#X = int((FORM3_X+10))
		#Y = int((FORM3_Y+492))
		#self.cancel_signup_button = xbmcgui.ControlButton(X, Y, W, H, label='', textColor="0xFF777777", focusTexture=self.image_s_button_selc, noFocusTexture=self.image_s_button, alignment=2|4)
		#self.cancel_signup_button.setLabel(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7013))
		#self.addControl(self.cancel_signup_button)
		#self.secondWindow.append(self.cancel_signup_button)
		#end
		W = 300
		H = 45
		X = int((FORM3_X+300))
		Y = int((FORM3_Y+400))
		self.cancel_signup_button = xbmcgui.ControlButton(X, Y, W, H, label='', textColor="0xFF777777", focusTexture=self.image_s_button_selc, noFocusTexture=self.image_s_button_selc, alignment=2|4)
		self.cancel_signup_button.setLabel(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7013))
		self.addControl(self.cancel_signup_button)
		self.secondWindow.append(self.cancel_signup_button)
		
		# submit form button
		#old code
		#W = 130
		#H = 45
		#X = int((self.screenx/2)-(W/2))
		#Y = int((FORM3_Y+492))
		#self.submit_signup_button = xbmcgui.ControlButton(X, Y, W, H, label='', textColor="0xFF777777", focusTexture=self.image_s_button_selc, noFocusTexture=self.image_s_button, alignment=2|4)
		#self.submit_signup_button.setLabel(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7014))
		#self.addControl(self.submit_signup_button)
		#self.secondWindow.append(self.submit_signup_button)
		#end code
		W = 300
		H = 45
		X = int((FORM3_X+300))
		Y = int((FORM3_Y+350))
		self.submit_signup_button = xbmcgui.ControlButton(X, Y, W, H, label='', textColor="0xFF777777", focusTexture=self.image_s_button_signup, noFocusTexture=self.image_s_button_signup, alignment=2|4)
		#self.submit_signup_button.setLabel(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7014))
		self.submit_signup_button.setLabel(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7012))
		self.addControl(self.submit_signup_button)
		self.secondWindow.append(self.submit_signup_button)
		
		# free trial form button
		#W = 130
		#H = 45
		#X = int(FORM3_X+FORM3_W-W-10)
		#Y = int((FORM3_Y+492))
		#self.submit_signuptrial_button = xbmcgui.ControlButton(X, Y, W, H, label='', textColor="0xFF777777", focusTexture=self.image_s_button_selc, noFocusTexture=self.image_s_button, alignment=2|4)
		#self.submit_signuptrial_button.setLabel(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8011))
		#self.addControl(self.submit_signuptrial_button)
		#self.secondWindow.append(self.submit_signuptrial_button)

		## TextEdit
		# Username entry
		# old user name text box
		#W = 300
		#H = 45
		#X = int((FORM1_X+200))
		#Y = int((FORM1_Y+50))
		#self.username_textbox = xbmcgui.ControlEdit(X, Y, W, H, '', textColor="0xFF777777", focusTexture=self.image_txt_input_selc, noFocusTexture=self.image_txt_input, _alignment=6|4)
		#self.username_textbox.setPosition(X, Y)
		#self.username_textbox.setHeight(H)
		#self.username_textbox.setWidth(W)
		#self.addControl(self.username_textbox)
		#self.username_textbox.setText(self.hqusername)
		#self.firstWindow.append(self.username_textbox)
		W = 300
		H = 45
		X = int((FORM1_X+150))
		Y = int((FORM1_Y+110))
		#self.user_text_field_image=xbmcgui.ControlImage (X, Y, 30, 30, self.user_image_for_text_box)

		self.username_textbox = xbmcgui.ControlEdit(X, Y, W, H, '', textColor="0xFF777777", focusTexture=self.image_txt_input_selc, noFocusTexture=self.image_txt_input_user, _alignment=6|4)
		self.username_textbox.setPosition(X, Y)
		self.username_textbox.setHeight(H)
		self.username_textbox.setWidth(W)
		self.addControl(self.username_textbox)
		self.username_textbox.setText(self.hqusername)
		self.firstWindow.append(self.username_textbox)
		# password entry
		#old password
		#W = 300
		#H = 45
		#X = int((FORM1_X+200))
		#Y = int((FORM1_Y+110))
		#self.password_textbox = xbmcgui.ControlEdit(X, Y, W, H, '', textColor="0xFF777777", focusTexture=self.image_txt_input_selc, noFocusTexture=self.image_txt_input, _alignment=6|4, isPassword=True)
		#self.password_textbox.setPosition(X, Y)
		#self.password_textbox.setHeight(H)
		#self.password_textbox.setWidth(W)
		#self.addControl(self.password_textbox)
		#self.password_textbox.setText(self.hqpassword)
		#self.firstWindow.append(self.password_textbox)

		W = 300
		H = 45
		X = int((FORM1_X+150))
		Y = int((FORM1_Y+180))
		self.password_textbox = xbmcgui.ControlEdit(X, Y, W, H, '', textColor="0xFF777777", focusTexture=self.image_txt_input_selc, noFocusTexture=self.image_txt_input_user_pass, _alignment=6|4, isPassword=True)
		self.password_textbox.setPosition(X, Y)
		self.password_textbox.setHeight(H)
		self.password_textbox.setWidth(W)
		self.addControl(self.password_textbox)
		self.password_textbox.setText(self.hqpassword)
		self.firstWindow.append(self.password_textbox)

		# unique code entry
		#W = 200
		#H = 45
		#X = int((FORM3_X)+400)
		#Y = int((FORM3_Y)+5)
		#self.unique_code_bg = self.image_txt_input
		#self.unique_code_textbox = xbmcgui.ControlEdit(X, Y, W, H, '', textColor="0xFF777777", focusTexture=self.image_txt_input_selc, noFocusTexture=self.unique_code_bg, _alignment=6|4)
		#self.unique_code_textbox.setPosition(X, Y)
		#self.unique_code_textbox.setHeight(H)
		#self.unique_code_textbox.setWidth(W)
		#self.addControl(self.unique_code_textbox)
		#self.secondWindow.append(self.unique_code_textbox)
		#X = int(X+W+10)
		#Y = int(Y+10)
		#self.error_unique_code = xbmcgui.ControlImage(X, Y, 10, 10, self.image_input_err_star)
		#self.addControl(self.error_unique_code)
		#self.error_unique_code.setVisible(False)
		#self.formerror.append(self.error_unique_code)
		# first name entry
		#old code
		#W = 200
		#H = 45
		#X = int((FORM3_X)+400)
		#Y = int((FORM3_Y)+100)
		#end
		W = 350
		H = 55
		X = int((FORM3_X)+80)
		Y = int((FORM3_Y)+100)
		
		self.first_name_textbox = xbmcgui.ControlEdit(X, Y, W, H, '', textColor="0xFF777777", focusTexture=self.image_txt_input_selc, noFocusTexture=self.image_txt_input_user, _alignment=6|4)
		self.first_name_textbox.setPosition(X, Y)
		self.first_name_textbox.setHeight(H)
		self.first_name_textbox.setWidth(W)
		self.addControl(self.first_name_textbox)
		#self.ctrlimg_firstname = xbmcgui.ControlImage(X, Y, W, H, self.image_firstname)
		#self.addControl(self.ctrlimg_firstname)
		#cid = self.first_name_textbox.getId()
		#visibleCondition = '[!Control.HasFocus(%d) & Control.getText(%d)]'%(cid, cid)
		#self.ctrlimg_firstname.setVisibleCondition(visibleCondition, False)
		self.first_name_textbox.setText("FIRST NAME")
		self.secondWindow.append(self.first_name_textbox)
		#self.secondWindow.append(self.ctrlimg_firstname)
		
		#self.secondWindow.append(self.confirm_password_label)
		# last name entry
		W = 350
		H = 55
		X = int((FORM3_X)+490)
		Y = int((FORM3_Y)+100)
		self.last_name_textbox = xbmcgui.ControlEdit(X, Y, W, H, '', textColor="0xFF777777", focusTexture=self.image_txt_input_selc, noFocusTexture=self.image_txt_input_user, _alignment=6|4)
		self.last_name_textbox.setPosition(X, Y)
		self.last_name_textbox.setHeight(H)
		self.last_name_textbox.setWidth(W)
		self.addControl(self.last_name_textbox)
		self.last_name_textbox.setText("LAST NAME")
		self.secondWindow.append(self.last_name_textbox)
		X = int(X+W+10)
		Y = int(Y+10)
		self.error_names = xbmcgui.ControlImage(X, Y, 10, 10, self.image_input_err_star)
		self.addControl(self.error_names)
		self.error_names.setVisible(False)
		self.formerror.append(self.error_names)
		# email entry
		#old code
		#W = 340
		#H = 45
		#X = int((FORM3_X)+400)
		#Y = int((FORM3_Y)+165)
		#end
		W = 350
		H = 55
		X = int((FORM3_X)+490)
		Y = int((FORM3_Y)+190)
		self.create_email_textbox = xbmcgui.ControlEdit(X, Y, W, H, '', textColor="0xFF777777", focusTexture=self.image_txt_input_selc, noFocusTexture=self.image_txt_input_user_email, _alignment=6|4)
		self.create_email_textbox.setPosition(X, Y)
		self.create_email_textbox.setHeight(H)
		self.create_email_textbox.setWidth(W)
		self.addControl(self.create_email_textbox)
		self.create_email_textbox.setText("YOUR EMAIL ADDRESS")
		self.secondWindow.append(self.create_email_textbox)
		X = int(X+W+10)
		Y = int(Y+10)
		self.error_email = xbmcgui.ControlImage(X, Y, 10, 10, self.image_input_err_star)
		self.addControl(self.error_email)
		self.error_email.setVisible(False)
		self.formerror.append(self.error_email)
		# username entry
		#old code
		#W = 340
		#H = 45
		#X = int((FORM3_X)+400)
		#Y = int((FORM3_Y)+285)
		#end
		W = 350
		H = 55
		X = int((FORM3_X)+80)
		Y = int((FORM3_Y)+190)
		self.create_username_textbox = xbmcgui.ControlEdit(X, Y, W, H, '', textColor="0xFF777777", focusTexture=self.image_txt_input_selc, noFocusTexture=self.image_txt_input_user, _alignment=6|4)
		self.create_username_textbox.setPosition(X, Y)
		self.create_username_textbox.setHeight(H)
		self.create_username_textbox.setWidth(W)
		self.addControl(self.create_username_textbox)
		self.create_username_textbox.setText("CHOOSE A USER NAME")
		self.secondWindow.append(self.create_username_textbox)
		X = int(X+W+10)
		Y = int(Y+10)
		self.error_username = xbmcgui.ControlImage(X, Y, 10, 10, self.image_input_err_star)
		self.addControl(self.error_username)
		self.error_username.setVisible(False)
		self.formerror.append(self.error_username)
		# password entry
		# old code
		#W = 340
		#H = 45
		#X = int((FORM3_X)+400)
		#Y = int((FORM3_Y)+377)
		#end

		#create password position
		W = 350
		H = 55
		X = int((FORM3_X)+80)
		Y = int((FORM3_Y)+275)
		self.create_password_textbox = xbmcgui.ControlEdit(X, Y, W, H, '', textColor="0xFF777777", focusTexture=self.image_txt_input_selc, noFocusTexture=self.image_txt_input_user_pass, _alignment=6|4, isPassword=True)
		#self.create_password_textbox = xbmcgui.ControlEdit(X, Y, W, H, '', textColor="0xFF777777", focusTexture=self.image_txt_input_selc, noFocusTexture=self.image_txt_input_user_pass, _alignment=6|4)
		self.create_password_textbox.setPosition(X, Y)
		self.create_password_textbox.setHeight(H)
		self.create_password_textbox.setWidth(W)
		#self.create_password_textbox.setText('PASSWORD')
		self.addControl(self.create_password_textbox)
		self.ctrlimg_password = xbmcgui.ControlImage(X, Y, W, H, self.image_password)
		self.addControl(self.ctrlimg_password)
		cid = self.create_password_textbox.getId()
		visibleCondition = '!Control.HasFocus(%d)'%cid
		self.ctrlimg_password.setVisibleCondition(visibleCondition, False)
		#self.create_password_textbox.setText("PASSWORD")
		self.secondWindow.append(self.create_password_textbox)
		self.secondWindow.append(self.ctrlimg_password)
		X = int(X+W+10)
		Y = int(Y+10)
		self.error_password = xbmcgui.ControlImage(X, Y, 10, 10, self.image_input_err_star)
		self.addControl(self.error_password)
		self.error_password.setVisible(False)
		self.formerror.append(self.error_password)
		# confirm password entry
		#old code
		#W = 340
		#H = 45
		#X = int((FORM3_X)+400)
		#Y = int((FORM3_Y)+435)
		#end
		# confirm password points
		W = 350
		H = 55
		X = int((FORM3_X)+490)
		Y = int((FORM3_Y)+275)
		
		self.confirm_password_textbox = xbmcgui.ControlEdit(X, Y, W, H, '', textColor="0xFF777777", focusTexture=self.image_txt_input_selc, noFocusTexture=self.image_txt_input_user_pass, _alignment=6|4, isPassword=True)
		#self.confirm_password_textbox = xbmcgui.ControlEdit(X, Y, W, H, '', textColor="0xFF777777", focusTexture=self.image_txt_input_selc, noFocusTexture=self.image_txt_input_user_pass, _alignment=6|4)
		self.confirm_password_textbox.setPosition(X, Y)
		self.confirm_password_textbox.setHeight(H)
		self.confirm_password_textbox.setWidth(W)
		#self.confirm_password_textbox.setText('CONFIRM YOUR PASSWORD')
		self.addControl(self.confirm_password_textbox)
		self.ctrlimg_confirmpassword = xbmcgui.ControlImage(X, Y, W, H, self.image_confirmpassword)
		self.addControl(self.ctrlimg_confirmpassword)
		cid = self.confirm_password_textbox.getId()
		visibleCondition = '!Control.HasFocus(%d)'%cid
		self.ctrlimg_confirmpassword.setVisibleCondition(visibleCondition, False)
		#self.confirm_password_textbox.setText("      CONFIRM YOUR PASSWORD")
		self.secondWindow.append(self.confirm_password_textbox)
		self.secondWindow.append(self.ctrlimg_confirmpassword)
		X = int(X+W+10)
		Y = int(Y+10)
		self.error_passwordconfirm = xbmcgui.ControlImage(X, Y, 10, 10, self.image_input_err_star)
		self.addControl(self.error_passwordconfirm)
		self.error_passwordconfirm.setVisible(False)
		self.formerror.append(self.error_passwordconfirm)


	def setActions(self):
		# winset #1
		self.username_textbox.controlUp(self.new_acct_button)
		self.username_textbox.controlDown(self.password_textbox)
		self.password_textbox.controlUp(self.username_textbox)
		self.password_textbox.controlDown(self.login_button)
		#self.autologin_toggle_button.controlUp(self.password_textbox)
		#self.autologin_toggle_button.controlDown(self.login_button)
		#self.autologin_toggle_button.controlLeft(self.login_button)
		#self.autologin_toggle_button.controlRight(self.login_button)
		self.login_button.controlUp(self.password_textbox)
		self.login_button.controlDown(self.new_acct_button)
		#self.login_button.controlLeft(self.autologin_toggle_button)
		#self.login_button.controlRight(self.autologin_toggle_button)
		self.new_acct_button.controlUp(self.login_button)
		self.new_acct_button.controlDown(self.username_textbox)
		# winset #2
		#self.unique_code_textbox.controlUp(self.confirm_password_textbox)
		#self.unique_code_textbox.controlDown(self.first_name_textbox)
		self.first_name_textbox.controlUp(self.submit_signup_button)
		self.first_name_textbox.controlDown(self.last_name_textbox)
		#self.first_name_textbox.controlLeft(self.last_name_textbox)
		#self.first_name_textbox.controlRight(self.last_name_textbox)

		self.last_name_textbox.controlUp(self.first_name_textbox)
		self.last_name_textbox.controlDown(self.create_username_textbox)
		#self.last_name_textbox.controlLeft(self.first_name_textbox)
		#self.last_name_textbox.controlRight(self.first_name_textbox)

		self.create_username_textbox.controlUp(self.last_name_textbox)
		self.create_username_textbox.controlDown(self.create_email_textbox)

		self.create_email_textbox.controlUp(self.create_username_textbox)
		self.create_email_textbox.controlDown(self.create_password_textbox)

		self.create_password_textbox.controlUp(self.create_username_textbox)
		self.create_password_textbox.controlDown(self.confirm_password_textbox)

		self.confirm_password_textbox.controlUp(self.create_password_textbox)
		self.confirm_password_textbox.controlDown(self.submit_signup_button)

		self.submit_signup_button.controlUp(self.confirm_password_textbox)
		self.submit_signup_button.controlDown(self.cancel_signup_button)#self.submit_signup_button.controlDown(self.submit_signuptrial_button)
		self.submit_signup_button.controlLeft(self.confirm_password_textbox)
		self.submit_signup_button.controlRight(self.cancel_signup_button)#self.submit_signup_button.controlRight(self.submit_signuptrial_button)

		self.cancel_signup_button.controlUp(self.submit_signup_button)
		self.cancel_signup_button.controlDown(self.first_name_textbox)
		self.cancel_signup_button.controlLeft(self.submit_signup_button)
		self.cancel_signup_button.controlRight(self.first_name_textbox)
		#self.submit_signuptrial_button.controlUp(self.submit_signup_button)
		#self.submit_signuptrial_button.controlDown(self.unique_code_textbox)
		#self.submit_signuptrial_button.controlLeft(self.submit_signup_button)
		#self.submit_signuptrial_button.controlRight(self.cancel_signup_button)


	def setWinState(self):
		self.busy = True
		self.imgBusyOuter.setVisible(True)
		#time.sleep(1)
		if self.winset == 1:
			for element in self.secondWindow:
				element.setVisible(False)
			for element in self.formerror:
				element.setVisible(False)
			for element in self.firstWindow:
				element.setVisible(True)
			if gd.selfAddon.getSetting("hqusername"): self.setFocus(self.login_button)
			else: self.setFocus(self.username_textbox)
		elif self.winset == 2:
			for element in self.firstWindow:
				element.setVisible(False)
			for element in self.secondWindow:
				element.setVisible(True)
			self.setFocus(self.first_name_textbox)#self.setFocus(self.unique_code_textbox)
		#time.sleep(.5)
		self.imgBusyOuter.setVisible(False)
		self.busy = False


	def checkvalidform(self, trial=False):
		result = True
		mtfields=[]
		error_password=False
		error_passwordconfirm=False
		if trial == False:
			self.error_unique_code.setVisible(True); mtfields.append(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7100)) if not self.unique_code_textbox.getText() else self.error_unique_code.setVisible(False)
		self.error_names.setVisible(True); mtfields.append(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7101)) if not self.first_name_textbox.getText() or not self.last_name_textbox.getText() else self.error_names.setVisible(False)
		self.error_email.setVisible(True); mtfields.append(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7102)) if not self.create_email_textbox.getText() else self.error_email.setVisible(False)
		self.error_username.setVisible(True); mtfields.append(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7103)) if not self.create_username_textbox.getText() or " " in self.create_username_textbox.getText() else self.error_username.setVisible(False)
		self.error_password.setVisible(True); error_password=True if not self.create_password_textbox.getText() or len(self.create_password_textbox.getText()) < 6 else self.error_password.setVisible(False)
		self.error_passwordconfirm.setVisible(True) if not self.confirm_password_textbox.getText() or self.create_password_textbox.getText() != self.confirm_password_textbox.getText() else self.error_passwordconfirm.setVisible(False)
		if mtfields:
			result = False
			for x in mtfields:
				xbmcgui.Dialog().ok(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7104), '',x,'')
		if error_password:
			result = False
			xbmcgui.Dialog().ok(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7105), '',xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7106),'')
		if self.create_password_textbox.getText() != self.confirm_password_textbox.getText():
			result = False
			self.error_passwordconfirm.setVisible(True)
			xbmcgui.Dialog().ok(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7107), xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7108), xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7109),'')
		return result

	def handler_signupresponse(self):
		self.busy = True
		self.imgBusyOuter.setVisible(True)
		time.sleep(.5)
		data = []
		data_dict = {}
		data_dict["username"] = self.create_username_textbox.getText()
		data_dict["password"] = self.create_password_textbox.getText()
		data_dict["email"]	= self.create_email_textbox.getText()
		data_dict["fname"]	= self.first_name_textbox.getText()
		data_dict["lname"]	= self.last_name_textbox.getText()
		data_dict["coupon"]   = ""
		#if not self.unique_code_textbox.getText():
		#	data_dict["coupon"]   = ""
		#else:
		#	data_dict["coupon"]   = self.unique_code_textbox.getText()

		# TESTING ONLY:
		################################################
		# data_dict = {}
		# data_dict["username"] = "testname6"
		# data_dict["password"] = "testpassword"
		# data_dict["email"]	= "testname6@gmail.com"
		# data_dict["fname"]	= "myfirstname"
		# data_dict["lname"]	= "mylastname"
		# data_dict["coupon"]   = "38570"
		################################################

		data.append(data_dict)
		response = send2remote(mode="signup", data=data)
		time.sleep(.5)
		self.imgBusyOuter.setVisible(False)
		self.busy = False
		if response["response"] == "errors":
			errors=response["errors"]
			for x in errors:
				text = x["text"]
				if not x["id"] in ["coupon", 'name_f', 'name_l', "email", "login", "pass", "_pass"]:
					if x["id"] == "coupon": self.error_unique_code.setVisible(True); text = xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7110)+"\n"+x["text"]
					if x["id"] == 'name_f': self.error_names.setVisible(True); text = xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7111)+"\n"+x["text"]
					if x["id"] == 'name_l': self.error_names.setVisible(True); text = xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7112)+"\n"+x["text"]
					if x["id"] == "email": self.error_email.setVisible(True); text = xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7113)+"\n"+x["text"]
					if x["id"] == "login": self.error_username.setVisible(True); text = xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7114)+"\n"+x["text"]
					if x["id"] == "pass": self.error_password.setVisible(True); text = xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7115)+"\n"+x["text"]
					if x["id"] == "_pass": self.error_passwordconfirm.setVisible(True); text = xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7116)+"\n"+x["text"]
					xbmcgui.Dialog().ok(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7117), '',text,'')
		elif response["response"] == "success":
			if int(response["exp_date"]) < 2145826800:
				text = xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8014)+"\n"+datetime.datetime.fromtimestamp(int(response["exp_date"])).strftime('%Y-%m-%d %H:%M:%S')
                                       
				xbmcgui.Dialog().ok(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8013), '',text,'')
			# Save login information into addon settings
			gd.selfAddon.setSetting("hqusername",data_dict["username"])
			gd.selfAddon.setSetting("hqpassword",data_dict["password"])
			self.username_textbox.setText(data_dict["username"])
			self.password_textbox.setText(data_dict["password"])
			if gd.selfAddon.getSetting("autologin").lower() == "true":
				time.sleep(.5)
				self.handler_loginresponse()
			else:
				self.winset = 1
				self.setWinState()

	def handler_signupresponseTrial(self):
		print 'handler_signupresponseTrial'
		self.busy = True
		self.imgBusyOuter.setVisible(True)
		time.sleep(.5)
		data = []
		data_dict = {}
		data_dict["username"] = self.create_username_textbox.getText()
		data_dict["password"] = self.create_password_textbox.getText()
		data_dict["email"]	= self.create_email_textbox.getText()
		data_dict["fname"]	= self.first_name_textbox.getText()
		data_dict["lname"]	= self.last_name_textbox.getText()
		#data_dict["coupon"]   = self.unique_code_textbox.getText()

		# TESTING ONLY:
		################################################
		# data_dict = {}
		# data_dict["username"] = "testname6"
		# data_dict["password"] = "testpassword"
		# data_dict["email"]	= "testname6@gmail.com"
		# data_dict["fname"]	= "myfirstname"
		# data_dict["lname"]	= "mylastname"
		# data_dict["coupon"]   = "38570"
		################################################

		data.append(data_dict)
		response = send2remote(mode="signuptrial", data=data)
		time.sleep(.5)
		self.imgBusyOuter.setVisible(False)
		self.busy = False
		if response["response"] == "errors":
			errors=response["errors"]
			for x in errors:
				text = x["text"]
				#if not x["id"] in ["coupon", 'name_f', 'name_l', "email", "login", "pass", "_pass"]:
				if x["id"] == "coupon": self.error_unique_code.setVisible(True); text = xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7110)+"\n"+x["text"]
				if x["id"] == 'name_f': self.error_names.setVisible(True); text = xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7111)+"\n"+x["text"]
				if x["id"] == 'name_l': self.error_names.setVisible(True); text = xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7112)+"\n"+x["text"]
				if x["id"] == "email": self.error_email.setVisible(True); text = xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7113)+"\n"+x["text"]
				if x["id"] == "login": self.error_username.setVisible(True); text = xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7114)+"\n"+x["text"]
				if x["id"] == "pass": self.error_password.setVisible(True); text = xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7115)+"\n"+x["text"]
				if x["id"] == "_pass": self.error_passwordconfirm.setVisible(True); text = xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7116)+"\n"+x["text"]
				xbmcgui.Dialog().ok(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7117), '',text,'')
		elif response["response"] == "success":
			# Save login information into addon settings
			gd.selfAddon.setSetting("hqusername",data_dict["username"])
			gd.selfAddon.setSetting("hqpassword",data_dict["password"])
			self.username_textbox.setText(data_dict["username"])
			self.password_textbox.setText(data_dict["password"])
			#xbmcgui.Dialog().ok(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8023), '',xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8024),'')

                        pDialog = xbmcgui.DialogProgress()
                        pDialog.create(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8023), '',xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8024),data_dict['email'])
                        TOTAL = 100
                        COUNTDOWN_TIME = 15
                        pDialog.update(TOTAL)
                        division = float(100)/float(COUNTDOWN_TIME)
                        
                        while COUNTDOWN_TIME > 0:
                                TOTAL -= division
                                COUNTDOWN_TIME -= 1
                                pDialog.update(int(TOTAL))
                                xbmc.sleep(1000)
                        pDialog.close()
			self.winset = 1
			self.setWinState()
			"""
			if gd.selfAddon.getSetting("autologin").lower() == "true":
				time.sleep(.5)
				self.handler_loginresponse()
			else:
				self.winset = 1
				self.setWinState()
			"""
		else:
			xbmcgui.Dialog().ok(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7117), '','unknown error','')

	def handler_loginresponse(self):
		username = self.username_textbox.getText()
		password = self.password_textbox.getText()
		if gd.selfAddon.getSetting("autologin").lower() == "true":
			gd.selfAddon.setSetting("hqusername",username)
			gd.selfAddon.setSetting("hqpassword",password)
		else:
			gd.selfAddon.setSetting("hqusername",'')
			gd.selfAddon.setSetting("hqpassword",'')
		gd.get3Settings()
		self.busy = True
		self.imgBusyOuter.setVisible(True)
		time.sleep(.5)
		data = []
		data_dict = {}
		data_dict["username"] = username
		data_dict["password"] = password
		data.append(data_dict)
		response = send2remote(mode="signin", data=data)
		time.sleep(.5)
		self.imgBusyOuter.setVisible(False)
		self.busy = False
		print "handler_loginresponse"
		print "response:" + str(response)
		if response["response"] == "errors":
			for x in response["errors"]:
				xbmcgui.Dialog().ok(xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(7118), '',x["text"],'')
		elif response["response"] == "success":
			self.playlisturl = response["url"]
			self.close()
	
	def onAction(self, action):
		if action == ACTION_PREVIOUS_MENU or action == ACTION_BACK:
			choice = xbmcgui.Dialog().yesno('Close XBMC/Kodi', xbmcaddon.Addon(id=gd.addon_id).getLocalizedString(8015), nolabel='No, Cancel',yeslabel='Yes, Close')
			if choice is 1:
				xbmc.executebuiltin('XBMC.shutdown()')#self.close()
	

	def onControl(self, control):
		if control == self.new_acct_button:
			if not self.busy:
				self.winset = 2
				self.setWinState()
		if control == self.cancel_signup_button:
			if not self.busy:
				self.winset = 1
				self.first_name_textbox.setText("First Name")
				self.last_name_textbox.setText("Last Name")
				self.create_email_textbox.setText("Email ID")
				self.create_username_textbox.setText("Choose Name")
				self.setWinState()
		#if control == self.submit_signup_button:
		#	if not self.busy:
		#		if self.checkvalidform():
		#			self.handler_signupresponse()
		if control == self.submit_signup_button:
			if not self.busy:
				if self.checkvalidform(True):
					self.handler_signupresponseTrial()
		if control == self.login_button:
			if not self.busy:
				self.handler_loginresponse()
		#if control == self.autologin_toggle_button:
			#if not self.busy:
				#if gd.selfAddon.getSetting("autologin").lower() == "true":
					#self.autologin_toggle_button.setSelected(False)
					#gd.selfAddon.setSetting("autologin","false")
				#else:
					#self.autologin_toggle_button.setSelected(True)
					#gd.selfAddon.setSetting("autologin","true")

	
	def onFocus(self, controlId):
		print "onFocus::::"
		if controlId == self.first_name_textbox:
			if self.first_name_textbox.getText() is 'FIRST NAME':
				self.first_name_textbox.setText('')
		elif controlId == self.last_name_textbox:
			if self.last_name_textbox.getText() is 'LAST NAME':
				self.last_name_textbox.setText('')
		elif controlId == self.create_username_textbox:
			if self.create_username_textbox.getText() is 'CHOOSE A USER NAME':
				self.create_username_textbox.setText('')
		elif controlId == self.create_email_textbox:
			if self.create_email_textbox.getText() is 'YOUE EMAIL ADDRESS':
				self.create_email_textbox.setText('')
		elif controlId == self.create_password_textbox:
			if self.create_password_textbox.getText() is 'PASSWORD':
				self.create_password_textbox.setText('')
		elif controlId == self.confirm_password_textbox:
			if self.confirm_password_textbox.getText() is 'CONFIRM YOUR PASSWORD':
				self.confirm_password_textbox.setText('')

		if self.first_name_textbox.getText() is '':
			self.first_name_textbox.setText('FIRST NAME')
		if self.last_name_textbox.getText() is '':
			self.last_name_textbox.setText('LAST NAME')
		if self.create_username_textbox.getText() is '':
			self.create_username_textbox.setText('CHOOSE A USER NAME')
		if self.create_email_textbox.getText() is '':
			self.create_email_textbox.setText('YOUE EMAIL ADDRESS')
		if self.create_password_textbox.getText() is '':
			self.create_password_textbox.setText('PASSWORD')
		if self.confirm_password_textbox.getText() is '':
			self.confirm_password_textbox.setText('CONFIRM YOUR PASSWORD')
	

def send2remote(mode="openaddon", data=[]):
	url = gd.BASE_URL+"/iptv-api2.php"
	if mode == "openaddon":
		post_data = {}
		post_data["openaddon"] = ''
		response = gd.net.http_POST(url,post_data)
		try:
                        return json.loads(response.content)
		except:
                        return {"response": "errors", "errors": []}
	if mode == "signup":
		post_data = {}
		post_data["signup"]   = ''
		post_data["username"] = data[0]["username"]
		post_data["password"] = data[0]["password"]
		post_data["email"]	= data[0]["email"]
		post_data["fname"]	= data[0]["fname"]
		post_data["lname"]	= data[0]["lname"]
		post_data["coupon"]   = data[0]["coupon"]
		print post_data
		response = gd.net.http_POST(url,post_data)
		print "Returned response from server:"+response.content
		try:
			return json.loads(response.content)
		except:
			return {"response": "errors", "errors": []}
	if mode == "signuptrial":
		post_data = {}
		post_data["signup"]   = ''
		post_data["username"] = data[0]["username"]
		post_data["password"] = data[0]["password"]
		post_data["email"]	= data[0]["email"]
		post_data["fname"]	= data[0]["fname"]
		post_data["lname"]	= data[0]["lname"]
		post_data["trial"]   = ''
		print post_data
		response = gd.net.http_POST(url,post_data)
		print "Returned response from server:"+response.content
		try:
			return json.loads(response.content)
		except:
			return {"response": "errors", "errors": []}
	if mode == "signin":
		post_data = {}
		post_data["signin"]   = ''
		post_data["username"] = data[0]["username"]
		post_data["password"] = data[0]["password"]
		response = gd.net.http_POST(url,post_data)
		print "Returned response from server:"+response.content
		try:
			return json.loads(response.content)
		except:
			return {"response": "errors", "errors": []}
	return


