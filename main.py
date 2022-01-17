import readchar
from colorama import init, Fore, Back, Style
import time

from bs4 import BeautifulSoup
import requests, string, random

init(autoreset=True)

PADDING = "                             "
CHAR_IN_WORD = 5

# status generator
def start_sequence():
    """ iterate from 0 to total and show progress in console """
    for i in range(3, -1, -1):
        if i == 0:
            out = "!!!!!!!GO!!!!!!!    "
        else:
            out = f"<-----{i}----->    "

        if i < 3:
            out = "\r" + out
        print(out, end="")
        time.sleep(0.5)


def start_game(sentence):
    user_input = ""
    style_string(sentence, user_input)

    while sentence != user_input:
        x = readchar.readkey()

        if x == "\x7f":
            user_input = user_input[:-1]

        elif len(x) > 1:
            pass

        else:
            user_input += x

        style_string(sentence, user_input)

        if len(user_input) > len(sentence) + len(PADDING):
            print("\nWe don't have this kind of space.. goodbye")
            break


def style_string(original, user_input):
    string = ""

    buffer = len(user_input) - len(original)

    # if buffer > 0 we need to concatenate the incorrect letters to the end of the string
    if buffer > 0:
        active_string = original + user_input[-buffer::] + PADDING
        compare = user_input[:-buffer] + " " * buffer
    else:
        active_string = original + PADDING
        compare = user_input

    count = len(user_input)

    for i in range(len(active_string)):
        # start the carriage at 0 at the start of each new loop
        if i == 0:
            print("\r", end="")

        if i == len(compare):
            ele = Style.BRIGHT + active_string[i]
        else:
            ele = active_string[i]
            if i > count:
                ele = Style.DIM + ele
            elif i >= len(compare):
                ele = Fore.RED + ele
            elif active_string[i] == compare[i]:
                ele = Fore.GREEN + ele
            elif active_string[i] != compare[i]:
                ele = Fore.RED + ele

        print(ele, end="")


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


if __name__ == "__main__":
    sentence = get_quote()
    print(sentence)
    # start_sequence()
    # total_chracters = len(sentence) + 1

    # start = time.time()
    # start_game(sentence)

    # time_to_type = time.time() - start
    # print("\n")

    # print(f"WORDS PER MINUTE: {(total_chracters/CHAR_IN_WORD * 60/time_to_type):.2f} ")

