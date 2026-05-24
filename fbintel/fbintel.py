# FBIntelPy: Python Facebook Intelligence Search Tool
# GitHub @unclesocks: https://github.com/UncleSocks
#
# MIT License
#
# Copyright (c) 2026 Tyrone Kevin Ilisan
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the 
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit 
# persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT 
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.




import os
import sys
import base64
import json
import tkinter as tk
from tkinter import ttk
from urllib.parse import quote

import pyperclip



WINDOW_TITLE = "FBIntelPy: Python Facebook Intelligence Search Tool"
WINDOW_DIMENSION = "690x500"
WINDOW_ICON_PATH = "assets/logo.png"

WIDGET_LABEL_MAP = {
    "search_type":"Search Type:",
    "id_type":"ID Type:",
    "id_value":"ID:",
    "keyword":"Keyword:",
    "year":"Year:",
    "account":"Account:",
    "section":"Section:",
    "generate_button":"Generate URL"
}

FACEBOOK_BASE_URL = "https://www.facebook.com/"
SEARCH_TYPE_SELECTION = ["Posts", "Photos", "Videos", "People", "Places", 
                         "Events", "Account", "Search"]

YEAR_SELECTION = ["Top", "2026", "2025", "2024", "2023", "2022", 
                  "2021", "2020", "2019", "2018", "2017", "2016", 
                  "2015", "2014", "2013", "2012", "2011", "2010"]

ACCOUNT_SECTION_MAP = {
    "Timeline":"",
    "About":"about",
    "Intro":"directory_intro",
    "Category":"directory_category",
    "Personal Details":"directory_personal_details",
    "Work":"directory_work",
    "Education":"directory_education",
    "Hobbies":"directory_activities",
    "Interests":"directory_interests",
    "Travel":"directory_travel",
    "Links":"directory_links",
    "Contact Info":"directory_contact_info",
    "Privacy/Legal Info":"directory_privacy_and_legal_info",
    "Names":"directory_names",
    "Details About You":"about_details",
    "Following":"following",
    "Photos":"photos",
    "Photos Albums":"photos_albums",
    "Videos":"videos",
    "Reels":"reels",
    "Check-ins":"places_visited",
    "Visits":"map",
    "Recent Check-ins":"places_recent",
    "Sports":"sports",
    "Music":"music",
    "Movies":"movies",
    "TV":"tv",
    "Books":"books",
    "Apps & Games":"games",
    "Likes":"likes",
    "Events":"events",
    "Facts":"did_you_know",
    "Reviews":"reviews",
    "Reviews Given":"reviews_given",
    "Reviews Written":"reviews_written",
    "Notes":"notes"
}

SEARCH_QUERY_SELECTION = ["Top", "Posts", "People", "Photos", "Videos", 
                          "Marketplace", "Pages", "Places", "Groups",
                          "Apps", "Events", "Links", "Watch"]

POSTS_PHOTOS_VIDEOS_ID_TYPES = ["User ID", "Location ID"]
PEOPLE_ID_TYPES = ["Employer ID", "City ID", "School ID"]
EVENTS_ID_TYPES = ["Location ID"]

PEOPLE_SEARCH_ID_MAP = {
    "employer id":{"filter":"employer", "name":"users_employer"},
    "city id":{"filter":"city", "name":"users_location"},
    "school id":{"filter":"school", "name":"users_school"}
}


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def encode(filter_string):
    string_bytes = filter_string.encode("ascii")
    base64_bytes = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string


