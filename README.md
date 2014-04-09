rFactor Remote LCD
==================

rfactorlcd is a simple HUD for rFactor, it allows to display
information such as speed, rpm, oil temperature and current position
on a second monitor or on another computer.


Installation
------------

rfactorlcd consists of two parts, a rFactor plugin that makes the
rFactor data available over the network and a simple app to display
that data.

At the moment rfactorlcd doesn't come with it's own plug-in, instead
it connects to the rFactor plug-in vracingDisplayPRO. Download and
install vracingDisplayPRO_rFactor_Plugin_1_02_Setup.exe from:

http://display.vracing.pl/download.html

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
