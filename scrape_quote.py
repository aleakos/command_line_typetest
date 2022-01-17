from bs4 import BeautifulSoup
import requests, string, random


def scrape_and_clean(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, features="lxml")

    # get quotes from page
    div_quotes = soup(
        "div", attrs={"class": "quoteText"}
    )  # soup("div") == soup.find_all("div")
    quotes = []
    for q in div_quotes:
        quote = ""
        # turn multiline quotes/poems into a single string
        for i in range(len(q.contents)):
            line = q.contents[i].encode("ascii", errors="ignore").decode("utf-8")
            if line[0] == "<":  # is tag, ignore characters that aren't part of quote
                break
            else:
                quote += line

        quote = quote.replace("\n", " ").replace("\r", "").strip()
        quotes.append(quote)

    return quotes


def generate_goodreads_url():
    page_number = random.randint(1, 100)
    return f"https://www.goodreads.com/quotes?page={page_number}"


def get_quote():
    url = generate_goodreads_url()
    quotes = scrape_and_clean(url)
    quote_count = len(quotes) - 1

    return quotes[random.randint(0, quote_count)]