class ConstructFbUrl:

    def __init__(self, selected_type, selected_id=None, id_value=None, 
                 keyword=None, selected_year=None, account=None, section=None):
        self.selected_type = selected_type
        self.selected_id = selected_id.lower() if selected_id else None
        self.id_value = id_value.lower() if id_value else None
        self.keyword = (quote(keyword) if keyword else None)
        self.selected_year = selected_year.lower() if selected_year else None
        self.account = quote(account.lower()) if account else None
        self.section = section

    def _build_filtered_url(self, url_path, raw_filter_dict):
        raw_filter = json.dumps(raw_filter_dict)
        encoded_filter = encode(raw_filter)
        return f"{FACEBOOK_BASE_URL}{url_path}{encoded_filter}"

    def _creation_time_json(self):
        creation_time_args = {
            "start_year":self.selected_year,
            "start_month":f"{self.selected_year}-1",
            "end_year":self.selected_year,
            "end_month":f"{self.selected_year}-12",
            "start_day":f"{self.selected_year}-1-1",
            "end_day":f"{self.selected_year}-12-31"
        }
        creation_time = {
            "name":"creation_time",
            "args":json.dumps(creation_time_args)
        }
        return json.dumps(creation_time)

    def _construct_user_id_url(self):
        if not self.id_value:
            return "Unable to generate URL. Enter a user ID."
        
        filter_args_dict = {
                "name":"author",
                "args":self.id_value
            }
        
        if self.selected_year == "top":
            raw_filter_dict = {
                "rp_author":json.dumps(filter_args_dict)
            }
        else:
            raw_filter_dict = {
                "rp_author":json.dumps(filter_args_dict),
                "rp_creation_time":self._creation_time_json()
            }

        url_path = f"search/{self.selected_type}?q={self.keyword}&epa=FILTERS&filters="
        return self._build_filtered_url(url_path, raw_filter_dict)

    def _construct_location_id_url(self):
        if not self.id_value:
            return "Unable to generate URL. Enter a location ID."

        filter_args_dict = {
            "name":"location",
            "args":self.id_value
        }

        if self.selected_type == "posts" and self.selected_year == "top":
            raw_filter_dict = {
                "rp_location":json.dumps(filter_args_dict)
            }
        elif self.selected_type == "posts":
            raw_filter_dict = {
                "rp_location":json.dumps(filter_args_dict),
                "rp_creation_time":self._creation_time_json()
            }
        elif self.selected_year == "top":
            raw_filter_dict = {
                "rp_author":json.dumps(filter_args_dict)
            }
        else:
            raw_filter_dict = {
                "rp_author":json.dumps(filter_args_dict),
                "rp_creation_time":self._creation_time_json()
            }

        url_path = f"search/{self.selected_type}?q={self.keyword}&epa=FILTERS&filters="
        return self._build_filtered_url(url_path, raw_filter_dict)
    
    def _construct_people_url(self):
        if not self.id_value or not self.keyword:
            output = "Unable to generate URL. Enter an ID and a keyword (account name)."
            return output
        
        filter_args_dict = {
            "name":PEOPLE_SEARCH_ID_MAP[self.selected_id]["name"],
            "args":self.id_value
        }
        raw_filter_dict = {
            PEOPLE_SEARCH_ID_MAP[self.selected_id]["filter"]:json.dumps(filter_args_dict)
        }
        url_path = f"search/people/?q={self.keyword}&epa=FILTERS&filters="
        return self._build_filtered_url(url_path, raw_filter_dict)
    
    def _construct_events_url(self):
        if not self.id_value or not self.keyword:
            return "Unable to generate URL. Enter a location ID and keyword."
        
        filter_args_dict = {
            "name":"filter_events_location",
            "args":self.id_value
        }
        raw_filter_dict = {
            "rp_events_locations":json.dumps(filter_args_dict)
        }
        url_path = f"search/{self.selected_type}?q={self.keyword}&epa=FILTERS&filters="
        return self._build_filtered_url(url_path, raw_filter_dict)
    
    def _construct_account_url(self):
        if not self.account:
            return "Unable to generate URL. Enter an account."
        return f"{FACEBOOK_BASE_URL}{self.account}/{ACCOUNT_SECTION_MAP[self.section]}"

    def _construct_places_url(self):
        if not self.keyword:
            return "Unable to generate URL. Enter a keyword."
        return f"{FACEBOOK_BASE_URL}search/places/?q={self.keyword}"
    
    def _construct_search_url(self):
        if not self.keyword:
            return "Unable to generate URL. Enter a keyword."
        return f"{FACEBOOK_BASE_URL}search/{self.section.lower()}/?q={self.keyword}" 

    def construct_fb_url(self):
        construct_url_handlers = {
            "people":self._construct_people_url,
            "events":self._construct_events_url,
            "account":self._construct_account_url,
            "places":self._construct_places_url,
            "search":self._construct_search_url
        }
        
        if self.selected_type in {"posts", "photos", "videos"}:
            self.keyword = self.keyword if self.keyword else self.selected_type
            if self.selected_id == "user id":
                return self._construct_user_id_url()
            else:
                return self._construct_location_id_url()

        handler = construct_url_handlers.get(self.selected_type)
        if handler:
            return handler()

        return "Unknown error. Try selecting an ID type."
    

