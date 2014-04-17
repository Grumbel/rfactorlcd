rFactor Remote LCD
==================

rfactorlcd is a remote HUD for rFactor and compatible games (e.g. Game
Stock Car Extreme). It allows to display information such as speed,
rpm, oil temperature and current position on a second monitor or on
another computer.

rfactorlcd-gui.py is covered under the GPL, while the rfactorlcdPlugin
is covered under LGPL.


Installation
------------

rfactorlcd consists of two parts, a rFactor plugin that makes the
telemetry data available over the network and a simple app to display
that data.

The plugin source can be found in src/ and can be compiled with Visual
Studio Express. The resulting .dll has to be copied over into rFators
Plugins/ directory.

The rFactorLCDPlugin.ini file allows to customize the port on which
the plugin is listening, the default port is TCP/4580.

Once rFactor is running, start rfactorlcd and give it the IP of the
computer that is running rFactor on, e.g.:

./rfactorlcd-gui.py 192.168.1.1

If you want to run rfactorlcd on a second display, instead of another
computer, start it with:

./rfactorlcd-gui.py 127.0.0.1

The plugin doesn't limited the number of connected computers, so
connecting from multiple laptops should work.

To see a list of all available options:

./rfactorlcd-gui.py --help


Development
-----------

rfactorlcd-gui.py is writen in Python2.7 and uses Gtk and Cairo for
the rendering. To create a new Dashlets, create a new file for it in
`rfactorlcd/dashlets/`, use the existing dashlets for guidance. The
dashlet will automatically be detected and made available in
rfactorlcd-gui.py.


Security
--------

rfactorlcd.dll doesn't do any authentification, it will send data to
every computer that connects to port 4580.


Performance and Bandwidth
-------------------------

rFactor updates telemetry data 90 times a second and score data (lap
times, place, etc.) twice a second. rfactorlcdPlugin.dll sends that
data basically raw over the network, using around 40kB/s.


Disclaimer
----------

rfactorlcd is a homebrew tool for rFactor, GSC2013 and other
compatible games and in no way affiliated with Image Space
Incorporated, SimBin Studios or Reiza Studios.
