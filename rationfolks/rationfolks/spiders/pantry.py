import scrapy
from ..items import RationfolksItem


class AmazonSpider(scrapy.Spider):
    name = "pantries"

    page_number = 2 

    i = 1
    start_urls = [
        'https://www.amazon.in/s?i=grocery&srs=9574332031&rh=n%3A9574332031%2Cn%3A4859750031&page=2&_encoding=UTF8&pf_rd_p=9199e4e5-3094-492b-97b3-c6aa62add99c&pf_rd_r=R1SHMZ09MEQND3F6YV33&pf_rd_s=pantry-subnav-flyout-content-3&pf_rd_t=SubnavFlyout&qid=1621785069&rw_html_to_wsrp=1&ref=sr_pg_2',
    ]

    def parse(self, response):
        items = RationfolksItem()
        all_div_items = response.css(
            'div.s-result-item div.a-section.a-spacing-medium')[:-1]
        print("\ntotal items: ",len(all_div_items))
        for item in all_div_items:
            if item:
                image = item.css('.s-image::attr(src)').extract()
                title = item.css(
                    '.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-4 .a-link-normal .a-color-base::text').extract()
                
                if title and ',' in title[0]:
                    print(title[0])
                    middle = title[0].split(',')
                    title = middle[0]
                    weight = middle[1]
                else:
                    weight = [''] 
                
                price = item.css(
                    '.a-price .a-offscreen::text').extract()

                additional_info = item.css(
                    '.a-size-base.a-color-secondary::text').extract()
                
                
                if len(price) > 1:
                    mrp = [str(price[1])]
                    price = [str(price[0])]
                elif len(price):
                    mrp = ['']
                    price = [str(price[0])]

                print()
                items['sno'] = AmazonSpider.i
                items['title'] = title
                items['weight'] = weight
                items['price'] = price
                items['mrp'] = mrp
                items['additional_info'] = additional_info
                items['image'] = image
                
                print("image", image)
                print("title", title)
                print("weight", weight)
                print("price", price)
                print("additional_info", additional_info)
                print("mrp", mrp)

                yield items

                AmazonSpider.i += 1

        while AmazonSpider.page_number < 4:
            next_page = 'https://www.amazon.in/s?i=grocery&srs=9574332031&rh=n%3A9574332031%2Cn%3A4859750031&page=2&_encoding=UTF8&pf_rd_p=9199e4e5-3094-492b-97b3-c6aa62add99c&pf_rd_r=R1SHMZ09MEQND3F6YV33&pf_rd_s=pantry-subnav-flyout-content-3&pf_rd_t=SubnavFlyout&qid=1621785069&rw_html_to_wsrp=1&ref=sr_pg_2'

            yield response.follow(next_page, callback=self.parse)

            AmazonSpider.page_number += 1
        