def generate_url(widgets):
    selected_type = widgets.search_type_combobox.get().lower()
    captured_widget_data = {
        "selected_id":widgets.id_type_combobox.get(),
        "id_value":widgets.id_entry.get(),
        "keyword":widgets.keyword_entry.get(),
        "selected_year":widgets.year_selection_combobox.get(),
        "account":widgets.account_entry.get(),
        "section":widgets.section_combobox.get()
    }
    if selected_type:
        fb_url = ConstructFbUrl(selected_type, **captured_widget_data).construct_fb_url()
        pyperclip.copy(fb_url)
        widgets.output_label.config(state="normal")
        widgets.output_label.delete("1.0", "end")
        widgets.output_label.insert(tk.END, fb_url)
        widgets.output_label.config(state="disabled")
    return


class WidgetLogicController:
    def __init__ (self, widgets):
        self.widgets = widgets

    def _disable_widget(self, widget, clear=False):
        if clear:
            if isinstance(widget, ttk.Combobox):
                widget.set("")
            else:
                widget.delete(first=0, last="end")
        widget.config(state="disabled")

    def _setup_posts_photos_videos_widgets(self):
        self.widgets.id_type_combobox.set(POSTS_PHOTOS_VIDEOS_ID_TYPES[0])
        self.widgets.id_type_combobox.config(values=POSTS_PHOTOS_VIDEOS_ID_TYPES, state="readonly")
        self.widgets.id_entry.config(state="normal")
        self.widgets.year_selection_combobox.config(values=YEAR_SELECTION, state="readonly")
        self.widgets.year_selection_combobox.set("Top")
        self.widgets.keyword_entry.config(state="normal")

        self._disable_widget(widget=self.widgets.account_entry, clear=True)
        self._disable_widget(widget=self.widgets.section_combobox, clear=True)


    def _setup_people_widgets(self):
        self.widgets.id_type_combobox.set(PEOPLE_ID_TYPES[0])
        self.widgets.id_type_combobox.config(values=PEOPLE_ID_TYPES, state="readonly")
        self.widgets.id_entry.config(state="normal")
        self.widgets.keyword_entry.config(state="normal")

        self._disable_widget(widget=self.widgets.year_selection_combobox, clear=True)
        self._disable_widget(widget=self.widgets.account_entry, clear=True)
        self._disable_widget(widget=self.widgets.section_combobox, clear=True)

    def _setup_places_widgets(self):
        self.widgets.keyword_entry.config(state="normal")

        self._disable_widget(widget=self.widgets.id_type_combobox, clear=True)
        self._disable_widget(widget=self.widgets.id_entry, clear=True)
        self._disable_widget(widget=self.widgets.year_selection_combobox, clear=True)
        self._disable_widget(widget=self.widgets.account_entry, clear=True)
        self._disable_widget(widget=self.widgets.section_combobox, clear=True)

    def _setup_events_widgets(self):
        self.widgets.id_type_combobox.config(values=EVENTS_ID_TYPES, state="readonly")
        self.widgets.id_type_combobox.set(EVENTS_ID_TYPES[0])
        self.widgets.id_entry.config(state="normal")
        self.widgets.keyword_entry.config(state="normal")

        self._disable_widget(widget=self.widgets.year_selection_combobox, clear=True)
        self._disable_widget(widget=self.widgets.account_entry, clear=True)
        self._disable_widget(widget=self.widgets.section_combobox, clear=True)

    def _setup_account_widgets(self):
        self._disable_widget(widget=self.widgets.section_combobox, clear=True)
        self.widgets.account_entry.config(state="normal")
        self.widgets.section_combobox.set(next(iter(ACCOUNT_SECTION_MAP)))
        self.widgets.section_combobox.config(state="readonly", values=list(ACCOUNT_SECTION_MAP.keys()))

        self._disable_widget(widget=self.widgets.id_entry, clear=True)
        self._disable_widget(widget=self.widgets.keyword_entry, clear=True)
        self._disable_widget(widget=self.widgets.year_selection_combobox, clear=True)

    def _setup_search_widgets(self):
        self._disable_widget(widget=self.widgets.section_combobox, clear=True)
        self.widgets.keyword_entry.config(state="normal")
        self.widgets.section_combobox.set(SEARCH_QUERY_SELECTION[0])
        self.widgets.section_combobox.config(state="readonly", values=SEARCH_QUERY_SELECTION)

        self._disable_widget(widget=self.widgets.id_type_combobox, clear=True)
        self._disable_widget(widget=self.widgets.id_entry, clear=True)
        self._disable_widget(widget=self.widgets.year_selection_combobox, clear=True)
        self._disable_widget(widget=self.widgets.account_entry, clear=True)


    def search_type_logic(self, event=None):
        self.widgets.id_type_combobox.set("")
        self.widgets.id_type_combobox.config(state="disabled")
        self.selected_type = self.widgets.search_type_combobox.get().lower()
        
        if self.selected_type == "posts" or self.selected_type == "photos" or \
            self.selected_type == "videos":
            self._setup_posts_photos_videos_widgets()
        elif self.selected_type == "people":
            self._setup_people_widgets()
        elif self.selected_type == "places":
            self._setup_places_widgets()
        elif self.selected_type == "events":
            self._setup_events_widgets()
        elif self.selected_type == "account":
            self._setup_account_widgets()
        elif self.selected_type == "search":
            self._setup_search_widgets()
        else:
            self._disable_id_type_combobox()


