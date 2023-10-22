import asyncio
import logging

import aiohttp
from bs4 import BeautifulSoup
from urlextract import URLExtract
import lxml
import re

data_market = set()
urls_market_dict = {
    'BK': 'https://carte.by/grodno/burger-king-delivery/',
    'woksushi': 'https://woksushi.by/',
    'pizzahome': 'https://pizzahome.by/menu/akczii/',
    'dominos': 'https://dominos.by/discount_campaign/',
    'hot-dog-family': 'https://carte.by/grodno/hot-dog/',
    'faradey': 'https://carte.by/grodno/faraday-delivery/',
    'shaw-books': 'https://carte.by/grodno/shawbooks-sov-delivery/',
}


async def get_page_data(session, market):
    async with session.get(url=market) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        if market == 'https://carte.by/grodno/burger-king-delivery/':
            market_name = ('BK',)

            name_coupons = soup.find_all('a', class_="ddish__url")
            name_coupons_list = [i.text.strip() for i in name_coupons[1:-7]]

            price_product = soup.find_all('div', class_='ddish__sum')
            price_coupons_gen = (i.text.strip() for i in price_product[1:-7])

            images = soup.find_all(src=re.compile("assets"))
            images_action_list = [image['src'] for image in images[1:-7]]

            content_combo_list = ['' for i in range(len(name_coupons_list))]
            burger_king_data = zip(name_coupons_list, content_combo_list, price_coupons_gen,
                                   images_action_list, market_name * len(name_coupons_list))

            data_market.add(burger_king_data)

        elif market == 'https://woksushi.by/':
            market_name = ('woksushi',)
            name_combo = soup.find(attrs={"data-id": "30"}).find_all('a', class_='ddish__name')
            name_combo_list = [name.text for name in name_combo]
            image_combo_gen = (image.get('data-full') for image in soup.find(attrs={"data-id": "30"}).select('img'))

            content_combo = soup.find(attrs={"data-id": "30"}).find_all('div', class_='ddish__ingredients')
            content_combo_gen = (content.text.replace('\n', '') for content in content_combo)

            price_combo = soup.find(attrs={"data-id": "30"}).find_all('div', class_='ddish__sum')
            price_combo_gen = (price.text.strip() for price in price_combo)

            data_woksushi = zip(name_combo_list, content_combo_gen, price_combo_gen, image_combo_gen,
                                market_name * len(name_combo_list))
            data_market.add(data_woksushi)

        elif market == 'https://pizzahome.by/menu/akczii/':
            market_name = ('pizzahome',)
            name_action = soup.find('ul', class_="products columns-4").find_all('h2', class_='woocommerce-loop'
                                                                                             '-product__title')
            name_action_list = [name.text.strip() for name in name_action]

            content_action = soup.find_all('div', class_="product-description")
            content_action_gen = (content.text.replace('\n', '') for content in content_action)

            image_action = soup.find_all('img',
                                         class_='attachment-woocommerce_thumbnail size-woocommerce_thumbnail')
            image_action_gen = (image.get('src') for image in image_action)

            price_action = soup.find_all('span', class_='badge big_sale')
            price_action_gen = (price_action[price].text.replace('Цена со скидкой', '') for price in
                                range(len(price_action) + 1) if
                                price % 2 != 0)

            data_pizzahome = zip(name_action_list, content_action_gen, price_action_gen,
                                 image_action_gen, market_name * len(name_action_list))
            data_market.add(data_pizzahome)

        elif market == 'https://dominos.by/discount_campaign/':
            market_name = ('dominos',)
            name_price_action = soup.find_all('div', class_='info-card__content-title')
            name_price_action_list = [price.text for price in name_price_action]

            extractor = URLExtract()
            image_action = soup.find_all('div', class_='info-card__media-wrapper')
            image_action_gen = (image.get('style') for image in image_action)
            image_action_gen_rez = (",".join(extractor.find_urls(i)) for i in image_action_gen)

            content_action = soup.find_all('div', class_='info-card__content-description')
            content_action_gen = (content.text for content in content_action)

            data_dominos = zip(name_price_action_list, content_action_gen, image_action_gen_rez,
                               market_name * len(name_price_action))
            data_market.add(data_dominos)

        elif market == 'https://carte.by/grodno/hot-dog/':
            market_name = ('hot-dog-family',)

            name_action_zapek = soup.find_all('div', class_='cmdish__name')
            name_action_list = [name.text.strip() for name in name_action_zapek[:4]]

            content = soup.find_all('div', class_='cmdish__ingredients')

            name_content_list = [cont.text.strip() for cont in content[:4]]

            prices = soup.find_all('div', class_='cmdish__price')

            price_action_list = [price.text.strip() for price in prices[:4]]

            images = soup.find_all(href=re.compile("assets"))

            images_action_list = [image['href'] for image in images[:4]]
            data_family = zip(name_action_list, name_content_list, price_action_list,
                              images_action_list, market_name * len(name_action_list))
            data_market.add(data_family)

        elif market == 'https://carte.by/grodno/faraday-delivery/':
            market_name = ('faradey',)
            name_products = soup.find_all('div', class_='ddish__name')
            name_product_list = [name.text.strip() for name in name_products[:8]]

            content_products = soup.find_all('div', class_='ddish__ingredients')
            content_product_list = [content.text.strip() for content in content_products[:8]]

            price_products = soup.find_all('div', class_='ddish__sum')
            price_product_list = [price.text.strip() for price in price_products[:8]]

            images = soup.find_all(src=re.compile("assets"))
            images_action_list = [image['src'] for image in images[1:9]]
            faradey = zip(name_product_list, content_product_list, price_product_list,
                          images_action_list, market_name * len(name_product_list))
            data_market.add(faradey)

        elif market == 'https://carte.by/grodno/shawbooks-sov-delivery/':
            market_name = ('shaw-books',)
            name_products = soup.find_all('div', class_='ddish__name')
            name_product_list = [name.text.strip() for name in name_products[1:13]]

            content_products = soup.find_all('div', class_='ddish__ingredients')
            content_product_list = [content.text.strip() for content in content_products[1:13]]

            price_products = soup.find_all('div', class_='ddish__sum')
            price_product_list = [price.text.strip() for price in price_products[1:13]]

            images = soup.find_all(src=re.compile("assets"))
            images_action_list = [image['src'] for image in images[2:13]]
            shaw_books = zip(name_product_list, content_product_list, price_product_list,
                             images_action_list, market_name * len(name_product_list))
            data_market.add(shaw_books)


async def gather_data():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for market in urls_market_dict.values():
            task = asyncio.create_task(get_page_data(session, market))
            tasks.append(task)
        await asyncio.gather(*tasks)


def parser():
    try:
        asyncio.run(gather_data())
        return data_market
    except aiohttp.ClientConnectorError as ClientConnectorError:
        logging.basicConfig(level=logging.ERROR, filename="erors_log.log", filemode="a",
                            format="%(asctime)s %(levelname)s %(message)s")
        logging.error('aiohttp.ClientConnectorError', exc_info=False)


if __name__ == '__main__':
    parser()
