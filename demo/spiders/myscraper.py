import scrapy


class LibrarythingSpiderSpider(scrapy.Spider):
    name = "librarything_spider"
    allowed_domains = ["www.librarything.com"]
    start_urls = ["https://www.librarything.com/topic/341827"]

    items_count = 0
    max_items = 1500  # Đặt giới hạn cao hơn, ví dụ 1500 dòng

    def parse(self, response):
        posts = response.xpath('//*[starts-with(@id, "mh")]')

        for post in posts:
            if self.items_count >= self.max_items:
                return

            post_id = post.xpath('@id').get()
            content_id = "mg" + post_id[2:]  # Chuyển 'mh...' thành 'mg...'

            yield {
                'author': post.xpath('./span/a/text()').get(),
                'date': post.xpath('./div/text()').get(),
                'content': ' '.join(response.xpath(f'//*[@id="{content_id}"]//text()').getall()).strip(),
            }

            self.items_count += 1

        if self.items_count < self.max_items:
            next_page = response.xpath('//a[@class="next"]/@href').get()
            if next_page:
                yield response.follow(next_page, self.parse)