class GenerateWidgets:
    def __init__(self, root):
        self.root = root
        self._root_setup()
        self.widget_controller = WidgetLogicController(self)

    def _root_setup(self):
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_DIMENSION)
        window_icon_path = resource_path(WINDOW_ICON_PATH)
        window_icon = tk.PhotoImage(file=window_icon_path)
        self.root.iconphoto(True, window_icon)

    def display_widgets(self):
        self.search_type_widgets()
        self.id_type_widgets()
        self.id_entry_widgets()
        self.keyword_widgets()
        self.year_selection_widgets()
        self.account_widgets()
        self.section_widgets()
        self.generate_button()
        self.output_widgets()

    def search_type_widgets(self):
        search_type_label = tk.Label(self.root, text=WIDGET_LABEL_MAP["search_type"])
        search_type_label.grid(row=0, column=0, padx=10, pady=15, sticky="E")
        self.search_type_combobox = ttk.Combobox(self.root, values=SEARCH_TYPE_SELECTION, state="readonly")
        self.search_type_combobox.grid(row=0, column=1, sticky="W")
        self.search_type_combobox.bind("<<ComboboxSelected>>", func=self.widget_controller.search_type_logic)

    def id_type_widgets(self):
        id_type_label = tk.Label(self.root, text=WIDGET_LABEL_MAP["id_type"])
        id_type_label.grid(row=1, column=0, padx=10, pady=15, sticky="E")
        self.id_type_combobox = ttk.Combobox(self.root, state="disabled")
        self.id_type_combobox.grid(row=1, column=1, sticky="W")

    def id_entry_widgets(self):
        id_entry_label = tk.Label(self.root, text=WIDGET_LABEL_MAP["id_value"])
        id_entry_label.grid(row=1, column=2, padx=10, sticky="E")
        self.id_entry = tk.Entry(self.root, state="disabled")
        self.id_entry.grid(row=1, column=3, sticky="W")

    def keyword_widgets(self):
        keyword_label = tk.Label(self.root, text=WIDGET_LABEL_MAP["keyword"])
        keyword_label.grid(row=2, column=0, padx=10, sticky="E")
        self.keyword_entry = tk.Entry(self.root, state="disabled")
        self.keyword_entry.grid(row=2, column=1, sticky="W")

    def year_selection_widgets(self):
        year_selection_label = tk.Label(self.root, text=WIDGET_LABEL_MAP["year"])
        year_selection_label.grid(row=2, column=2, padx=10, sticky="E")
        self.year_selection_combobox = ttk.Combobox(self.root, state="disabled")
        self.year_selection_combobox.grid(row=2, column=3, sticky="W")

    def account_widgets(self):
        account_label = tk.Label(self.root, text=WIDGET_LABEL_MAP["account"])
        account_label.grid(row=3, column=0, padx=10, pady=15, sticky="E")
        self.account_entry = tk.Entry(self.root, state="disabled")
        self.account_entry.grid(row=3, column=1, sticky="W")

    def section_widgets(self):
        section_label = tk.Label(self.root, text=WIDGET_LABEL_MAP["section"])
        section_label.grid(row=3, column=2, padx=10, sticky="E")
        self.section_combobox = ttk.Combobox(self.root, state="disabled")
        self.section_combobox.grid(row=3, column=3, sticky="W")

    def generate_button(self):
        self.generate_button = tk.Button(self.root, text=WIDGET_LABEL_MAP["generate_button"],
                                    command=lambda: generate_url(self), width=20)
        self.generate_button.grid(row=4, column=0, columnspan=2, padx=5, pady=20)

    def output_widgets(self):
        output_frame = tk.Frame(self.root)
        output_frame.grid(row=5, column=0, columnspan=6, sticky="EW", padx=20)
        self.output_label = tk.Text(output_frame, wrap="char")
        self.output_label.pack(fill="both")
        self.output_label.config(height=15)
        self.output_label.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    init = GenerateWidgets(root)
    init.display_widgets()
    root.mainloop()