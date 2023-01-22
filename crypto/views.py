

from django.shortcuts import render
import requests
from requests import Session
import json
from bs4 import BeautifulSoup

#note it uses an api key from config.py which is removed
from financeNews import config

def coinID(cryptocurrency):
    if cryptocurrency == "bitcoin":
        return "1"

    elif cryptocurrency == "ethereum":
        return "1027"
    
    elif cryptocurrency == "bnb":
        return "1839"
    
    elif cryptocurrency == "tether":
        return "825"

    elif cryptocurrency == "dogecoin":
        return "74"

    elif cryptocurrency == "xrp":
        return "52"

    elif cryptocurrency == "tron":
        return "1958"
    
    else:
        return "error"


class CoinMarketCap:
    def __init__(self,apitoken):
        self.url = "https://pro-api.coinmarketcap.com"
        self.headers = {"Accepts":"application/json","X-CMC_PRO_API_KEY": apitoken}
        self.session = Session()
        self.session.headers.update(self.headers)

    def getSymbol(self,slug):
        url = self.url + "/v2/cryptocurrency/quotes/latest"
        parameters = {"slug": slug}
        r = self.session.get(url, params=parameters)
        data = r.json()["data"][coinID(slug)]["symbol"]
        return data

    def priceOfCryptocurrency(self,slug,convert):
        url = self.url + "/v2/cryptocurrency/quotes/latest"
        parameters = {"slug": slug, "convert": convert}
        r = self.session.get(url, params=parameters)
        data = r.json()["data"][coinID(slug)]["quote"][convert]["price"]
        return data

    def percentChange(self,slug,convert):
        url = self.url + "/v2/cryptocurrency/quotes/latest"
        parameters = {"slug": slug, "convert": convert}
        r = self.session.get(url, params=parameters)
        data = r.json()["data"][coinID(slug)]["quote"][convert]["percent_change_1h"]
        return data

    def volume(self,slug,convert):
        url = self.url + "/v2/cryptocurrency/quotes/latest"
        parameters = {"slug": slug, "convert": convert}
        r = self.session.get(url, params=parameters)
        data = r.json()["data"][coinID(slug)]["quote"][convert]["volume_24h"]
        return data
    
    def volumeChange(self,slug,convert):
        url = self.url + "/v2/cryptocurrency/quotes/latest"
        parameters = {"slug": slug, "convert": convert}
        r = self.session.get(url, params=parameters)
        data = r.json()["data"][coinID(slug)]["quote"][convert]["volume_change_24h"]
        return data
    
    def totalSupply(self,slug):
        url = self.url + "/v2/cryptocurrency/quotes/latest"
        parameters = {"slug": slug}
        r = self.session.get(url, params=parameters)
        data = r.json()["data"][coinID(slug)]["total_supply"]
        return data

