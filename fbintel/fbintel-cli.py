

import base64
import json
import argparse
from urllib.parse import quote


FACEBOOK_BASE_URL = "https://www.facebook.com/"
SEARCH_TYPE_SELECTION = ["posts", "photos", "videos", "people",
                         "places", "events", "account", "search"]

PEOPLE_SEARCH_ID_MAP = {
    "employer":{"filter":"employer", "name":"users_employer"},
    "city":{"filter":"city", "name":"users_location"},
    "school":{"filter":"school", "name":"users_school"}
}

ACCOUNT_SECTION_MAP = {
    0:"",
    1:"about",
    2:"directory_intro",
    3:"directory_category",
    4:"directory_personal_details",
    5:"directory_work",
    6:"directory_education",
    7:"directory_activities",
    8:"directory_interests",
    9:"directory_travel",
    10:"directory_links",
    11:"directory_contact_info",
    12:"directory_privacy_and_legal_info",
    13:"directory_names",
    14:"about_details",
    15:"following",
    16:"photos",
    17:"photos_albums",
    18:"videos",
    19:"reels",
    20:"places_visited",
    21:"map",
    22:"places_recent",
    23:"sports",
    24:"music",
    25:"movies",
    26:"tv",
    27:"books",
    28:"games",
    29:"likes",
    30:"events",
    31:"did_you_know",
    32:"reviews",
    33:"reviews_given",
    34:"reviews_written",
    35:"notes"
}

SEARCH_SECTION_MAP = {
    0:"top",
    1:"posts",
    2:"photos",
    3:"videos",
    4:"marketplace",
    5:"pages",
    6:"places",
    7:"groups",
    8:"apps",
    9:"events",
    10:"links",
    11:"watch"
}


class ArgParser:

    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="FBIntelPy-CLI", description="Command-line version of FBIntelPy.")
        self._add_args()

    def _add_args(self):
        self.parser.add_argument(
            "type",
            type=str,
            help="Specify the search type: posts, videos, photos, people, places, events, account, or search."
        )
        self.parser.add_argument(
            "-iT", "--id-type",
            type=str,
            default="user",
            dest="id_type",
            help="Specify the ID type."
        )
        self.parser.add_argument(
            "--id",
            type=str,
            dest="id",
            help="Enter ID value."
        )
        self.parser.add_argument(
            "-k", "--keyword",
            type=str,
            dest="keyword",
            help="Enter a keyword."
        )
        self.parser.add_argument(
            "-y", "--year",
            type=str,
            default="top",
            dest="year",
            help="Specify the year."
        )
        self.parser.add_argument(
            "-a", "--account",
            type=str,
            dest="account",
            help="Enter the account name."
        )
        self.parser.add_argument(
            "-s", "--section",
            type=int,
            default=0,
            dest="section",
            help="Specify a specific profile section number."
        )

    def parse_arguments(self):
        return self.parser.parse_args()
    

def encode(filter_string):
    string_bytes = filter_string.encode("ascii")
    base64_bytes = base64.b64encode(string_bytes)
    return base64_bytes.decode("ascii") 


