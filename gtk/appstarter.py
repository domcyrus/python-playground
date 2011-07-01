#!/usr/bin/env python
# Based on gtk docs. Just a file to play around with pygtk.

# This gtk app is just a gui to start some processes and
# setup the trackpoint.

import gtk
import os
import pygtk
import subprocess

class AppStarter(object):

  FIREFOX = "/usr/bin/firefox"
  THUNDERBIRD = "/usr/bin/thunderbird"

  def __init__(self, name):
    self._name = name

    # create a new window
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
    self.window.set_title(name)
    #self.window.resize(400,400)

    vbox = gtk.VBox(False, 0)
    vbox.set_border_width(2)
    frame = gtk.Frame(name)
    
    vbox.pack_start(frame, False, False, 3)
    frame.show()

    # When the window is given the "delete_event" signal (this is given
    # by the window manager, usually by the "close" option, or on the
    # titlebar), we ask it to call the delete_event () function
    # as defined above. The data passed to the callback
    # function is NULL and is ignored in the callback function.
    self.window.connect("delete_event", self.delete_event)

    # Here we connect the "destroy" event to a signal handler.
    # This event occurs when we call gtk_widget_destroy() on the window,
    # or if we return FALSE in the "delete_event" callback.
    self.window.connect("destroy", self.destroy)

    # Sets the border width of the window.
    self.window.set_border_width(10)

    # Creates a new button with the label "Hello World".
    button_track = gtk.Button("Setup Trackpoint")

    # When the button receives the "clicked" signal, it will call the
    button_track.connect("clicked", self.SetupTrackpoint, None)

    button_close = gtk.Button("Close")
    # This will cause the window to be destroyed by calling
    # gtk_widget_destroy(window) when "clicked".  Again, the destroy
    # signal could come from here, or the window manager.
    button_close.connect_object("clicked", gtk.Widget.destroy, self.window)

    button_fire = gtk.Button("Start Firefox")
    button_fire.connect("clicked", self.StartFirefox, None)

    button_thunder = gtk.Button("Start Thunderbird")
    button_thunder.connect("clicked", self.StartThunderbird, None)

    # This packs the button into the window (a GTK container).
    vbox.pack_start(button_track, False, False, 3)
    vbox.pack_start(button_fire, False, False, 3)
    vbox.pack_start(button_thunder, False, False, 3)
    vbox.pack_start(button_close, False, False, 3)
    self.window.add(vbox)


    # The final step is to display this newly created widget.
    for button in [button_fire, button_track, button_thunder, button_close]:
      button.show()
    vbox.show()

    # and the window
    self.window.show()

  def SetupTrackpoint(self, widget, data=None):
    print "Setup Trackpoint."
    home_dir = os.environ['HOME']
    trackpoint = os.path.join(home_dir, 'bin', 'trackpoint.sh')
    print "trackpoint: %s" % trackpoint
    self._starter([trackpoint])

  def StartFirefox(self, widget, data=None):
    print "Start firefox."
    self._starter([self.FIREFOX, '&'])

  def StartThunderbird(self, widget, data=None):
    print "Start thunderbird."
    self._starter([self.THUNDERBIRD])

  def delete_event(self, widget, event, data=None):
    # If you return FALSE in the "delete_event" signal handler,
    # GTK will emit the "destroy" signal. Returning TRUE means
    # you don't want the window to be destroyed.
    # This is useful for popping up 'are you sure you want to quit?'
    # type dialogs.
    print "delete event occurred"

    # Change FALSE to TRUE and the main window will not be destroyed
    # with a "delete_event".
    return False

  # Another callback
  def destroy(self, widget, data=None):
    gtk.main_quit()

  def main(self):
    # All PyGTK applications must have a gtk.main(). Control ends here
    # and waits for an event to occur (like a key press or mouse event).
    gtk.main()

  # private helper methods.
  def _starter(self, cmd):
    print "".join(cmd)
    p = subprocess.Popen(cmd, close_fds=True)

def main():
  app_starter = AppStarter('Hello %s!' % os.environ['USER'])
  app_starter.main()

if __name__ == "__main__":
  main()

