# Web Spider and Search Functionality

## Overview
This section of the application handles web crawling and search functionality, including searching for broken links and keyword-related links. It also provides features to display search results and download the results as an Excel file. Additionally, it detects links from the University of Melbourne that require sign-in.

## Functionality

### Web Spider
- **Web_spider Class:** A class to crawl and search for broken links and keyword-related links.
  - **Attributes:**
    - `visited_or_about_to_visit`: Set to keep track of visited or about-to-visit URLs.
    - `web_links`: Queue to manage URLs to be processed.
    - `baseurl`: Base URL for the spider to crawl.
    - `UOM_sign_links`: List to store links from the University of Melbourne that require sign-in.
    - `counter`: Counter to keep track of the number of URLs being processed.
    - `broken_links`: List to store broken links.
    - `keyword`: Keyword to search for in the web pages.
    - `keyword_links`: List to store links that contain the keyword.
    - `keyword_type`: Type of keyword search (wildcard or specified text).
  - **Methods:**
    - `__init__(self)`: Initializes the web spider.
    - `put_url(self, baseurl)`: Adds the base URL to the queue.
    - `put_keyword(self, keyword)`: Sets the keyword for the search.
    - `is_uom_sign_link(self, link)`: Checks if a link is from the University of Melbourne that requires sign-in.
    - `add_uom_sign_link(self, link, source_link, associated_text)`: Adds a link to the list of University of Melbourne-related links that require sign-in.
    - `deal_uom_sign_link(self, link, associated_text, source_link)`: Processes a link from the University of Melbourne that requires sign-in.
    - `add_broken_link(self, link, source_link, associated_text)`: Adds a broken link to the list.
    - `deal_broken_link(self, link, source_link, response_status, associated_text)`: Processes a broken link.
    - `translate_wildcard(self, pattern)`: Translates wildcard patterns for search.
    - `get_more_links(self)`: Processes URLs to find more links and check for keywords.
    - `detect_links(self)`: Detects broken links and filters out non-broken links.
    - `search_broken_links(self, baseurl)`: Initiates the search for broken links.
    - `search_keyword_links(self, baseurl, keyword)`: Initiates the search for keyword-related links.

### Search Functionality
- **search_link(request):** Handles the search request and initiates the web spider.
- **show_results(request):** Displays the search results.
- **search_task(url, keyword, user):** Performs the search task using the web spider.
- **download_table(results, table_name):** Saves the search results to an Excel file.
- **delete_file_after_timeout(file_path, timeout):** Deletes a file after a specified timeout.
- **download(request):** Handles the download request for the search results.

### Showing Results
- **show_results(request):** Renders the search results page.
  - Retrieves the results, token, and show_source_link flag from the session.
  - Renders the `results.html` template with the results.

### Downloading Results
- **download(request):** Handles the download request for the search results.
  - Retrieves the type and token from the GET request.
  - Constructs the file path.
  - Checks if the file exists and serves it as a response.
  - Returns an error response if the file does not exist or if the request is invalid.

## Usage
- **Search:** Access the search page, enter a URL and keyword (if any), and submit the form to initiate the search.
- **Results:** View the search results on the results page.
- **Download:** Download the search results as an Excel file.