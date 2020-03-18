# -*- coding: utf-8 -*-
import scrapy


class OpcvmSpider(scrapy.Spider):
    name = 'opcvm'
    allowed_domains = ['boursorama.com']

    custom_settings = {
        'FEED_URI': 'boursorama_opcvm.jl',

        # 'CLOSESPIDER_ITEMCOUNT': 5,
        # 'CLOSESPIDER_PAGECOUNT': 5,
        # 'LOG_LEVEL': 'DEBUG',

        'DOWNLOAD_DELAY': 0.5,
        'CONCURRENT_REQUESTS': 5,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 5,
        'DOWNLOAD_TIMEOUT': 20,
        'ROBOTSTXT_OBEY': False,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
    }

    def start_requests(self):
        for page in range(1, 43 + 1):
            if page == 1:
                yield scrapy.Request('https://www.boursorama.com/bourse/opcvm/recherche/?fundSearch%5Bclasse%5D=all&fundSearch%5Bcritgen%5D=all&fundSearch%5Bsaving%5D=1', self.parse_opcvm_list)

            yield scrapy.Request('https://www.boursorama.com/bourse/opcvm/recherche/page-' + str(page) + '?fundSearch%5Bclasse%5D=all&fundSearch%5Bcritgen%5D=all&fundSearch%5Bsaving%5D=1', self.parse_opcvm_list)

    def parse_opcvm_list(self, response):
        for a in response.css("#main-content > div > div > div.l-basic-page__sticky-container > div.l-basic-page__main > div.c-block > div.c-block__body > section > :nth-child(4) > div.o-gutter-bottom > div > div.u-relative > div > table > tbody > tr > td.c-table__cell.c-table__cell--dotted.u-text-uppercase > div > div.o-pack__item.u-ellipsis > a"):
            url = a.css('::attr(href)').get()

            yield response.follow(url, self.parse_opcvm, meta={'url_identifier': url.split('/')[-2]})

    def parse_opcvm(self, response):
        fields_selectors = {
            "nom": ".c-faceplate__company-link",
            "devise": ".c-faceplate__price-currency",
            "identifiant": ".c-faceplate__isin",

            "actif net": "#main-content > div > section.l-quotepage > header > div > div > div.c-faceplate__data.c-faceplate__data-min-height-18 > div:nth-child(1) > div > ul > li:nth-child(2) > p.c-list-info__value.u-color-big-stone",

            "date de création": ".c-fund-characteristics > div > div.c-block__body > div.c-list-info.c-list-info--bottom-separator.c-list-info--nopadding-top > ul > li:nth-child(1) > p.c-list-info__value",
            "société de gestion": ".c-fund-characteristics > div > div.c-block__body > div.c-list-info.c-list-info--bottom-separator.c-list-info--nopadding-top > ul > li:nth-child(2) > p.c-list-info__value > a",
            "groupe de gestion": ".c-fund-characteristics > div > div.c-block__body > div.c-list-info.c-list-info--bottom-separator.c-list-info--nopadding-top > ul > li:nth-child(4) > p.c-list-info__value > a",
            "catégorie Morningstar": "#main-content > div > section > div.l-quotepage__sticky-container > article > div.l-quotepage__main-head > div:nth-child(3) > div.o-grid__item.u-7\/12\@sm-min > div.c-fund-characteristics > div > div.c-block__body > div:nth-child(2) > ul > li:nth-child(2) > p.c-list-info__value.c-list-info__value--color-brand > a",
            "forme juridique": ".c-fund-characteristics > div > div.c-block__body > div.c-list-info.c-list-info--nopadding-bottom > ul > li:nth-child(1) > p.c-list-info__value",
            "affectation des résultats": ".c-fund-characteristics > div > div.c-block__body > div.c-list-info.c-list-info--nopadding-bottom > ul > li:nth-child(3) > p.c-list-info__value",
            "fonds de fonds": ".c-fund-characteristics > div > div.c-block__body > div.c-list-info.c-list-info--nopadding-bottom > ul > li:nth-child(5) > p.c-list-info__value",

            "frais d'entrée": "#main-content > div > section > div.l-quotepage__sticky-container > article > div.l-quotepage__main-head > div.c-costs-conditions > div > div.c-block__body > table > tbody > tr:nth-child(1) > td.c-table__cell.c-table__cell--to-list.c-table__cell--h-large.c-table__cell--wrap.c-table__cell--dotted.c-table__cell--bkg-colored.\/.c-costs-conditions__cell.\/.u-text-right",
            "frais de sortie": "#main-content > div > section > div.l-quotepage__sticky-container > article > div.l-quotepage__main-head > div.c-costs-conditions > div > div.c-block__body > table > tbody > tr:nth-child(2) > td.c-table__cell.c-table__cell--to-list.c-table__cell--h-large.c-table__cell--wrap.c-table__cell--dotted.c-table__cell--bkg-colored.\/.c-costs-conditions__cell.\/.u-text-right",
            "frais courants": "#main-content > div > section > div.l-quotepage__sticky-container > article > div.l-quotepage__main-head > div.c-costs-conditions > div > div.c-block__body > table > tbody > tr:nth-child(3) > td.c-table__cell.c-table__cell--to-list.c-table__cell--h-large.c-table__cell--color-light.c-table__cell--wrap.c-table__cell--dotted.\/.c-costs-conditions__cell.\/.u-text-right",
            "souscription min. initiale": "#main-content > div > section > div.l-quotepage__sticky-container > article > div.l-quotepage__main-head > div.c-costs-conditions > div > div.c-block__body > div.c-list-info.c-list-info--bottom-separator > ul > li:nth-child(1) > p.c-list-info__value",
        }

        data = {'url_identifier': response.meta['url_identifier']}
        for field, selector in fields_selectors.items():
            value = response.css(selector + "::text").get()

            if isinstance(value, str):
                value = value.strip()

            data[field] = value

        yield data

    class ScrapedItem(scrapy.Item):
        f = scrapy.Field()

        def __str__(self):
            return "<ScrapedItem>"
