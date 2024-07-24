# VERSION: 1.1
#
# LICENSING INFORMATION
# MIT License
#
# Copyright (c) 2024 galaris
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import urllib.parse
import urllib.request
import re
import math
import time
import gzip
from io import BytesIO
from novaprinter import prettyPrinter

class btdig(object):
    url = 'https://www.btdig.com'
    name = 'btdig'
    supported_categories = {'all': '0'}

    def search(self, what, cat='all'): 
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'DNT': '1',
            'Sec-GPC': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'trailers'
        }

        url = f"{self.url}/search?q={urllib.parse.quote(what)}&order=0" # order=0 will order by "relevance"
        response = self.get_response(urllib.request.Request(url, headers=headers))

        results_match = re.search(r'<span style="color:rgb\(100, 100, 100\);padding:2px 10px">(\d+) results found', response)
        if results_match:
            total_results = int(results_match.group(1))
            total_pages = math.ceil(total_results / 10)
        else:
            total_pages = 1 # assuming single page

        self.parse_page(response)

        for page in range(1, total_pages):
            time.sleep(1)  # Sleep for 1 second between requests
            url = f"{self.url}/search?q={urllib.parse.quote(what)}&p={page}&order=0"
            response = self.get_response(urllib.request.Request(url, headers=headers))
            self.parse_page(response)

    def get_response(self, req):
        try:
            with urllib.request.urlopen(req) as response:
                if response.info().get('Content-Encoding') == 'gzip':
                    gzip_file = gzip.GzipFile(fileobj=BytesIO(response.read()))
                    return gzip_file.read().decode('utf-8', errors='ignore')
                return response.read().decode('utf-8', errors='ignore')
        except Exception as e:
            return ""

    def parse_page(self, html_content):
        result_blocks = re.finditer(r'<div class="one_result".*?(?=<div class="one_result"|$)', html_content, re.DOTALL)
        
        for block in result_blocks:
            result = {}
            block_content = block.group(0)
            
            magnet_match = re.search(r'<a href="(magnet:\?xt=urn:btih:[^"]+)"', block_content)
            name_match = re.search(r'<div class="torrent_name".*?><a.*?>(.*?)</a>', block_content, re.DOTALL)
            size_match = re.search(r'<span class="torrent_size"[^>]*>(.*?)</span>', block_content)
            
            desc_link_match = re.search(r'<div class="torrent_name".*?><a href="([^"]+)"', block_content, re.DOTALL) # could implement retrieving further info on torrent later
            
            if magnet_match and name_match and size_match and desc_link_match:
                result['link'] = magnet_match.group(1)
                result['name'] = re.sub(r'<.*?>', '', name_match.group(1)).strip()
                result['size'] = size_match.group(1).strip().replace('&nbsp;', ' ')
                result['desc_link'] = desc_link_match.group(1)
                result['engine_url'] = self.url
                result['seeds'] = '-1'
                result['leech'] = '-1'
                prettyPrinter(result)