def scrapeNews(cryptocurrency):
    session = requests.Session()
    
    url_list = []
    scrapedInfo = []

    #determines which url to scrape based on what the cryptocurrency the user entered in from "crypto.html"
    if cryptocurrency == "bitcoin":
        url_list.append("https://www.coindesk.com/markets/2023/01/05/crypto-markets-analysis-on-chain-data-shows-short-term-bitcoin-holders-turning-profits/")
        url_list.append("https://www.coindesk.com/policy/2023/01/06/brother-of-criminal-bitcoin-mixing-ceo-pleads-guilty-to-stealing-712-bitcoins-from-irs/")
        
    elif cryptocurrency == "ethereum":
        url_list.append("https://www.coindesk.com/markets/2023/01/04/ethereum-name-service-recorded-over-28m-domain-registrations-in-2022/")
        url_list.append("https://www.coindesk.com/business/2023/01/04/ethereum-builder-consensys-and-amd-spac-plows-on-despite-95-of-shares-being-redeemed/")

    elif cryptocurrency == "bnb":
        url_list.append("https://www.coindesk.com/markets/2022/12/23/crypto-analysts-see-yellow-flag-in-us-exchanges-refusal-to-list-binances-bnb-token/")
        url_list.append("https://www.coindesk.com/markets/2022/12/13/justin-sun-looks-to-calm-crypto-market-fear-as-bnb-falls-8-withdrawals-continue-on-binance/")
    
    elif cryptocurrency == "tether":
        url_list.append("https://www.coindesk.com/tech/2022/11/12/tether-blacklists-mysterious-ftx-wallets-as-account-drainer-liquidates-matic-link-avax-holdings/")
        url_list.append("https://www.coindesk.com/business/2022/11/10/tether-freezes-46m-of-usdt-following-law-enforcement-request/")
    
    elif cryptocurrency == "dogecoin":
        url_list.append("https://www.coindesk.com/markets/2022/12/20/coinbases-slump-to-all-time-low-sends-market-cap-below-dogecoin/")
        url_list.append("https://www.coindesk.com/markets/2022/11/27/first-mover-asia-dogecoin-surges-16-to-continue-its-holiday-cheer/")
    
    elif cryptocurrency == "xrp":
        url_list.append("https://www.coindesk.com/business/2022/11/29/coinbase-wallet-quietly-delists-bitcoin-cash-ethereum-classic-ripples-xrp-and-stellars-xlm/")
        url_list.append("https://www.coindesk.com/markets/2022/09/30/cryptocurrencies-xrp-mkr-shine-as-btc-eth-hold-steady-ahead-of-us-inflation-figure/")
    
    elif cryptocurrency == "tron":
        url_list.append("https://www.coindesk.com/markets/2023/01/06/tron-price-sinks-8-usdd-depegs-amid-drama-at-justin-sun-related-huobi-crypto-exchange/")
        url_list.append("https://www.coindesk.com/markets/2023/01/04/first-mover-asia-why-is-tron-founder-justin-sun-keeping-some-of-his-coins-in-valkyrie-digital-assets/")
    
    else:
        #if no valid currency is provided an error is returned (honestly it should not go here, since the crypto_view function catches if an invalid coin is entered)
        return "error"

    for i in range(len(url_list)): 
        article_info = []
        scrapeUrl = session.get(url_list[i]).text
        soup = BeautifulSoup(scrapeUrl,"html.parser")
        articleTitle = soup.find("h1",class_="typography__StyledTypography-owin6q-0 fPbJUO").text
        excerpt = soup.find("h2", class_= "typography__StyledTypography-owin6q-0 jPQVef").text
        date = soup.find("span", class_="typography__StyledTypography-owin6q-0 fUOSEs").text
        category = soup.find("span", class_="typography__StyledTypography-owin6q-0 kjyoaM").text

        article_info.append(url_list[i])
        article_info.append(articleTitle)
        article_info.append(excerpt)
        article_info.append(date)
        article_info.append(category)
        scrapedInfo.append(article_info)

    return scrapedInfo

def crypto_view(request):

    #NEED TO UNCOMMENT THIS IF YOU WANT TO SEE CRYPTO INFORMATION
    coin_info = CoinMarketCap(config.api_key)

    context = {}

    #from the front end in "crypto.html" it allows the user to pass in a crypto coin and a type of currency
    if "cryptocurrency" and "convert" in request.GET:

        #forces the entry to be a lower case because the slug of the cryptocurrency has to be all lower case
        cryptocurrency = request.GET.get("cryptocurrency").lower()
        
        #forces the entry to be all uppercase because the convert parameter has to be all uppercase
        convert = request.GET.get("convert").upper()

        checkInput = coinID(cryptocurrency)
        
        if checkInput == "error":
            context['error'] = "Please enter one of the coins listed above"
        
        else:
            #UNCOMMENT THIS WHEN YOU WANT TO SEE CRYPTO INFORMATION
            symbol = coin_info.getSymbol(cryptocurrency)
            price = coin_info.priceOfCryptocurrency(cryptocurrency,convert)
            percentChange = coin_info.percentChange(cryptocurrency,convert)
            volume = coin_info.volume(cryptocurrency, convert)
            volumeChange = coin_info.volumeChange(cryptocurrency,convert)
            totalSupply = coin_info.totalSupply(cryptocurrency)

            
            context['cryptocurrency'] = cryptocurrency.capitalize()
            context['symbol'] = symbol
            context['convert'] = convert
            context['price'] = price
            context['percentChange'] = percentChange
            context['volume'] = volume
            context['volumeChange'] = volumeChange
            context['totalSupply'] = totalSupply

            #allows us to pass multiple news information to the front end (crypto.html)
            scrapedInfo = scrapeNews(cryptocurrency)
            counter = 0
            for articleInfo in scrapedInfo:
                counter += 1
                context[('url'+str(counter))] = articleInfo[0]
                context[('articleTitle'+str(counter))] = articleInfo[1]
                context[('excerpt'+str(counter))] = articleInfo[2]
                context[('date'+str(counter))] = articleInfo[3]
                context[('category'+str(counter))] = articleInfo[4]
            
        
    return render(request, 'crypto/crypto.html', context)
    
