import dateutil.parser
import scrapy
from scrapy.crawler import CrawlerProcess

from items import Appearance, Disc
from pipeline import Sqlite3Pipeline

from tqdm import tqdm

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
        broadcast_time = dateutil.parser.parse(time_str)

        yield Appearance(
            id=appearance_id,
            broadcast_time=broadcast_time,
            guest_name=guest_name,
        )

        for i, music_section in enumerate(response.css('.segments-list__item--music')):
            track = music_section.css('.segment__track')
            artist = track.css('.artist')

            yield Disc(
                appearance_id=appearance_id,
                artist=artist.css('::text').get() if artist else None,
                title=track.css('p > span::text').get(),
                position=i,
            )

        next_page = response.css('a[data-bbc-title="next:title"]::attr("href")').get()
        if next_page is not None:
            progress_bar = response.meta.get('progress_bar') or tqdm(total=3227)
            progress_bar.update(1)
            yield response.follow(next_page, self.parse, meta={'progress_bar': progress_bar})


if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'LOG_LEVEL': 'WARN',
    })

    process.crawl(DIDScraper)
    process.start()