class ConstructFbUrl:

    def __init__(self, type, id_type, id, keyword, year, 
                 account, section):
        self.type = type.lower()
        self.id_type = id_type.lower() if id_type else None
        self.id = id.lower() if id else None
        self.keyword = (quote(keyword.lower()) if keyword else None)
        self.year = year.lower() if year else None
        self.account = (quote(account.lower()) if account else None)
        self.section = section if section else 0

    def _build_filtered_url(self, url_path, raw_filter_dict):
        raw_filter = json.dumps(raw_filter_dict)
        encoded_filter = encode(raw_filter)
        return f"{FACEBOOK_BASE_URL}{url_path}{encoded_filter}"

    def _creation_time_json(self):
        creation_time_args = {
            "start_year":self.year,
            "start_month":f"{self.year}-1",
            "end_year":self.year,
            "end_month":f"{self.year}-12",
            "start_day":f"{self.year}-1-1",
            "end_day":f"{self.year}-12-31"
        }
        creation_time = {
            "name":"creation_time",
            "args":json.dumps(creation_time_args)
        }
        return json.dumps(creation_time)

    def _construct_user_id_url(self):
        if not self.id:
            return "Unable to generate a URL. Specify a user ID."
        
        filter_args_dict = {
            "name":"author",
            "args":self.id
        }

        if self.year == "top":
            raw_filter_dict = {
                "rp_author":json.dumps(filter_args_dict)
            }
        else:
            raw_filter_dict = {
                "rp_author":json.dumps(filter_args_dict),
                "rp_creation_time":self._creation_time_json()
            }

        url_path = f"search/{self.type}?q={self.keyword}&epa=FILTERS&filters="
        return self._build_filtered_url(url_path, raw_filter_dict)
    
    def _construct_location_id_url(self):
        if not self.id:
            return "Unable to generate a URL. Specify a location ID."
        
        filter_args_dict = {
            "name":"location",
            "args":self.id
        }

        if self.type == "posts" and self.year == "top":
            raw_filter_dict = {
                "rp_location":json.dumps(filter_args_dict)
            }
        elif self.type == "posts":
            raw_filter_dict = {
                "rp_location":json.dumps(filter_args_dict),
                "rp_creation_time":self._creation_time_json()
            }
        elif self.year == "top":
            raw_filter_dict = {
                "rp_author":json.dumps(filter_args_dict)
            }
        else:
            raw_filter_dict = {
                "rp_author":json.dumps(filter_args_dict),
                "rp_creation_time":self._creation_time_json()
            }

        url_path = f"search{self.type}?q={self.keyword}&epa=FILTERS&filters="
        return self._build_filtered_url(url_path, raw_filter_dict)
    
    def _construct_people_url(self):
        if not PEOPLE_SEARCH_ID_MAP.get(self.id_type):
            return "Unable to generate URL. Invalid ID type."
        if not self.id or not self.keyword:
            return "Unable to generate URL. Specify an ID and keyword."
        
        filter_args_dict = {
            "name":PEOPLE_SEARCH_ID_MAP[self.id_type]["name"],
            "args":self.id
        }
        raw_filter_dict = {
            PEOPLE_SEARCH_ID_MAP[self.id_type]["filter"]:json.dumps(filter_args_dict)
        }

        url_path = f"search/people/?q={self.keyword}&epa=FILTERS&filters="
        return self._build_filtered_url(url_path, raw_filter_dict)
    
    def _construct_events_url(self):
        if not self.id or not self.keyword:
            return "Unable to generate URL. Enter a location ID and keyword."
        
        filter_args_dict = {
            "name":"filter_events_location",
            "args":self.id
        }
        raw_filter_dict = {
            "rp_events_locations":json.dumps(filter_args_dict)
        }
        url_path = f"search/{self.type}?q={self.keyword}&epa=FILTERS&filters="
        return self._build_filtered_url(url_path, raw_filter_dict)

    def _construct_account_url(self):
        if not self.account:
            return "Unable to generate URL. Enter an account name and specify a section value."
        return f"{FACEBOOK_BASE_URL}{self.account}/{ACCOUNT_SECTION_MAP[self.section]}"
    
    def _consturct_places_url(self):
        if not self.keyword:
            return "Unable to generate URL. Enter a keyword."
        return f"{FACEBOOK_BASE_URL}search/places/?q={self.keyword}"
    
    def _construct_search_url(self):
        if not self.keyword:
            return "Unable to generate URL. Enter a keyword and specify a section value."
        return f"{FACEBOOK_BASE_URL}search/{SEARCH_SECTION_MAP[self.section]}/?q={self.keyword}" 


    def consturct_fb_url(self):
        construct_url_handlers = {
            "people":self._construct_people_url,
            "events":self._construct_events_url,
            "account":self._construct_account_url,
            "places":self._consturct_places_url,
            "search":self._construct_search_url
        }

        if self.type in ["posts", "videos", "photos"]:
            self.keyword = self.keyword if self.keyword else self.type
            if self.id_type == "user":
                return self._construct_user_id_url()
            if self.id_type == "location":
                return self._construct_location_id_url()
            
        handler = construct_url_handlers.get(self.type)
        if handler:
            return handler()
        
        return "Unknown error. Enter -h for the available options."


def generate_url(type=None, id_type=None, id=None, keyword=None,
                 year=None, account=None, section=None):
    
    if type.lower() in SEARCH_TYPE_SELECTION:
        filter_data = {
            "id_type":id_type,
            "id":id,
            "keyword":keyword,
            "year":year,
            "account":account,
            "section":section
        }
        return print(ConstructFbUrl(type, **filter_data).consturct_fb_url())
    else:
        return print("Invalid search type. Use -h for more information.")
        
    
if __name__ == "__main__":
    args = ArgParser().parser.parse_args()
    generate_url(args.type, args.id_type, args.id, args.keyword,
                 args.year, args.account, args.section)