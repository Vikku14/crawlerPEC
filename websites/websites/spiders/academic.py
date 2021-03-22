import scrapy
from ..items import WebsitesItem

class AcademicSpider(scrapy.Spider):
    name = 'academic'
    s_no = 1
    next_page_counter = 2
    start_urls = ['https://profiles.stanford.edu/search?p=1&q=india&ps=100']

    def parse(self, response):
        divs = response.css('div.customrow.no-margin:not(.extra-left-padding)')
        for div in divs:
            link = div.css('a::attr(href)').extract()

            academic_page = 'https://profiles.stanford.edu'+str(link[0])
            yield response.follow(academic_page, callback=self.academician)

        next_page = 'https://profiles.stanford.edu/search?p='+str(AcademicSpider.next_page_counter)+'&q=india&ps=100'
        if AcademicSpider.next_page_counter < 5:
            AcademicSpider.next_page_counter += 1
            yield response.follow(next_page, callback=self.parse)

    def academician(self, response):
        item = WebsitesItem()

        title = response.css('h1::text').extract_first()
        bio = response.css('h2::text').extract_first()
        email = response.css('span+ .extra-bottom-padding a::text').extract_first()
        department = response.css('.department::text').extract()
        designation = response.css('.affiliation::text').extract()
        detail_designation = response.css('.position::text').extract()
        phone = response.css('.phone a::text').extract_first()
        web_page = response.css('.nameAndTitle a::text').extract()
        image_url = response.css('img::attr(src)').extract()
        cv = response.css('.cv::attr(href)').extract()

        item['S_No'] = AcademicSpider.s_no
        item['Academician_Name'] = title
        item['Bio'] = bio
        item['Email'] = email
        item['Department'] = [dept[17:] for dept in department]
        item['Designation'] = designation
        item['Detail_Designation'] = [des[11:] for des in detail_designation]
        item['Phone'] = phone
        item['Web_Page'] = web_page
        item['Image_Url'] = image_url
        item['CV'] = cv

        yield item
        AcademicSpider.s_no += 1
