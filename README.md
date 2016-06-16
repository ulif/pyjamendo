# pyjamendo
List radio streams streamed by jamendo.com.

**Requires Python 3.x.**

## What's this?

https://jamendo.com/ distributes free music whereas "free" is defined
as in this [faq](https://www.jamendo.com/faq).

It also operates a couple of internet radios streaming free music.

This script uses jamendo API (v3) to determine the URLs of radio
streams. They are printed in a form suitable for m3u files. See
https://developer.jamendo.com/v3.0/read-methods for docs.

I use the listed URLs to create m3u files which are then fed to
`cmus`, my commandline music player. As `cmus` refuses to stream https
URLs, the script displays only ordinary, unencrypted http URLs. This
is a shortcoming of `cmus` not of jamendo.


## How to run

You might want to change the CLIENT_ID set in the script.

Afterwards, just do

    $ python3 pyjamendo.py
	#EXTINF -1, Jamendo - Best Of Jamendo Radio
	http://streaming.jamendo.com/JamBestOf
	#EXTINF -1, Jamendo - Electronic Radio
	http://streaming.jamendo.com/JamElectro
	#EXTINF -1, Jamendo - Rock Radio
	http://streaming.jamendo.com/JamRock
	...

You can save the result as an m3u file.
