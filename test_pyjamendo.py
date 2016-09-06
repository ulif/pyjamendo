# Tests for pyjamendo
# Requires py.test
import pytest
import pyjamendo
from pyjamendo import call_api, jam_radios_to_m3u, main


def fake_urlopen(url):
    from io import BytesIO
    if not "client_id=56d30c95" in url:
        result = BytesIO(SAMPLE_INVALID_CLIENT_ID)
    elif "radios/?" in url:
        result = BytesIO(SAMPLE_RADIOS_RESP)
    elif "name=bestof" in url:
        result = BytesIO(SAMPLE_RADIO_ENTRY_BESTOF)
    elif "name=electro" in url:
        result = BytesIO(SAMPLE_RADIO_ENTRY_ELECTRO)
    return result


@pytest.fixture(scope="function")
def jamendo_api(request, monkeypatch):
    """This fixture simulates the Jamendo API.

    Replaces 'urlopen' temporarily.
    """
    monkeypatch.setattr(pyjamendo, 'urlopen', fake_urlopen)


SAMPLE_RADIOS_RESP = b'''
{
        "headers":{
            "status":"success",
            "code":0,
            "error_message":"",
            "warnings":"",
            "results_count":10
        },
        "results":[
            {
                        "id":1,
                        "name":"bestof",
                        "dispname":"Best Of Jamendo Radio",
                        "type":"www",
    "image":"https:\/\/imgjam2.jamendo.com\/new_jamendo_radios\/bestof150.jpg"
            },
            {
                        "id":2,
                        "name":"electro",
                        "dispname":"Electronic Radio",
                        "type":"www",
   "image":"https:\/\/imgjam1.jamendo.com\/new_jamendo_radios\/electro150.jpg"
            }
       ]
}
'''


SAMPLE_RADIO_ENTRY_BESTOF = b'''
{
    "headers":{
        "status":"success",
        "code":0,
        "error_message":"",
        "warnings":"",
        "results_count":1
    },
    "results":[
        {
            "id":1,
            "name":"bestof",
            "dispname":"Best Of Jamendo Radio",
            "type":"www",
 "image":"https:\/\/imgjam1.jamendo.com\/new_jamendo_radios\/bestof150.jpg",
            "stream":"https:\/\/streaming.jamendo.com\/JamBestOf",
            "playingnow":{
                "track_id":"132859",
                "artist_id":"338094",
                "album_id":"18775",
                "album_name":"royal goulasch",
                "track_name":"La petite reine",
 "track_image":
   "https:\/\/imgjam.jamendo.com\/albums\/s18\/18775\/covers\/1.200.jpg",
                "artist_name":"Royal Goulasch"
            },
            "callmeback":"82000"
        }
    ]
}
'''

SAMPLE_RADIO_ENTRY_ELECTRO = b'''
{
    "headers":{
        "status":"success",
        "code":0,
        "error_message":"",
        "warnings":"",
        "results_count":1
    },
    "results":[
        {
            "id":2,
            "name":"electro",
            "dispname":"Electronic Radio",
            "type":"www",
   "image":"https:\/\/imgjam1.jamendo.com\/new_jamendo_radios\/electro150.jpg",
            "stream":"https:\/\/streaming.jamendo.com\/JamElectro",
            "playingnow":{
                "track_id":"552164",
                "artist_id":"358851",
                "album_id":"64251",
                "album_name":"Gotta hold On",
                "track_name":"Star (EM's Radio-Friendly Mix)",
                "track_image":
    "https:\/\/imgjam.jamendo.com\/albums\/s64\/64251\/covers\/1.200.jpg",
                "artist_name":"eddie e feat eliza"
            },
            "callmeback":"54000"
        }
    ]
}
'''


SAMPLE_INVALID_CLIENT_ID = b'''{
    "headers":{
        "status":"failed",
        "code":5,
        "error_message":
   "Jamendo Api Invalid Client Id Error: Your credential is not authorized.",
        "warnings":"",
        "results_count":0
    },
    "results":[

    ]
}
'''


def test_jam_radios_to_m3u(capfd, jamendo_api):
    # we can generate a list of jamendo radio stations
    jam_radios_to_m3u()
    out, err = capfd.readouterr()
    assert out.startswith("#EXTM3U")
    assert "EXTINF:-1, " in out


def test_allow_https_links_option_default(capfd, jamendo_api):
    # https_lins option default works
    jam_radios_to_m3u()  # default
    out, err = capfd.readouterr()
    assert "https:" in out
    assert "http:" not in out


def test_allow_https_links_option_on(capfd, jamendo_api):
    # https_lins option can be switched on
    jam_radios_to_m3u(allow_https_links=True)
    out, err = capfd.readouterr()
    assert "https:" in out
    assert "http:" not in out


def test_allow_https_links_option_off(capfd, jamendo_api):
    # https_lins option can be switched off
    jam_radios_to_m3u(allow_https_links=False)
    out, err = capfd.readouterr()
    assert "https:" not in out
    assert "http:" in out


def test_call_api_delivers_parsed_json_data(jamendo_api):
    # we can call the jamendo API and will get parsed JSON data.
    result = call_api(
        "radios/stream", dict(name="electro"))
    assert isinstance(result, dict)
    assert "headers" in result
    assert isinstance(result["results"], list)


def test_call_api_invalid_client_id(jamendo_api):
    # we can see if a client id is invalid
    result = call_api(
        "radios/stream", dict(name="electro"), client_id="nonsense")
    assert result["headers"]["status"] == "failed"
    assert result["headers"]["code"] == 5
    assert result["headers"]["results_count"] == 0


def test_call_api_valid_client_id(jamendo_api):
    # we can see if a client id is valid
    result = call_api(
        "radios/stream", dict(name="electro"), client_id="56d30c95")
    assert result["headers"]["status"] == "success"
    assert result["headers"]["code"] == 0
    assert result["headers"]["results_count"] > 0


def test_main(capfd, jamendo_api):
    # we can call main() w/o hassle
    main()
    out, err = capfd.readouterr()
    assert "EXTINF:-1, " in out
    assert "https:" not in out
