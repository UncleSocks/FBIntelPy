# FBIntelPy: Python Facebook Intelligence Search Tool

**FBIntelPy** is a Python-based Facebook intelligence search tool that aims to assists in generating filtered Facebook URLs. This is was created for the upcoming TraceLabs Search Party 2026.02. This was inspired by IntelTechnqiue's web-based search tool; this tool has updated some of the depracated filters.

In a nutshell, this tool supports the following filter types: **Posts**, **Photos**, **Videos**, **People**, **Events**, **User/Profile Information**, and **Global Search**. Some of these types also supports the addition of keywords and dates.

**[Update]:** I am really happy that this tool, especially the **Posts** search type, helped me successfully submit multiple flags in Trace Lab's February 2026 Global OSINT Search Party CTF.

### Dependencies
It is recommended to use the available PE (EXE) file. However, if you want to run it as a raw Python file, the tool is only dependent to one non-built-in library, **pyperclip**, which needs to be installed via pip.

**NOTE:** There is a known issue with **pyperclip**, where Python Interpreter version 3.10 needs to be specified for it to work.


## Generating A URL (How to Use)
Simply select one of the search types and it will enable the supported fields. Once the required fields are completed, click the **Generate URL** button to create the filtered URL. This will automatically be copied to your clipboard -- paste it to a web browser and it will display the results of the query. 


![2026-02-1823-27-04-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/5c53b360-8f14-40db-87a2-8be0ed6d35e3)


## Search Capabilities 
The table below outlines the supported search types. Certain fields are required to be filled before a URL will be generated.
| Search Type | Description | Supported Fields | Notes |
| --- | --- | --- | --- |
| Posts | Search for posts by user or location | User ID/Location ID, Keyword, Date (Year) | Relatively accurate but results may be limited; manual search appears to be unsupported. |
| Photos/Videos | Search for photos or videos by user or location | User ID/Location ID, Keyword, Date (Year) | Accuracy and result not guaranteed. Facebook appears to have deprecated this filter sometime September 2025. |
| People | Search for a person based on their employer, city, or school | Employer ID/City ID/School ID, Keyword | Working and accurate. |
| Places | Search for places (pages) based on a keyword | Keyword | Working and accurate. |
| Events | Search for events in a specific location | Location ID, Keyword | Working and accurate. |
| Account | Display account information | Account, Section | About section appears to have changed sometime last year, which resulted in fewer account information. |
| Search | Perform a global search on a specific section in the platform | Keyword, Section | N/A |

### Facebook Filtering Changes
After June 2019, Facebook has implemented _Base64-encoded JSON-structured queries_ for its filters. However, Facebook is constantly changing its filtering capabilities and sometime September 2025, they have also removed the ability to filter based on **Photos** and **Videos**. 

**IMPORTANT NOTE:** With that in mind, some of the search types may not provide accurate results (or at all) and may even suddenly be unsupported.

## Additional Developments and Known Issues
- I'm planning to consolidate other social media websites (i.e., X, Instagram, and LinkedIn) into one search tool.
- There is a known issue with one of its dependencies, **pyperclip**, where Python Interpreter version 3.10 needs to be used for it to work.
