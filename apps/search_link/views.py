from .tokens import download_token
from django.shortcuts import render, redirect
from multiprocessing import JoinableQueue as Queue
from threading import Thread
from django.contrib.auth.decorators import login_required
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import os
import pandas as pd
import threading
from fnmatch import *
from django.http import FileResponse, HttpResponseBadRequest,HttpResponseForbidden,HttpResponseNotFound
import io
from .models import ExcelFile
REQUEST_TIMEOUT = 20
WILDCARD = 1
SPECIFIED_TEXT = 0


def index(request):
    return render(request, 'search.html')


class Web_spider():
    def __init__(self):
        # checked the links already been visited or expected to be visited
        self.visited_or_about_to_visit = set()
        # used to place the website urls that about to be visited
        self.web_links = Queue()
        self.baseurl = ''
        self.UOM_sign_links = list()
        # used to track how many links remaining to be visited
        self.counter = 0
        self.broken_links = list()
        self.keyword = 'Funding Partners'
        self.keyword_links = list()
        self.keyword_type = None

    def put_url(self, baseurl):
        # [link, source page link, associated text]
        self.web_links.put([baseurl, None, None])
        self.counter += 1
        self.baseurl = baseurl

    def put_keyword(self, keyword):
        self.keyword = keyword

    def is_uom_sign_link(self, link):
        return 'unimelb' in link

    def add_uom_sign_link(self, link, source_link, associated_text):
        self.UOM_sign_links.append({'url': link, 'source_link': source_link, 'associated_text': associated_text})

    def deal_uom_sign_link(self, link, associated_text, source_link):
        if self.is_uom_sign_link(link):
            self.add_uom_sign_link(link, source_link, associated_text)

    def add_broken_link(self, link, source_link, associated_text):
        self.broken_links.append({'url': link, 'source_link':
            source_link, 'associated_text': associated_text})

    def deal_broken_link(self, link, source_link, response_status, associated_text):
        self.add_broken_link(link, source_link, associated_text)

    def translate_wildcard(self, pattern):
        pattern = pattern.replace('%', '*')
        pattern = pattern.replace('_', '?')
        return pattern

    def get_more_links(self):

        while True:
            link_combo = self.web_links.get()
            link = link_combo[0]
            try:
                response = requests.get(link, timeout=REQUEST_TIMEOUT)
                self.visited_or_about_to_visit.add(link)
                if response.status_code == 200:
                    # the link doesn't start with the specified prefix
                    # then no need to check the links derived from its source page
                    if not link.startswith(self.baseurl):
                        continue
                    soup = BeautifulSoup(response.content, 'html.parser')
                    if self.keyword_type == SPECIFIED_TEXT:
                        # check if the keyword matches the source page for the url
                        if self.keyword is not None:
                            text = response.text
                            for keyword in self.keyword:
                                if keyword in text:
                                    urls = [item['url'] for item in self.keyword_links]
                                    # only those cases would dict be added to the keyword_links: 1. new url
                                    # 2. existing url while keyword not the same keyword
                                    if link not in urls:
                                        self.keyword_links.append({'url': link, 'associated_text': [keyword]})

                                    else:
                                        index = \
                                            [data for data, item in enumerate(self.keyword_links) if item['url'] == link][0]
                                        if keyword not in self.keyword_links[index]['associated_text']:
                                            self.keyword_links[index]['associated_text'].append(keyword)
                                            # the first keyword is the whole input without splitting
                                    if keyword == self.keyword[0]:
                                        # preventing redundant work and focusing on the most relevant result first
                                        break;


                    elif self.keyword_type == WILDCARD:
                        # go through specified wildcard pattern to see if any keyword matches
                        pattern = self.keyword
                        if pattern is not None:
                            text = soup.get_text().split()
                            result = False
                            for word in text:
                                if fnmatch(word, pattern):
                                    result = True
                                    matched_pattern = word
                                    break
                            if not result:
                                pattern = self.translate_wildcard(pattern)
                                for word in text:
                                    if fnmatch(word, pattern):
                                        result = True
                                        break
                            # found keyword in the link
                            if result:
                                self.keyword_links.append({'url': link, 'associated_text': matched_pattern})

                    for href_link in soup.find_all('a', href=True):
                        href = href_link['href']
                        text = href_link.get_text()
                        if href not in self.visited_or_about_to_visit:
                            if 'mailto:' not in href:
                                self.visited_or_about_to_visit.add(href)
                                self.web_links.put([href, link, text])
                                self.counter += 1
                            else:
                                # skip emails as they'll not be checked as website links
                                pass
                else:
                    # 403 status indicates restricted access websites from UOM
                    # any other status not 200 will be invalid (broken) links
                    if response.status_code == 403:
                        self.deal_uom_sign_link(link, link_combo[2], link_combo[1])
                    else:
                        self.deal_broken_link(link, link_combo[1], response.status_code, link_combo[2])
            except Exception as e:
                print(f'error fetch {link}, {str(e)}')
            finally:
                self.web_links.task_done()
                self.counter -= 1

    # help save time by filtering out broken link to reduce response time
    def detect_links(self):
        while True:
            link_combo = self.web_links.get()
            link = link_combo[0]

            try:
                response = requests.get(link, timeout=REQUEST_TIMEOUT)
                # if not broken, then put back to the queue
                content_type = response.headers.get('Content-Type', '').lower()

                # Check if the link is a valid download link
                if 'application/' in content_type or 'octet-stream' in content_type:
                    pass

                elif response.status_code == 200:
                    if link.startswith(self.baseurl):
                        self.web_links.put(link_combo)
                        self.counter += 1
                    else:
                        # if the qsize is zero, then no further links to be detected, ends scraping
                        if self.web_links.qsize() == 0:
                            return
                else:
                    if response.status_code == 403:
                        self.deal_uom_sign_link(link, link_combo[2], link_combo[1])
                    else:
                        self.deal_broken_link(link, link_combo[1], response.status_code, link_combo[2])

            except Exception as e:
                print(f'error fetch {link}, {str(e)}')
            finally:
                self.web_links.task_done()
                self.counter -= 1


    def search_broken_links(self, baseurl):
        self.put_url(baseurl)
        thread_list = list()
        for _ in range(20):
            t = Thread(target=self.get_more_links)
            thread_list.append(t)
        for _ in range(20):
            t = Thread(target=self.detect_links)
            thread_list.append(t)
        for t in thread_list:
            t.daemon = True
            t.start()
        self.web_links.join()
        self.broken_links = sorted(self.broken_links, key=lambda x: x['associated_text'])
        return (self.broken_links, self.UOM_sign_links)

    def search_keyword_links(self, baseurl, keyword):
        if keyword[0] == '/':
            keyword = keyword[1:]
            self.keyword_type = WILDCARD
        else:
            self.keyword_type = SPECIFIED_TEXT
        if self.keyword_type == SPECIFIED_TEXT:
            temp = keyword
            keyword = keyword.split()
            if len(keyword) == 1:
                pass
            else:
                keyword_list = [temp]
                keyword_list.extend(keyword)
                keyword = keyword_list
        self.put_keyword(keyword)

        self.put_url(baseurl)
        thread_list = list()
        for _ in range(20):
            t = Thread(target=self.get_more_links)
            thread_list.append(t)
        for _ in range(20):
            t = Thread(target=self.detect_links)
            thread_list.append(t)
        for t in thread_list:
            t.daemon = True
            t.start()
        self.web_links.join()
        if self.keyword_type == SPECIFIED_TEXT:
            for item in self.keyword_links:
                item['associated_text'] = sorted(item['associated_text'])
                item['associated_text'] = ', '.join(item['associated_text'])
        self.keyword_links = sorted(self.keyword_links, key=lambda x: x['associated_text'])
        return (self.keyword_links, self.UOM_sign_links)


