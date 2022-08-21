import requests
from bs4 import BeautifulSoup

RHYME_URL = "https://brachot.net/rhymes.php"


def give_rhymes(word: str) -> list:
    """
    The function returns 10 rhymes
    :return: list of rhymes
    """
    data = requests.get(f"{RHYME_URL}?q={word}")
    soup = BeautifulSoup(data.content)
    res = soup.find_all('head')[0].find_all('meta',{"name": "description"})[0].attrs['content'].replace(',','').split()
    return res[9:-1]

# print(give_rhymes("נכון"))
