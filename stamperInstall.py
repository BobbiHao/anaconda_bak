#!/usr/bin/python
# -*- coding: UTF-8 -*-

import gi
import os
import time
import threading
import random

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

ret1 = int(time.strftime("%H%M%S", time.localtime()))

class BackupGuiObject(Gtk.Window):
    WIDTH, HEIGHT = 840, 472
    def __init__(self):
        super(BackupGuiObject, self).__init__()
        self.set_title("")
        self.set_decorated(False)
        self.set_size_request(self.WIDTH, self.HEIGHT)
        self.move((Gdk.Screen.width() - self.WIDTH) / 2, (Gdk.Screen.height() - self.HEIGHT) / 2)


class Stamper(BackupGuiObject):
    def __init__(self):
	super(Stamper, self).__init__()
	self.state = 'n'
         
	fixed = Gtk.Fixed()

        self.button1 = Gtk.CheckButton.new_with_label("")
#        self.button1.connect("toggled", self.on_button_toggled)

        button2 = Gtk.Button()
        button2.set_size_request(100, 37)
	button2.connect("clicked", self.on_clicked)
        img_btn2 = Gtk.Image.new_from_file(os.path.join(os.path.dirname(__file__), "/usr/share/anaconda/pixmaps/start-install.png"))
        button2.set_image(img_btn2)

        button3 = Gtk.Button()
        button3.set_size_request(100, 37)
        button3.connect("clicked", self.on_clicked_reboot)
        img_btn3 = Gtk.Image.new_from_file(os.path.join(os.path.dirname(__file__), "/usr/share/anaconda/pixmaps/quit.png"))
        button3.set_image(img_btn3) 

        img_bar = Gtk.Image()
        img_bar.set_from_file("/usr/share/anaconda/pixmaps/stamper-install.jpg")

        fixed.put(img_bar, 0 , 0)
#        fixed.put(label, 10, 100)
        fixed.put(button3, 570, 395)
        fixed.put(button2, 690, 395)
        fixed.put(self.button1, 56, 199)
        self.connect("destroy", Gtk.main_quit)

        self.add(fixed)
        self.show_all()

    def on_clicked(self, widget):
	if self.button1.get_active():
	    self.state = 'y'
	else:
	    self.state = 'n'
	Gtk.Widget.hide(self)
	ProgressBarWindow(self.state)
    def on_clicked_reboot(self, widget):
        os.system("reboot")
   
class ProgressBarWindow(BackupGuiObject):
    def __init__(self, state):
	super(ProgressBarWindow, self).__init__()
#        self.set_border_width(10)
        self.table = Gtk.Table(10, 10, True)

        fixed = Gtk.Fixed()
        vbox = Gtk.VBox(False, 3)
        vbox.set_size_request(700, 10)

        img_bar = Gtk.Image()
        img_bar.set_from_file("/usr/share/anaconda/pixmaps/Bar-stam-ins.jpg")

        self.ret = 1
        ret1 = int(time.strftime("%H%M%S", time.localtime()))
        print("{0}", ret1)
        self.t_beg = ((ret1/10000*3600)+(((ret1/100)%100)*60)+(ret1%100))

#        label1 = Gtk.Label()
        self.label2 = Gtk.Label()
        self.label2.modify_fg(Gtk.StateType.NORMAL,Gdk.color_parse("white"))
#        label3 = Gtk.Label()
        self.label4 = Gtk.Label()
        self.label4.modify_fg(Gtk.StateType.NORMAL,Gdk.color_parse("white"))

        self.progressbar = Gtk.ProgressBar()
	self.progressbar.set_size_request(740, 30)
        vbox.pack_start(self.progressbar, True, True, 0)

        fixed.put(img_bar, 0 , 0)
        fixed.put(vbox, 50 , 368)
        fixed.put(self.label2, 125 , 321)
        fixed.put(self.label4, 475 , 321)
        self.activity_mode = True

        cmd = "ls -l --block-size=K /run/initramfs/live/stamper*.fsa  | awk '{print $5}'"
        Total = os.popen(cmd)

        self.t = int(Total.read()[:-2])*10
	self.ret = os.system("/usr/bin/stamper-install.sh " + state + " &>/tmp/stamper.log &")
        print "进度条显示"
        self.timeout_id = GLib.timeout_add(1000, self.on_timeout, None)
        self.activity_mode = False

        self.add(fixed)
	self.connect("destroy", Gtk.main_quit)
        self.show_all()

    def on_timeout(self, user_data):
        """
        Update value on the progress bar     
        """

        if self.activity_mode:
            self.progressbar.pulse()
        else:
            ret2 = int(time.strftime("%H%M%S", time.localtime()))
            t_now = ((ret2/10000*3600)+(((ret2/100)%100)*60)+(ret2%100))
            ret3 = t_now-self.t_beg

            if ret3 >= 1 and ret3 <= self.t/19500:
                ret4 = random.randint((self.t/19500-ret3-5), self.t/19500-ret3+5)
                print("{0} {1} {2}".format(ret3/60,":",ret3%60))
                self.label2.set_text("{0} {1} {2}".format(ret3/60,":",ret3%60))
                self.label4.set_text("{0} {1} {2}".format(ret4/60,":",ret4%60))
            else:
                if self.progressbar.get_fraction() >= 1:
		    Gtk.Widget.hide(self)
                    ProgressBarWindow1()
                    return False
                else:
                    new_value = self.progressbar.get_fraction() + 0.1
                    self.progressbar.set_fraction(new_value)
                    #retrun False
            new_value = self.progressbar.get_fraction() + 1.000000/(self.t/19500)
            self.progressbar.set_fraction(new_value)

        return True

class ProgressBarWindow1(BackupGuiObject):
    def __init__(self):
	super(ProgressBarWindow1, self).__init__()
#        self.set_border_width(10)
        self.table = Gtk.Table(10, 10, True)

        fixed = Gtk.Fixed()

        fixed = Gtk.Fixed()
        vbox = Gtk.VBox(False, 3)
        vbox.set_size_request(700, 10)

        self.progressbar = Gtk.ProgressBar()
        vbox.pack_start(self.progressbar, True, True, 0)

        button1 = Gtk.Button()
        button1.set_size_request(100, 37)
        img_btn1 = Gtk.Image.new_from_file(os.path.join(os.path.dirname(__file__), "/usr/share/anaconda/pixmaps/reboot.png"))
        button1.set_image(img_btn1)

        button2 = Gtk.Button()
        button2.set_size_request(100, 37)
        img_btn2 = Gtk.Image.new_from_file(os.path.join(os.path.dirname(__file__), "/usr/share/anaconda/pixmaps/poweroff.png"))
        button2.set_image(img_btn2)

        button1.connect("clicked", self.on_clicked_reboot)
        button2.connect("clicked", self.on_clicked_poweroff)

        img_bar = Gtk.Image()
        img_bar.set_from_file("/usr/share/anaconda/pixmaps/com-stam-ins.jpg")

        fixed.put(img_bar, 0 , 0)
        fixed.put(button1, 570, 395)
        fixed.put(button2, 690, 395)

        self.activity_mode = True
        self.add(fixed)
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
    def on_clicked_reboot(self, widget):
        os.system("reboot")
    def on_clicked_poweroff(self, widget):
        os.system("poweroff")


win = Stamper()
win.show_all()
Gtk.main()
