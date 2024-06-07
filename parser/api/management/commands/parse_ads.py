import random
import time
from typing import List

import requests
from django.core.management import BaseCommand  # type: ignore
from bs4 import BeautifulSoup, Tag
from requests import Response
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.proxy import Proxy, ProxyType

from api.models import Author, Advt


class Command(BaseCommand):
    """Класс команды для парсинга последних 10 объявлений"""

    help = "Parse ads from farpost.ru"

    def handle(self, *args, **options) -> None:
        """Функция для парсинга последних 10 объявлений"""
        base_url: str = "https://www.farpost.ru"
        url: str = (
            base_url
            + "/vladivostok/service/construction/guard/+/Системы+видеонаблюдения/"
        )

        proxies: List[str] = self.get_proxies()
        proxy: str = random.choice(proxies)
        driver: WebDriver = self.get_driver_with_proxy(proxy)

        driver.get(url)
        time.sleep(5)

        soup: BeautifulSoup = BeautifulSoup(driver.page_source, "html.parser")
        ads: List[Tag] = soup.select("tr.bull-list-item-js")[:7]

        for position, ad in enumerate(ads, start=1):
            title_tag: Tag | None = ad.select_one(".bulletinLink")
            href: str = base_url + title_tag.get("href")  # type: ignore

            title: str = title_tag.get_text(strip=True)
            author_name: str = self.parse_author(href)
            views_tag: Tag | None = ad.select_one("span.views")
            views_text: str = views_tag.get_text(strip=True) if views_tag else "0"
            views: int = int(views_text) if views_text else 0

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
                            f"Successfully added advertisement "
                            f"{title} by {author_name}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.NOTICE(
                            f"Advertisement {title} by " f"{author_name} already exists"
                        )
                    )

            else:
                self.stdout.write(
                    self.style.ERROR("Parser error: no advertisement title and author")
                )

        driver.quit()

    def parse_author(self, url) -> str:
        """
        Функция получения имени автора объявления
        :param url: URL объявления
        :return: Имя автора объявления
        """
        proxies: List[str] = self.get_proxies()
        proxy: str = random.choice(proxies)
        driver: WebDriver = self.get_driver_with_proxy(proxy)

        driver.get(url)
        time.sleep(5)

        soup: BeautifulSoup = BeautifulSoup(driver.page_source, "html.parser")
        author_tag: Tag | None = soup.select_one("span.userNick")
        author_name: str = author_tag.get_text(strip=True)

        driver.quit()

        return author_name

    def get_driver_with_proxy(self, proxy) -> WebDriver:
        """
        Функция для получения драйвера
        :param proxy: Один прокси
        :return: Драйвер
        """
        chrome_options: Options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        proxy_options: Proxy = Proxy()
        proxy_options.proxy_type = ProxyType.MANUAL
        proxy_options.http_proxy = proxy
        proxy_options.ssl_proxy = proxy

        chrome_options.Proxy = proxy_options
        driver: WebDriver = webdriver.Chrome(options=chrome_options)

        return driver

    def get_proxies(self) -> List[str]:
        """
        Функция для получения списка прокси
        :return: Список прокси
        """
        url: str = "https://www.proxy-list.download/api/v1/get?type=https"
        response: Response = requests.get(url)
        proxies: List[str] = response.text.split("\r\n")
        return proxies
