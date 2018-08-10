import json
import requests

BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

query_type = {  "simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"} }


def query_site(url, params, uid="", fmt="json"):
    """
    This is the main function for making queries to the musicbrainz API.
    The query should return a json document.
    """
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print ("requesting", r.url)

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    """
    This adds an artist name to the query parameters before making an API call
    to the function above.
    """
    params["query"] = "artist:" + name

    return query_site(url, params)


def pretty_print(data, indent=4):
    """
    After we get our output, we can use this function to format it
    to be more readable.
    """
    if type(data) == dict:
        print (json.dumps(data, indent=indent, sort_keys=True))
    else:
        print (data)


def main():
    """
    Example and the 5 quizzes
    """
    # Query for releases from that band using the artist_id
    results = query_by_name(ARTIST_URL, query_type["simple"], "Nirvana")
    artist_id = results["artists"][3]["id"]
    artist_data = query_site(ARTIST_URL, query_type["releases"], artist_id)
    releases = artist_data["releases"]

    # Print information about releases from the selected band
    print ("\nONE RELEASE:")
    pretty_print(releases[0], indent=2)
    release_titles = [r["title"] for r in releases]
    print ("\nALL TITLES:")
    for t in release_titles:
        print (t)

    # How many bands named "First Aid Kit"
    first_aid_kit = query_by_name(ARTIST_URL, query_type["simple"], "First Aid Kit")
    all_bands = [atr["name"] for atr in first_aid_kit["artists"]]
    count = 0
    for name in all_bands:
        if name.lower() == "first aid kit":
            count += 1
    print ("\nNumber of the bands named 'First Aid Kit': ", count)

    # Begin-Area name for "Queen"
    queen = query_by_name(ARTIST_URL, query_type["simple"], "Queen")
    pretty_print (queen["artists"][0]["begin-area"])

    # Spanish alias for "Beatles"
    beatles = query_by_name(ARTIST_URL, query_type["simple"], "Beatles")
    beatles_id = beatles["artists"][0]["id"]
    beatles_data = query_site(ARTIST_URL, query_type["aliases"], beatles_id)
    beatles_aliases = [{ali["locale"]:ali["name"]} for ali in beatles_data["aliases"]]
    spanish_alias = [loc['es'] for loc in beatles_aliases if 'es' in loc]
    print ("\nBeatles Aliases: ", spanish_alias)

    # Nirvana disambiguation
    nirvana = query_by_name(ARTIST_URL, query_type["simple"], "Nirvana")
    print ("\nNirvana Disambiguation:", nirvana["artists"][0]["disambiguation"])

    # When was "One Direction" formed
    one_direction = query_by_name(ARTIST_URL, query_type["simple"], "One Direction")
    print ("\nOne Direction Formed: ", one_direction["artists"][0]["life-span"]["begin"])


if __name__ == '__main__':
    main()
