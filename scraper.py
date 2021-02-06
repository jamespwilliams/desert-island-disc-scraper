from datetime import datetime
import scrapy
from scrapy.crawler import CrawlerProcess

from items import Appearance, Disc
from pipeline import Sqlite3Pipeline

class DIDScraper(scrapy.Spider):
    name = 'desert_island_discs'
    start_urls = [
        'https://www.bbc.co.uk/programmes/p009y0nq',
    ]

    custom_settings = {
        'ITEM_PIPELINES': {
            Sqlite3Pipeline: 500,
        },
    }

    def parse(self, response):
        appearance_id = response.request.url.split("/")[-1]

        episode_box = response.css('.map--episode')
        guest_name = episode_box.css('h1::text').get()

        time_str = response.css('.broadcast-event__time::attr("content")').get()
        broadcast_time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S%z')

        yield Appearance(
            id=appearance_id,
            broadcast_time=broadcast_time,
            guest_name=guest_name,
        )

        for music_section in response.css('.segments-list__item--music'):
            track = music_section.css('.segment__track')
            artist = track.css('.artist')

            yield Disc(
                appearance_id=appearance_id,
                artist=artist.css('::text').get() if artist else None,
                title=track.css('p > span::text').get(),
            )

        next_page = response.css('a[data-bbc-title="next:title"]::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(DIDScraper)
    process.start()
