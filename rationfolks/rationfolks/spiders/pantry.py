import scrapy
from ..items import RationfolksItem


class AmazonSpider(scrapy.Spider):
    name = "pantries"

    page_number = 2 

    i = 1
    start_urls = [
        'https://www.amazon.in/s?i=pantry&srs=9574332031&rh=n%3A9574332031%2Cn%3A4859481031&_encoding=UTF8&pf_rd_p=3598e449-49c9-40b4-906a-4a7e48120d01&pf_rd_r=HWSGK1JZ38ADREHYKHX0&pf_rd_s=pantry-subnav-flyout-content-2&pf_rd_t=SubnavFlyout&rw_html_to_wsrp=1&ref=sn_gfs_co_in_pantry-wayfinder-2-1_undefined_7',
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
                    '.a-color-base.a-text-normal::text').extract()
                
                if title and ',' in title[0]:
                    print(title[0])
                    middle = title[0].split(',')
                    title = middle[0]
                    weight = middle[1]
                else:
                    weight = [''] 
                
                price = item.css(
                    '.a-price-whole::text').extract()
                mrp = item.css(
                    '.a-text-price span.a-offscreen::text').extract()

                additional_info = item.css(
                    '.a-text-normal .a-color-secondary::text').extract()
                
                
                # if len(price) > 1:
                #     mrp = [str(price[1])]
                #     price = [str(price[0])]
                # elif len(price):
                #     mrp = ['']
                #     price = [str(price[0])]

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

        # while AmazonSpider.page_number < 2:
        #     next_page = 'https://www.amazon.in/s?i=pantry&srs=9574332031&rh=n%3A14668710031&page=2&qid=1621833387&ref=sr_pg_2'
            
        #     yield response.follow(next_page, callback=self.parse)

            AmazonSpider.page_number += 1
        


