#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import gi
import threading
import random
import glob 

gi.require_version("Gtk", "3.0")
import time

from gi.repository import Gtk, GLib, Gdk, GObject
import logging
import string 

ret1 = int(time.strftime("%H%M%S", time.localtime()))

class BackupGuiObject(Gtk.Window):
    WIDTH, HEIGHT = 840, 472
    def __init__(self):
	super(BackupGuiObject, self).__init__()
	self.set_title("")
	self.set_decorated(False)
	self.set_size_request(self.WIDTH, self.HEIGHT)
	self.move((Gdk.Screen.width() - self.WIDTH) / 2, (Gdk.Screen.height() - self.HEIGHT) / 2)

class G_SELECTED_BK(object):
    i = 0
g_selected_bk = G_SELECTED_BK()


class PyApp(BackupGuiObject):
    def __init__(self):
	super(PyApp, self).__init__()
	self.select_bk = g_selected_bk.i
        if self.select_bk == 0:
            button1 = Gtk.RadioButton.new_with_label_from_widget(None, "")
            button2 = Gtk.RadioButton.new_with_label_from_widget(button1, "")
            button3 = Gtk.RadioButton.new_with_label_from_widget(button2, "")
        elif self.select_bk == 1:
            button2 = Gtk.RadioButton.new_with_label_from_widget(None, "")
            button1 = Gtk.RadioButton.new_with_label_from_widget(button2, "")
            button3 = Gtk.RadioButton.new_with_label_from_widget(button1, "")
        elif self.select_bk == 2:
            button3 = Gtk.RadioButton.new_with_label_from_widget(None, "")
            button1 = Gtk.RadioButton.new_with_label_from_widget(button3, "")
            button2 = Gtk.RadioButton.new_with_label_from_widget(button1, "")

        button1.connect("clicked", self.on_clicked_backup)
        button2.connect("clicked", self.on_clicked_restore)
        button3.connect("clicked", self.on_clicked_stamper)
	
	ok = Gtk.Button()
	ok.set_size_request(100, 37)
	image1 = Gtk.Image.new_from_file(os.path.join(os.path.dirname(__file__), "/usr/share/anaconda/pixmaps/next.png"))
	ok.set_image(image1)
	ok.connect("clicked", self.on_clicked_ok)

	quit = Gtk.Button()
	image2 = Gtk.Image.new_from_file(os.path.join(os.path.dirname(__file__), "/usr/share/anaconda/pixmaps/quit.png"))
	quit.set_image(image2)
	quit.connect("clicked", self.on_clicked_quit)
	quit.set_size_request(100, 37)

	img1 = Gtk.Image()
	img1.set_from_file("/usr/share/anaconda/pixmaps/main.jpg")

	fixed = Gtk.Fixed()
	fixed.put(img1, 0 , 0)
	fixed.put(ok, 570, 395)
	fixed.put(quit, 690, 395)
	fixed.put(button1, 489, 199)
	fixed.put(button2, 489, 250)
        fixed.put(button3, 489, 300)
	self.connect("destroy", Gtk.main_quit)
	self.add(fixed)
	self.show_all()

    def on_destroy(self, widget):
	Gtk.main_quit()

    def on_clicked_backup(self, widget):
	g_selected_bk.i = 0
	self.select_bk = 0
    def on_clicked_restore(self, widget):
	g_selected_bk.i = 1
	self.select_bk = 1
    def on_clicked_stamper(self,widget):
	g_selected_bk.i = 2
        self.select_bk = 2

    def on_clicked_quit(self, widget):
	Gtk.main_quit()
	os.system("reboot")
	
    def on_clicked_ok(self, widget):
	if self.select_bk == 0:
            Gtk.Widget.hide(self)
	    Backup()
	elif self.select_bk == 1:
            Gtk.Widget.hide(self)
	    Restore()
        elif self.select_bk == 2:
	    backup_dev = os.popen(r"df |grep '/$' |awk -F ' ' '{print $1}'", "r")
            dev = backup_dev.read()[:-2]
            if (os.path.exists("/sys/firmware/efi")):
                home_dev = dev + '6'
            else:
                home_dev = dev + '5'
            os.system("mkdir /mnt/home_dev ; mount " + home_dev + " /mnt/home_dev")
            cmd = "df |grep " + home_dev + " |awk -F ' ' '{print $3}'"
            Total = os.popen(cmd)

            size = int(Total.read())
	    os.system("umount /mnt/root_dev; rmdir /mnt/root_dev")

            if size >= 2097152: 
                dialog = DialogWarn_size(self)
                response = dialog.run()
                if response == Gtk.ResponseType.CANCEL:
                    dialog.destroy()
            else:
                dialog = DialogWarn3(self)
                response = dialog.run()
                if response == Gtk.ResponseType.OK:
                    Gtk.Widget.hide(self)
                    ProgressBarStamper()
                dialog.destroy()

