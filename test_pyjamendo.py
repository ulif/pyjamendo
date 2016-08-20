# Tests for pyjamendo
# Requires py.test
from pyjamendo import jam_radios_to_m3u

def test_jam_radios_to_m3u(capfd):
    jam_radios_to_m3u()
    out, err = capfd.readouterr()
    assert out.startswith("#EXTM3U")
    assert "EXTINF:-1, " in out
    assert "https:" not in out   # how bad, we can test this
    assert "http:" in out
