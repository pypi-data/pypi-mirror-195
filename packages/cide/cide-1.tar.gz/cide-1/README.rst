README
######


**NAME**


``CIDE`` - mortality model of the netherlands during the 2020 genocide.


**SYNOPSIS**

::

 cide [<cmd>|-c|-d] [key=value] [key==value]


**DESCRIPTION**


``cide`` is a mortality model (deaths by disease) of the netherlands during
the genocide that took place in 2020. It has a IRC bot that can display
the cause of disease besides the every seconds/minutes/hours between each
deaths there are.

``cide`` has some other functionality, mostly feeding RSS feeds into a irc
channel. It can do some logging of txt and take note of things todo.


**INSTALL**


::

 $ sudo pip3 install cide


**CONFIGURATION**


configuration is done by calling the ``cfg`` command of ``cidec``


IRC

::

 $ cidec cfg server=<server> channel=<channel> nick=<nick>

 (*) default channel/server is #cide on localhost


SASL

::

 $ cidec pwd <nickservnick> <nickservpass>
 $ cidec cfg password=<outputfrompwd>


USERS

as default the user's userhost is not checked when a user types a command in a
channel. To enable userhost checking enable users with the ``cfg`` command::

 $ cidec cfg users=True


To add a user to the bot use the met command::

 $ cidec met <userhost>

to delete a user use the del command with a substring of the userhost::

 $ cidec del <substring>


RSS

::

 $ cidec rss <url>



**RUNNING**


this part shows how to run ``cidec``.


**cli**


without any arguments ``cidec`` doesn't respond, add arguments to have
``cidec`` execute a command::


 $ cidec
 $


the ``cmd`` command shows you a list of available commands::


 $ cidec cmd
 cfg,cmd,dlt,dpl,flt,fnd,ftc,met,mre,nme,pwd,rem,rss,thr,upt


**console**


use the ``cidec`` program to start the bot as a console::

 $ cide
 OPB started at Fri Jan 6 01:49:58 2023
 > cmd
 cfg,cmd,dlt,dpl,flt,ftc,krn,log,met,mre,nme,pwd,rem,rss,thr,upt
 >

running the bot in the background is done by starting ``cided``::

 $ cided
 $


**24/7**


24/7 and how todo that is still under discussion


**COMMANDS**


here is a short description of the commands::

 cfg - show the irc configuration, also edits the config
 cmd - show all commands
 dlt - remove a user
 dne - flag todo as done
 dpl - set display items for a rss feed
 flt - show a list of bot registered to the bus
 fnd - allow you to display objects on the datastore, read-only json files on disk 
 ftc - run a rss feed fetching batch
 log - log some text
 met - add a users with there irc userhost
 mre - displays cached output, channel wise.
 nme - set name of a rss feed
 pwd - combine a nickserv name/password into a sasl password
 rem - remove a rss feed by matching is to its url
 rss - add a feed to fetch, fetcher runs every 5 minutes
 thr - show the running threads
 tdo - adds a todo item, no options returns list of todo's
 upt - show uptime


**PROGRAMMING**


The ``cide`` package provides an Object class, that mimics a dict while using
attribute access and provides a save/load to/from json files on disk.
Objects can be searched with database functions and uses read-only files
to improve persistence and a type in filename for reconstruction. Methods are
factored out into functions to have a clean namespace to read JSON data into.

basic usage is this::

 >>> from cide.objects import Object
 >>> o = Object()
 >>> o.key = "value"
 >>> o.key
 >>> 'value'

Objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided, the methods are
factored out into functions like get, items, keys, register, set, update
and values.

great for giving objects peristence by having their state stored in files::

 >>> from cide.objects import Object
 >>> o = Object()
 >>> from cide.storage import Storage
 >>> Storage.save(o)
 cide.objects.Object/89efa5fd7ad9497b96fdcb5f01477320/2022-11-21/17:20:12.221192


**AUTHOR**


B.H.J. Thate - operbot100@gmail.com


**COPYRIGHT**


``cide`` is placed in the Public Domain.