class Backup(BackupGuiObject):
    def __init__(self):
        super(Backup, self).__init__()

        fixed = Gtk.Fixed()

       	main_vbox = Gtk.VBox(False, 8)
        main_vbox.set_size_request(755, 370)
	self.add(fixed)

	scw= Gtk.ScrolledWindow()
	main_vbox.pack_start(scw, True, True, 0)
	
	store = self.create_model()

        tree = Gtk.TreeView(store)
	
	tree.connect("row-activated", self.on_node_selected)
        scw.add(tree)
	
	self.create_columns(tree)
	self.statusbar = Gtk.Statusbar()
	main_vbox.pack_start(self.statusbar, True, True, 0)	

	btn_ok = Gtk.Button()
	img_next = Gtk.Image.new_from_file(os.path.join(os.path.dirname(__file__), "/usr/share/anaconda/pixmaps/next.png"))
        btn_ok.set_image(img_next)
	btn_ok.connect("clicked", self.on_clicked_ok)
	btn_ok.set_size_request(100, 37)
	btn_cal = Gtk.Button()
	img_last = Gtk.Image.new_from_file(os.path.join(os.path.dirname(__file__), "/usr/share/anaconda/pixmaps/last.png"))
        btn_cal.set_image(img_last)
	btn_cal.connect("clicked", self.on_clicked_cal)
	btn_cal.set_size_request(100, 37)


	img2 = Gtk.Image()
        img2.set_from_file("/usr/share/anaconda/pixmaps/backup.jpg")

        fixed.put(img2, 0 , 0)
	fixed.put(main_vbox, 45, 85)
        fixed.put(btn_cal, 570, 395)
        fixed.put(btn_ok, 690, 395)
        self.connect("destroy", Gtk.main_quit)

        self.show_all()	
              
    def on_clicked_ok(self, widget):
        dialog = DialogWarn(self)
        response = dialog.run()
	if response == Gtk.ResponseType.OK:
	    print("The OK button was clicked")
            Gtk.Widget.hide(self)
            ProgressBarBackup()
        dialog.destroy()

    def on_clicked_cal(self, widget):
	Gtk.Widget.hide(self)
	PyApp()
    def create_columns(self, tree):
        res = Gtk.TreeViewColumn()
        res.set_title("备份节点")

        cell = Gtk.CellRendererText()
        res.pack_start(cell, True)
        res.add_attribute(cell, "text", 0)

        tree.append_column(res)
  
    def create_model(self):
        store = Gtk.ListStore(str)

        f = os.popen(r"ls /backup", "r")
        str_file = f.read()[:-1]
        file_lst = str_file.split('\n')
        for d in file_lst:
            store.append([d])
        return store

    def on_node_selected(self, widget, row, col):
        model = widget.get_model()

class Restore(BackupGuiObject):
    def __init__(self):
        super(Restore, self).__init__()
#	first_model = os.popen(r"ls /backup |awk -F ' ' '{print $1}' |awk 'NR==1{print}'", "r")
#        self.selected_model = first_model.read()[-1]
	
	self.file_lst = []
	fixed = Gtk.Fixed()

        main_vbox = Gtk.VBox(False, 8)
	main_vbox.set_size_request(750, 200)
	self.add(fixed)
	scw= Gtk.ScrolledWindow()
	main_vbox.pack_start(scw, True, True, 0)
	
	store = self.create_model()
#        tree = Gtk.TreeView(activate_on_single_click=True)
        tree = Gtk.TreeView(store)
