# Python built-in libraries
import os, re
from urllib.parse import unquote

# 3rd party libraries
import requests
from bs4 import BeautifulSoup

# Own code
from ..utils import create_dir_recursively


def download_html(url: str, path_save_to: str) -> None:
    response = requests.get(url)
    with open(path_save_to, 'wb') as html:
        html.write(response.content)


def get_soup(html_index_path: str) -> BeautifulSoup:
    with open(html_index_path, 'r', encoding='utf-8') as html:
        return BeautifulSoup(html.read(), 'html.parser')


def download_fonts(base_url: str, html_index_path: str, folder_save_to: str = None, force_download: bool = False, debug: bool = False):
    # @font-face {  font-family: YAE5fD6jXa8-0;  src: url(fonts/668e204ecea8e06c27fb74af58a48107.woff2);  font-weight: 900;  font-style: normal;}
    pattern = r'(?:@font-face {)(?:.*?)(?:src: url\()(?P<font_url>[a-zA-Z0-9.\/:\-_]+)(?:\);(?:.*?);})'
    with open(html_index_path, 'r', encoding='utf-8') as html_raw:
        html_doc = html_raw.read()
        matches = re.findall(pattern, html_doc)
        fonts = list(set(matches))  # Get unique values
        if debug:
            print(fonts)
    for i in range(len(fonts)):
        font = fonts[i]
        if folder_save_to != None:
            filepath = os.path.join(folder_save_to, font)
        else:
            filepath = font
        if os.path.exists(filepath) == False or force_download:
            print(f'Font {i+1} of {len(fonts)}: Downloading...')
            response = requests.get(f'{base_url}/{font}')
            folder, filename = os.path.split(filepath)
            if folder != '':
                create_dir_recursively(folder)
            open(filepath, "wb").write(response.content)
        else:
            print(f'Font {i+1} of {len(fonts)}: Skipped. Already downloaded.')

def remove_all_inline_scripts(soup: BeautifulSoup, html_index_path: str):
    for elem in soup.find_all('script'):
        elem.clear()
    with open(html_index_path, 'w', encoding='utf-8') as html:
        html.write(str(soup))


def remove_inline_scripts_containing_keywords(soup: BeautifulSoup, html_index_path: str, keywords: list[str]):
    for elem in soup.find_all('script'):
        for keyword in keywords:
            if keyword in elem.text:
                elem.clear()
                break
    with open(html_index_path, 'w', encoding='utf-8') as html:
        html.write(str(soup))


def prepare_web_folder(folder: str):
    if not os.path.exists(folder):
        create_dir_recursively(folder)


def download_local_resources(base_url: str, soup: BeautifulSoup, folder_save_to: str = None, force_download: bool = False):
    resources = {
        "link": "href", # head
        "img": "src",
        "video": "src",
        "image": "href", # images inside svg vectors
        "script": "src",
    }
    for tag, attribute in resources.items():
        elements = soup.find_all(tag)
        for i in range(len(elements)):
            base_msg = f'<{tag}> {i+1} of {len(elements)}'
            elem = elements[i]
            try:
                resource_path: str = elem[attribute]
                if resource_path.startswith('/'):
                    resource_path = resource_path[1:]
                # We only care about resources that are local to the website we
                # are downloading.
                if not resource_path.startswith('http'):
                    if folder_save_to != None:
                        filepath = os.path.join(folder_save_to, resource_path)
                    else:
                        filepath = resource_path
                    if os.path.exists(filepath) == False or force_download:
                        print(f'{base_msg}: Downloading...')
                        response = requests.get(f"{base_url}/{resource_path}")
                        folder, filename = os.path.split(filepath)
                        if folder != '':
                            create_dir_recursively(folder)
                        with open(filepath, 'wb') as f:
                            f.write(response.content)
                    else:
                        print(f'{base_msg}: Skipped. It is already downloaded. File: {filepath}')
                else:
                    print(f'{base_msg}: Ignored. It is an external resource.')
            except KeyError:
                print(f"{base_msg}: Ignored. It has no '{attribute}' attribute.")


def fix_links(soup: BeautifulSoup, html_index_path: str):
    pattern = r'^(?:.+?)?(?:\/_link\/\?link=)(?P<link>.+?)(?:&(?:amp;)?target=.*)$'
    compiled_pattern = re.compile(pattern)
    a_elements = soup.find_all('a')
    for elem in a_elements:
        try:
            link: str = elem["href"]
            match = re.match(compiled_pattern, link)
            if match != None:
                new_link = unquote(match.groupdict()["link"])
                match = re.match(compiled_pattern, new_link)
                if match != None:
                    new_link = unquote(match.groupdict()["link"])
                elem["href"] = new_link
        except KeyError:
            # Nothing to fix in link because it has no href attribute.
            pass
    with open(html_index_path, 'w', encoding='utf-8') as html:
        html.write(str(soup))


def download_full_site(url: str, folder: str = None, force_download: bool = False):
    site_folder = os.path.join('sites', folder)
    index_path = os.path.join(site_folder, 'index.html')
    prepare_web_folder(site_folder)
    download_html(url, index_path)
    download_fonts(url, index_path, site_folder, force_download)
    soup = get_soup(index_path)
    download_local_resources(url, soup, site_folder, force_download)
    fix_links(soup, index_path)
    remove_inline_scripts_containing_keywords(
        soup,
        index_path, 
        keywords=["modal_backdrop"])
