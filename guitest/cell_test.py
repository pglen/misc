#!/usr/bin/env python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

class CellRendererProgressWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="CellRendererProgress Example")

        self.set_default_size(200, 200)

        self.liststore = Gtk.ListStore(str, int, bool, str)

        self.current_iter = \
        self.liststore.append(["Sabayon", 0, False, ""])
        self.liststore.append(["Zenwalk", 0, False, ""])
        self.liststore.append(["SimplyMepis", 0, False, ""])

        treeview = Gtk.TreeView(model=self.liststore)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Text", renderer_text, text=0)
        treeview.append_column(column_text)

        renderer_progress = Gtk.CellRendererProgress()
        column_progress = Gtk.TreeViewColumn("Progress", renderer_progress,
            value=1, inverted=2)
        treeview.append_column(column_progress)

        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_inverted_toggled)
        column_toggle = Gtk.TreeViewColumn("Inverted", renderer_toggle,
            active=2)
        treeview.append_column(column_toggle)

        #renderer_pixbuf = Gtk.CellRendererPixbuf()
        #column_pixbuf = Gtk.TreeViewColumn("Image", renderer_pixbuf, icon_name=2)
        #treeview.append_column(column_pixbuf)

        manufacturers = ["Sony", "LG",
            "Panasonic", "Toshiba", "Nokia", "Samsung"]
        self.liststore_manufacturers = Gtk.ListStore(str)
        for item in manufacturers:
            self.liststore_manufacturers.append([item])

        renderer_combo = Gtk.CellRendererCombo()
        renderer_combo.set_property("editable", True)
        renderer_combo.set_property("model", self.liststore_manufacturers)
        renderer_combo.set_property("text-column", 0)
        renderer_combo.set_property("has-entry", False)
        renderer_combo.connect("edited", self.on_combo_changed)

        column_combo = Gtk.TreeViewColumn("Combo", renderer_combo, text=3)
        treeview.append_column(column_combo)

        self.add(treeview)
        self.timeout_id = GLib.timeout_add(1000, self.on_timeout, None)

    def on_combo_changed(self, widget, path, text):
        self.liststore[path][3] = text

    def on_inverted_toggled(self, widget, path):
        self.liststore[path][2] = not self.liststore[path][2]

    def on_timeout(self, user_data):
        new_value = self.liststore[self.current_iter][1] + 1
        if new_value > 100:
            self.current_iter = self.liststore.iter_next(self.current_iter)
            if self.current_iter is None:
                self.reset_model()
            new_value = self.liststore[self.current_iter][1] + 1

        self.liststore[self.current_iter][1] = new_value
        return True

    def reset_model(self):
        for row in self.liststore:
            row[1] = 0
        self.current_iter = self.liststore.get_iter_first()

win = CellRendererProgressWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