#	tree.connect("row-activated", self.on_node_selected)
#	tree.set_model(store)
	tree.set_rules_hint(True)
        scw.add(tree)
	
	self.create_columns(tree)
	self.statusbar = Gtk.Statusbar()
	main_vbox.pack_start(self.statusbar, True, True, 0)	

	btn_ok = Gtk.Button()
	btn_ok.connect("clicked", self.on_clicked_ok, tree)
	btn_ok.set_size_request(100, 37)
	img_next = Gtk.Image.new_from_file(os.path.join(os.path.dirname(__file__), "/usr/share/anaconda/pixmaps/next.png"))
	btn_ok.set_image(img_next)	

	btn_del = Gtk.Button()
	btn_del.connect("clicked", self.on_clicked_del, tree)
	btn_del.set_size_request(100, 37)
	img_del = Gtk.Image.new_from_file(os.path.join(os.path.dirname(__file__), "/usr/share/anaconda/pixmaps/remove.png"))
	btn_del.set_image(img_del)
   
 	btn_cal = Gtk.Button()
	btn_cal.connect("clicked", self.on_clicked_cal)
	btn_cal.set_size_request(100, 37)
	img_last = Gtk.Image.new_from_file(os.path.join(os.path.dirname(__file__), "/usr/share/anaconda/pixmaps/last.png"))
	btn_cal.set_image(img_last)

        img3 = Gtk.Image()
        img3.set_from_file("/usr/share/anaconda/pixmaps/restore.jpg")

        fixed.put(img3, 0 , 0) 
        fixed.put(main_vbox, 46, 84)
	fixed.put(btn_ok, 570, 395)
	fixed.put(btn_del, 690, 395)
	fixed.put(btn_cal, 450, 395)
	self.activity_mode = True

        self.connect("destroy", Gtk.main_quit)

        self.show_all()
    def create_columns(self, tree):
        res = Gtk.TreeViewColumn()
        res.set_title("备份节点")

        cell = Gtk.CellRendererText()
        res.pack_start(cell, True)
        res.add_attribute(cell, "text", 0)

        tree.append_column(res)

    def create_model(self):
	store = Gtk.ListStore(str)
        f = os.popen(r"ls /backup", "r")
        str_file = f.read()[:-1]
        self.file_lst = str_file.split('\n')
        for d in self.file_lst:
            store.append([d])
	return store

#    def on_node_selected(self, widget, row, col):
#	model = widget.get_model()
#	self.selected_model = model[row][0]

    def on_clicked_ok(self, button, treeview):
	path_files = glob.glob('/backup/*')

        selection = treeview.get_selection()
        model, iter = selection.get_selected()
        if iter:
            m_path = model.get_path(iter)[0]
            print "path :%s", m_path
            selected_model = self.file_lst[m_path]
            print "selected_model: %s", selected_model
        else:
            selected_model = self.file_lst[0]


        if len(path_files) == 0 :
            dialog = DialogWarn_err(self)
            response = dialog.run()
        else:
	    if selected_model == "backup.fsa":
		dialog = DialogWarn4(self)
        	response = dialog.run()
	    else:
		dialog = DialogWarn1(self)
		response = dialog.run()

            if response == Gtk.ResponseType.OK:
                print("The OK button was clicked")
                Gtk.Widget.hide(self)
		ProgressBarRestore(selected_model)
        dialog.destroy()

    def on_clicked_del(self, button, treeview):
        path_files = glob.glob('/backup/*')

        selection = treeview.get_selection()
        model, iter = selection.get_selected()
        if iter:
            m_path = model.get_path(iter)[0]
            print "path :%s", m_path
            selected_model = self.file_lst[m_path]
            print "selected_model: %s", selected_model
        else:
            selected_model = self.file_lst[0]


        if len(path_files) == 0 :
            dialog = DialogWarn_err(self)
            response = dialog.run()
        else:
	    if selected_model == "backup.fsa":
		dialog = DialogWarn_err2(self)
        	response = dialog.run()
	    else:
        	dialog = DialogWarn2(self)
        	response = dialog.run()
        	path = "/backup"

		if response == Gtk.ResponseType.OK:
                    os.remove(path+'/'+selected_model)
		    dialog.destroy()
		    Restore()
        dialog.destroy()

    def on_clicked_cal(self, widget):
	Gtk.Widget.hide(self)
	PyApp()	

class DialogwarnGuiObject(Gtk.Dialog):
    def __init__(self):
        self.set_default_size(150, 100)
        self.set_decorated(False)
        provider = Gtk.CssProvider()
        css = """
           button{font-size:11px;background: #0073dd;color:#ebedf5;box-shadow:0 0 2px white;}
           button:hover{font-weight:bold;background: #3888ef;color:#ebedf5;box-shadow:0 0 2px white;}
           button:active{font-weight:bold;background: #3888ef;color:#66a7e2;box-shadow:0 0 3px white ;}
           dialog {background: #ebedf5;box-shadow:0 0 20px #000;}
        """
        # css = """
        #    button {background: transparent}
        #    dialog {background: transparent}
        # """
        provider.load_from_data(bytes(css.encode()));
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider,
                                                 Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


