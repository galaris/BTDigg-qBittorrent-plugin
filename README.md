# BTDigPlugin for qBittorrent

![BTDig qBittorrent plugin](https://github.com/user-attachments/assets/c809f550-96e1-4959-9c09-51ccb4b8ad1d)

This repository contains the BTDig search plugin for qBittorrent, implemented according to the [qBittorrent search plugin guidelines](https://github.com/qbittorrent/search-plugins/wiki/How-to-write-a-search-plugin).

## Features

- Integrates [BTDig](http://btdig.com) search functionality into qBittorrent
- Handles pagination (10 results / page)
- Implements a 1-second delay between page retrievals to avoid overloading the server, BTDig doesn't seem to like scripts, and historically blocks some.

## Implementation Details

- The plugin parses the following information for each torrent:
  - Torrent name
  - Magnet link
  - File size
- Seeders and leechers information is not provided by BTDig, so these values are set to -1 as per qBitorrent's specification.

## Usage

1. Download the plugin file from this repository
2. In qBittorrent, go to Search
3. Click on the "Search plugins" button
4. Click "Install a new one" and select the plugin file
5. The BTDig search option should now be available in your qBittorrent search engine list

## Note

This plugin uses [BTDig](http://btdig.com), which is based on the [DHT Crawler](https://github.com/btdig/dhtcrawler2) project. For more information about the underlying technology, visit their GitHub repository.

## Contributing

Contributions, issues, and feature requests are welcome.

## License

MIT License

Copyright (c) 2024 galaris

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