@login_required
def search_link(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        keyword = request.POST.get('specifiedText')  # Fetch the keyword if it's provided
        # get user
        user = request.user
        result, token = search_task(url, keyword, user)
        if keyword:
            show_source_link = False
        else:
            show_source_link = True
        request.session['results'] = result
        request.session['token'] = token
        request.session['expiration'] = (datetime.now() + timedelta(minutes=10)).isoformat()
        request.session['show_source_link'] = show_source_link

        return redirect('show_results')
    return render(request, 'search.html')

@login_required
def show_results(request):
    results = request.session.get('results')
    show_source_link = request.session.get('show_source_link')
    token = request.session.get('token')
    return render(request, 'results.html', {'results': results, 'show_source_link': show_source_link, 'token':token})


def search_task(url, keyword, user):
    # Initialize Web_spider instance
    web_spider = Web_spider()

    if keyword:
        results, uom_result = web_spider.search_keyword_links(url, keyword)
    else:
        results, uom_result = web_spider.search_broken_links(url)

    token = download_token.make_token(user)

    download_table(results, "1"+token+".xlsx")
    download_table(uom_result, "2"+token+".xlsx")
    # return results
    return [results, token]


def download_table(results, table_name):
    df = pd.DataFrame(results)
    filename = table_name
    if not os.path.exists('download_table'):
        os.mkdir('download_table')
    path = os.path.join('download_table', filename)
    with pd.ExcelWriter(path, engine='openpyxl') as output:
        df.to_excel(output, index=False, sheet_name='Sheet1')
        worksheet = output.sheets['Sheet1']
        column_widths = {
            'A': 100,
            'B': 100,
            'C': 50
        }
        for col, width in column_widths.items():
            worksheet.column_dimensions[col].width = width
    delete_file_after_timeout(path, timeout=600)

# directory of result xlsx files
BASE_DIR = 'download_table'

# Function to delete the file after a timeout
def delete_file_after_timeout(file_path, timeout):
    # Wait for the timeout (in seconds) and then delete the file
    def delete_file():
        if os.path.exists(file_path):
            os.remove(file_path)

    timer = threading.Timer(timeout, delete_file)
    timer.start()


@login_required
def download(request):
    type = request.GET.get('type')
    token = request.GET.get('token')

    if not type or not token:
        return HttpResponseBadRequest('Invalid File Request')

    filename = type + token + ".xlsx"
    file_path = os.path.join(BASE_DIR, filename)
    canonicalized_path = os.path.abspath(file_path)

    # check canonicalised path starts with expected base dir
    if not canonicalized_path.startswith(os.path.abspath(BASE_DIR)):
        return HttpResponseForbidden("Forbidden")

    # Check if the file exists
    if os.path.exists(file_path):
        # Open the file in binary mode and send it as a response
        with open(file_path, 'rb') as file:
            file_data = file.read()

        # Create a file-like object in memory
        file_in_memory = io.BytesIO(file_data)

        # Serve the file from memory
        response = FileResponse(file_in_memory)
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response
    else:
        return HttpResponseNotFound("File not found.")