class DialogWarn(DialogwarnGuiObject):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "确认操作？", parent, 0,
            #(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            # Gtk.STOCK_OK, Gtk.ResponseType.OK))
            ("取消", Gtk.ResponseType.CANCEL,
             "确定", Gtk.ResponseType.OK))
	super(DialogWarn, self).__init__()
	path_files = glob.glob('/backup/*')
	if len(path_files) == 2 :
            label = Gtk.Label("备份功能会有数据风险，\n请谨慎操作。\n该操作将覆盖最近一次备份，\n确认继续系统备份？")
	else:
            label = Gtk.Label("备份功能会有数据风险，\n请谨慎操作。\n确认系统备份？")
        box = self.get_content_area()
        box.add(label)
        self.show_all()

class DialogWarn1(DialogwarnGuiObject):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "确认操作？", parent, 0,
            ("取消", Gtk.ResponseType.CANCEL,
             "确定", Gtk.ResponseType.OK))
	super(DialogWarn1, self).__init__()

        label = Gtk.Label("还原操作可能会丢失用户\n数据，确认系统还原？")
     
	box = self.get_content_area()
        box.add(label)
        self.show_all()

class DialogWarn2(DialogwarnGuiObject):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "确认操作", parent, 0,
            ("取消", Gtk.ResponseType.CANCEL,
             "确定", Gtk.ResponseType.OK))
	super(DialogWarn2, self).__init__()
        label = Gtk.Label("\n确认删除此备份节点？")
     
	box = self.get_content_area()
        box.add(label)
        self.show_all()

class DialogWarn_err(DialogwarnGuiObject):
    def __init__(self, parent):
        dlg = Gtk.Dialog.__init__(self, "确认操作？", parent, 0,
                                  ("取消", Gtk.ResponseType.CANCEL))
        super(DialogWarn_err, self).__init__()

        label = Gtk.Label("\n  没有备份节点  \n  请先做系统备份!")
        box = self.get_content_area()
        box.add(label)
        self.show_all()

class DialogWarn_err2(DialogwarnGuiObject):
    def __init__(self, parent):
        dlg = Gtk.Dialog.__init__(self, "确认操作？", parent, 0,
                                  ("取消", Gtk.ResponseType.CANCEL))
        super(DialogWarn_err2, self).__init__()

        label = Gtk.Label("\n  初始化备份文件  \n  请勿删除!")
        box = self.get_content_area()
        box.add(label)
        self.show_all()

class DialogWarn3(DialogwarnGuiObject):
    def __init__(self, parent):
        dlg = Gtk.Dialog.__init__(self, "确认操作？", parent, 0,
            ("取消", Gtk.ResponseType.CANCEL,
             "确定", Gtk.ResponseType.OK))
	super(DialogWarn3, self).__init__()

        path_files = glob.glob('/NeoKylin-*')
        if len(path_files) >= 1 :
            label = Gtk.Label("\n该操作将覆盖最近制作的母盘，\n  确认继续制作母盘？")
        else:
            label = Gtk.Label("\n确认制作母盘？")
        box = self.get_content_area()
        box.add(label)
        self.show_all()

class DialogWarn4(DialogwarnGuiObject):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "确认操作", parent, 0,
            ("取消", Gtk.ResponseType.CANCEL,
             "确定", Gtk.ResponseType.OK))
	super(DialogWarn4, self).__init__()

        label = Gtk.Label("\n确认初始化恢复操作？ \n用户数据可能会丢失。")
     
	box = self.get_content_area()
        box.add(label)
        self.show_all()

class DialogWarn_size(DialogwarnGuiObject):
    def __init__(self, parent):
        dlg = Gtk.Dialog.__init__(self, "确认操作？", parent, 0,
            ("取消", Gtk.ResponseType.CANCEL))

	super(DialogWarn_size, self).__init__()
        label = Gtk.Label("\n   /home分区下数据过大，  \n无法继续制作母盘!")
        box = self.get_content_area()
        box.add(label)
        self.show_all()


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
        img_bar.set_from_file("/usr/share/anaconda/pixmaps/completed.jpg")

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

class ProgressBarBackup(BackupGuiObject):
    def __init__(self):
	super(ProgressBarBackup, self).__init__()
