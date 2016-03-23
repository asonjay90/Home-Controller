# Home-Controller
Application developed to control as many devices in my apartment as possible.

Created as a RESTful web service using Python and the Flask microframework. This is designed to be used with a RaspberryPI. It takes advantage of the GPIO to control relays that control RF remotes for other devices such as light switches and outlets. This also uses the libCEC library to control HDMI Devices as well as the Phue library to control Philps Hue Bulbs.
