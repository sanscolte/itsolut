import random
import time

import requests
from django.core.management import BaseCommand
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType

from api.models import Author, Advt


class Command(BaseCommand):
    help = 'Parse ads from farpost.ru'

    def handle(self, *args, **options):
        base_url: str = 'https://www.farpost.ru'
        url: str = base_url + '/vladivostok/service/construction/guard/+/Системы+видеонаблюдения/'

        proxies = self.get_proxies()
        proxy = random.choice(proxies)
        driver = self.get_driver_with_proxy(proxy)

        driver.get(url)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        ads = soup.select('tr.bull-list-item-js')[:10]

        for position, ad in enumerate(ads, start=1):
            title_tag = ad.select_one('.bulletinLink')
            href = base_url + title_tag.get('href')

            title = title_tag.get_text(strip=True)
            author_name = self.parse_author(href)
            views_tag = ad.select_one('span.views')
            views_text = views_tag.get_text(strip=True) if views_tag else "0"
            views = int(views_text) if views_text else 0

            if title and author_name:
                author, _ = Author.objects.get_or_create(name=author_name)
                advt, created = Advt.objects.get_or_create(
                    title=title,
                    author=author,
                    views=views,
                    position=position,
                )

                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully added advertisement {title} by {author_name}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.NOTICE(
                            f'Advertisement {title} by {author_name} already exists'
                        )
                    )

            else:
                self.stdout.write(
                    self.style.ERROR(
                        f'Parser error: no advertisement title and author'
                    )
                )

        driver.quit()

    def parse_author(self, url):
        proxies = self.get_proxies()
        proxy = random.choice(proxies)
        driver = self.get_driver_with_proxy(proxy)

        driver.get(url)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        author_tag = soup.select_one('span.userNick')
        author_name = author_tag.get_text(strip=True)

        driver.quit()

        return author_name

    def get_driver_with_proxy(self, proxy):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        proxy_options = Proxy()
        proxy_options.proxy_type = ProxyType.MANUAL
        proxy_options.http_proxy = proxy
        proxy_options.ssl_proxy = proxy

        chrome_options.Proxy = proxy_options
        driver = webdriver.Chrome(options=chrome_options)

        return driver

    def get_proxies(self):
        # Возвращает список прокси-серверов в формате IP:PORT
        url = 'https://www.proxy-list.download/api/v1/get?type=https'
        response = requests.get(url)
        proxies = response.text.split('\r\n')
        return proxies