#        self.set_border_width(5)
        self.table = Gtk.Table(10, 10, True)

	fixed = Gtk.Fixed()
	vbox = Gtk.VBox(False, 3)
        vbox.set_size_request(700, 10)
	
        img_bar = Gtk.Image()
        img_bar.set_from_file("/usr/share/anaconda/pixmaps/Bar-backup.jpg")


	self.ret = 1
	ret1 = int(time.strftime("%H%M%S", time.localtime()))
	print("{0}", ret1)
        self.t_beg = ((ret1/10000*3600)+(((ret1/100)%100)*60)+(ret1%100))

        self.set_size_request(self.WIDTH, self.HEIGHT)
        self.move((Gdk.Screen.width() - self.WIDTH) / 2, (Gdk.Screen.height() - self.HEIGHT) / 2)
        self.label2 = Gtk.Label()
	self.label2.modify_fg(Gtk.StateType.NORMAL,Gdk.color_parse("white"))
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
       
	########get root dev, calculate the size of root
	backup_dev = os.popen(r"df |grep '/$' |awk -F ' ' '{print $1}'", "r")
	dev = backup_dev.read()[:-2]
	if (os.path.exists("/sys/firmware/efi")):
	    root_dev = dev + '4'
	else:
	    root_dev = dev + '1'
	os.system("mkdir /mnt/root_dev ; mount " + root_dev + " /mnt/root_dev")
	cmd = "df |grep " + root_dev + " |awk -F ' ' '{print $3}'"
	Total = os.popen(cmd)
	
        self.t = int(Total.read())*2
	os.system("umount /mnt/root_dev; rmdir /mnt/root_dev")
        
        self.ret = os.system("/usr/bin/backup.sh >  /tmp/backup.log 2>&1 &")

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

class ProgressBarRestore(BackupGuiObject):
    def __init__(self, rst_file):
	super(ProgressBarRestore, self).__init__()
#        self.set_border_width(5)
        self.table = Gtk.Table(10, 10, True)

        fixed = Gtk.Fixed()
        vbox = Gtk.VBox(False, 3)
        vbox.set_size_request(700, 10)

        img_bar = Gtk.Image()
        img_bar.set_from_file("/usr/share/anaconda/pixmaps/Bar-restore.jpg")

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
#        label3 = Gtk.Label()

        self.progressbar = Gtk.ProgressBar()
        self.progressbar.set_size_request(740, 30)
        vbox.pack_start(self.progressbar, True, True, 0)

        fixed.put(img_bar, 0 , 0)
        fixed.put(vbox, 50 , 368)
        fixed.put(self.label2, 125 , 321)
        fixed.put(self.label4, 475 , 321)
        self.activity_mode = True

        ########get root dev, calculate the size of root
        backup_dev = os.popen(r"df |grep '/$' |awk -F ' ' '{print $1}'", "r")
        dev = backup_dev.read()[:-2]
        if (os.path.exists("/sys/firmware/efi")):
            root_dev = dev + '4'
        else:
            root_dev = dev + '1'
	os.system("mkdir /mnt/root_dev ; mount " + root_dev + " /mnt/root_dev")
        cmd = "df |grep " + root_dev + " |awk -F ' ' '{print $3}'"
        Total = os.popen(cmd)

        self.t = int(Total.read())*1
	os.system("umount /mnt/root_dev; rmdir /mnt/root_dev")
        self.ret = os.system("/usr/bin/restore.sh "+rst_file+" > /tmp/restore.log 2>&1 &")
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

class ProgressBarStamper(BackupGuiObject):
    def __init__(self):
	super(ProgressBarStamper, self).__init__()
#        self.set_border_width(5)
        self.table = Gtk.Table(10, 10, True)

        fixed = Gtk.Fixed()
        vbox = Gtk.VBox(False, 3)
        vbox.set_size_request(700, 10)

        img_bar = Gtk.Image()
        img_bar.set_from_file("/usr/share/anaconda/pixmaps/Bar-stamper.jpg")

        self.ret = 1
        ret1 = int(time.strftime("%H%M%S", time.localtime()))
        print("{0}", ret1)
        self.t_beg = ((ret1/10000*3600)+(((ret1/100)%100)*60)+(ret1%100))

        self.label2 = Gtk.Label()
        self.label2.modify_fg(Gtk.StateType.NORMAL,Gdk.color_parse("white"))
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

        ########get root dev, calculate the size of root
        backup_dev = os.popen(r"df |grep '/$' |awk -F ' ' '{print $1}'", "r")
        dev = backup_dev.read()[:-2]
        if (os.path.exists("/sys/firmware/efi")):
            root_dev = dev + '4'
        else:
            root_dev = dev + '1'
	os.system("mkdir /mnt/root_dev ; mount " + root_dev + " /mnt/root_dev")
        cmd = "df |grep " + root_dev + " |awk -F ' ' '{print $3}'"
        Total = os.popen(cmd)

        self.t = int(Total.read())*3
	os.system("umount /mnt/root_dev; rmdir /mnt/root_dev")
        self.ret = os.system("/usr/bin/mkiso.sh >/tmp/mkiso.log 2>&1 &")

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


pyapp = PyApp()
pyapp.show_all()
Gtk.main()
