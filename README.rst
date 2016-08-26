pyjamendo
*********

List radio streams streamed by jamendo.com.

What's this?
============

https://jamendo.com/ distributes free music whereas "free" is defined
as in `this faq <https://www.jamendo.com/faq>`_.

It also operates a couple of internet radios streaming free music.

This script uses jamendo API (v3) to determine the URLs of radio
streams. They are printed in a form suitable for m3u files. See
https://developer.jamendo.com/v3.0/read-methods for docs.

I use the listed URLs to create [extended m3u files]
(https://en.wikipedia.org/wiki/M3U) which are then fed to `cmus`, my
commandline music player. As `cmus` refuses to stream https URLs, the
script displays only ordinary, unencrypted http URLs. This is a
shortcoming of `cmus` not of jamendo.


How to run
==========

You might want to change the ``CLIENT_ID`` set in the script.

Afterwards, just do::

    $ python pyjamendo.py
        #EXTM3U
        #EXTINF:-1, Jamendo - Best Of Jamendo Radio
        http://streaming.jamendo.com/JamBestOf
        #EXTINF:-1, Jamendo - Electronic Radio
        http://streaming.jamendo.com/JamElectro
        #EXTINF:-1, Jamendo - Rock Radio
        http://streaming.jamendo.com/JamRock
        ...

You can save the result as an `.m3u` file.

Kudos to `@schuellerf` for fixing the output file format!


Running Tests
=============

The local tests can be run, with `py.test` installed. In a
`virtualenv` this can be done with::

    (venv) $ pip install pytest

Afterwards, just run::

    (venv) $ py.test

You can use `pytest-cov` to check coverage. Install it (once) with::

    (venv) $ pip install pytest-cov

and run coverage tests like this::

    (venv) $ py.test --cov=pyjamendo.py

PEP8 and other standards-compatibility test can be run with `flake8`::

    (venv) $ pip install flake8
    (venv) $ flake8 pyjamendo.py test_pyjamendo.py

If there is no output, everything is fine.
