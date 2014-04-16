rFactor Remote LCD
==================

rfactorlcd is a simple HUD for rFactor and compatible games (e.g. Game
Stock Car Extreme). It allows to display information such as speed,
rpm, oil temperature and current position on a second monitor or on
another computer.


Installation
------------

rfactorlcd consists of two parts, a rFactor plugin that makes the
rFactor data available over the network and a simple app to display
that data.

The plugin source can be found in src/ and can be compiled with Visual
Studio Express. The resulting .dll has to be copied over into rFators
Plugins/ directory.

Once rFactor is running, start rfactorlcd and give it the IP of the
computer that is running rFactor on, e.g.:

./rfactorlcd-app.py 192.168.1.1

If you want to run rfactorlcd on a second display, instead of another
computer, start it with:

./rfactorlcd-app.py 127.0.0.1

To see a list of all available options:

./rfactorlcd-app.py --help


Disclaimer
----------

rfactorlcd is a homebrew tool for rFactor, GSC2013 and other
compatible games and in no way affiliated with Image Space
Incorporated, SimBin Studios, Reiza Studios or vRacing.pl.
