import requests
import re


def get_page_content(url):
    r = requests.get(url)
    html_text = r.text
    return (html_text)


def extract_product_links(content):
    product_url_regex = re.compile(r'<article class="product_pod">.*?<h3>.*?<a href="(.*?)"')
    result = re.findall(product_url_regex, content)
    links = ["https://books.toscrape.com/catalogue/" + x for x in result]
    return links


def get_all_product_links():
    all_product_urls = []

    for page in range(1, 51):
        url = "https://books.toscrape.com/catalogue/page-{}.html".format(page)
        print("Crawelling", url)
        content = get_page_content(url)
        links = extract_product_links(content)
        all_product_urls.extend(links)

    return all_product_urls


def get_product_details(url):
    content = get_page_content(url)
    title_regex = re.compile(r'<h1>(.*?)<h1>')
    result = re.findall(title_regex, content)
    name=result[0]
    product_details_regex=re.compile(r'<table class="table table-striped">(.*?)</table>')
    result=re.findall(product_details_regex , content)
    product_details=result[0]
    upc_regex=re.compile(r'<th>UPC</th>\s*<td>(.*?)</td>')
    result=re.findall(upc_regex,product_details)
    upc=result[0]
    price_regex=re.compile(r'<th>Price \(incl. tax\)</th\s*><td>(.*/)</td>')
    result=re.findall(price_regex,product_details)
    price=result[0]
    print(name,upc,price)


if __name__ == "__main__":
    # url="http://books.toscrape.com/index.html"
    # content=get_page_content(url)
    # links=extract_product_links(content)
    # print(links)
    all_product_urls = get_all_product_links()
    # print(all_product_url[:5])
    # print(len(all_product_url))
    for url in all_product_urls[0:5]:
        try:
            get_product_details(url)
        except:
            print("couldnt scrape",url)
