
# Documentation for Web_spider Class 

## Overview

The `Web_spider` class is a web crawler in search_link.py file under apps/search_link directory  designed to:
- Search for specific keywords on a given website.
- Detect broken or restricted links.
- Filter and collect links related to the University of Melbourne (UOM) sign-in required links.

This class maintains a queue of URLs to visit, stores various categories of links, and manages multithreaded crawling operations to retrieve, categorize, and filter links effectively.

---

## Class: `Web_spider`

### Attributes

- **`visited_or_about_to_visit`** (set): Tracks URLs that have already been visited or are about to be visited to avoid redundancy.
- **`web_links`** (`Queue`): Holds the URLs that are queued for processing.
- **`baseurl`** (str): The base URL of the website to be crawled.
- **`UOM_sign_links`** (list): Stores links associated with UOM.
- **`counter`** (int): Counts the current number of active tasks in the queue.
- **`broken_links`** (list): Records any broken or inaccessible links encountered.
- **`keyword`** (str): The target keyword or pattern to search for on each page.
- **`keyword_links`** (list): Stores links that contain the specified keyword.
- **`keyword_type`** (str): Specifies the type of keyword search (`SPECIFIED_TEXT` or `WILDCARD`).

### Methods

#### `__init__(self)`
Initializes the `Web_spider` class, setting up default values and preparing queues and lists for link storage and tracking.

#### `put_url(self, baseurl)`
Adds a base URL to the queue for processing.

- **Parameters**:
  - `baseurl` (str): The URL to add to the queue.

#### `put_keyword(self, keyword)`
Sets the keyword to search for on each webpage.

- **Parameters**:
  - `keyword` (str): The target keyword or pattern.

#### `is_uom_sign_link(self, link)`
Determines if a link belongs to the University of Melbourne by checking for 'unimelb' in the URL.

- **Parameters**:
  - `link` (str): The URL to check.
- **Returns**:
  - `bool`: `True` if the link contains 'unimelb', `False` otherwise.

#### `add_uom_sign_link(self, link, source_link, associated_text)`
Adds a link associated with UOM to `UOM_sign_links`.

- **Parameters**:
  - `link` (str): The UOM URL.
  - `source_link` (str): The source page link where this URL was found.
  - `associated_text` (str): The text associated with the link.

#### `deal_uom_sign_link(self, link, associated_text, source_link)`
Handles the processing of UOM links by checking and adding them to `UOM_sign_links`.

- **Parameters**:
  - `link` (str): The UOM URL.
  - `associated_text` (str): Associated text.
  - `source_link` (str): Source link where this URL was found.

#### `add_broken_link(self, link, source_link, associated_text)`
Records a broken link with the source link and associated text.

- **Parameters**:
  - `link` (str): The broken URL.
  - `source_link` (str): The page where this broken link was found.
  - `associated_text` (str): Associated text with the broken link.

#### `deal_broken_link(self, link, source_link, response_status, associated_text)`
Handles processing of broken links by adding them to `broken_links`.

- **Parameters**:
  - `link` (str): The broken URL.
  - `source_link` (str): The page where this broken link was found.
  - `response_status` (int): HTTP status code for the broken link.
  - `associated_text` (str): Text associated with the broken link.

#### `translate_wildcard(self, pattern)`
Converts SQL-like wildcard patterns to shell-like patterns for `fnmatch` use.

- **Parameters**:
  - `pattern` (str): The pattern to convert.
- **Returns**:
  - `str`: The converted pattern.

#### `get_more_links(self)`
Processes URLs in the `web_links` queue, categorizing links based on the keyword and UOM association, and queues new links found on each page.

- **Operations**:
  - Fetches each URL, checks if it matches the base URL or keyword.
  - Searches for links that contain the keyword.
  - Adds valid links back into the queue for further processing.

#### `detect_links(self)`
Detects if links in `web_links` are valid or broken, and re-adds valid links to the queue.

- **Operations**:
  - Checks content type and HTTP status.
  - Re-adds valid links to `web_links`.
  - Records broken links for reporting.

#### `search_broken_links(self, baseurl)`
Starts the process of detecting broken links on a website by populating the queue with `baseurl` and managing threads to detect and categorize links.

- **Parameters**:
  - `baseurl` (str): The starting URL for broken link detection.
- **Returns**:
  - `tuple`: Sorted list of broken links and UOM links found.

#### `search_keyword_links(self, baseurl, keyword)`
Starts the process of searching for links containing a specific keyword or pattern, managing threads to perform link detection and categorization.

- **Parameters**:
  - `baseurl` (str): The starting URL for keyword search.
  - `keyword` (str): The keyword or pattern to search.
- **Returns**:
  - `tuple`: Sorted list of keyword links and UOM links found.

---

This class is designed to run multiple threads for efficient web crawling, making it suitable for large-scale link analysis on websites with University of Melbourne affiliation or specific keywords.
