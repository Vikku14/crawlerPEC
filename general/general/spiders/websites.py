import scrapy
import pandas as pd
from ..items import GeneralItem
# from collections import defaultdict

class WebsitesSpider(scrapy.Spider):
    name = 'websites'
    start_urls = list()
    row_number = 1
    academician = list()
    academician_data = {
    'Name':['No data'],
    'h2':['No data'],
    'h3':['No data'],
    'h4':['No data'],
    'h5':['No data'],
    'h6':['No data'],
    'url':''
    }
    # academician_data = defaultdict(list)
    print(academician_data)
    file = '../Chicago/chicago.xlsx'
    data = pd.read_excel(file, usecols=['Name','URL'],
                        index_col = 0)

    # fetch 1st row of every excel file >> start_urls

    data_first = data.iloc[[0]]

    for i, row in data_first.iterrows():
        row0 = row[0].split(',')
        start_urls = list(map(str.strip, row0))
    row_urls_0 = [row.split("://")[1] for row in start_urls]
    row_urls = dict.fromkeys(row_urls_0, False)

    no_of_rows = int(data.shape[0])

    handle_httpstatus_list = [404, 500, 999]

    def parse(self, response):
        print("row_urls", self.row_urls)
        print(response.request.url)
        if self.row_urls[response.request.url.split("://")[1]] == False:
            r = response.request.url
            item = GeneralItem()

            if response.status == 999:
                print("linkedin URL")
                for ar in self.Linkedin_crawler(response):
                    yield ar

            elif response.status == 404:
                item['url'] = r
                item['Name'] = ["404: Page not found"]
                item['h2'] = ['No data']
                item['h3'] = ['No data']
                item['h4'] = ['No data']
                item['h5'] = ['No data']
                item['h6'] = ['No data']
                # yield item
            else:
                name = list(map(str.strip, response.xpath("//h1/text() | (//*)[not(ancestor::ul)][contains(@class, 'name') or contains(@id, 'name')]/text()").extract()))
                if not name:
                    name = ['No data']
                h2 = list(map(str.strip, response.css('h2 *::text').extract()))
                if not h2:
                    h2 = ['No data']
                h3 = list(map(str.strip, response.css('h3 *::text').extract()))
                if not h3:
                    h3 = ['No data']
                h4 = list(map(str.strip, response.css('h4 *::text').extract()))
                if not h4:
                    h4 = ['No data']
                h5 = list(map(str.strip, response.css('h5 *::text').extract()))
                if not h5:
                    h5 = ['No data']
                h6 = list(map(str.strip, response.css('h6 *::text').extract()))
                if not h6:
                    h6 = ['No data']
                # print(self.data[self.data['URL'].str.contains(str(r))])

                # extracting the Name


                item['url'] = r
                item['Name'] = name
                item['h2'] = h2
                item['h3'] = h3
                item['h4'] = h4
                item['h5'] = h5
                item['h6'] = h6
                # yield item
            self.academician.append(item)                                             # Storing the data fetched by all URLs for each academician.
            # print(self.academician)
            self.row_urls[response.request.url.split("://")[1]] = True
            if all(value == True for value in self.row_urls.values()):
                # print("enterkjdjfkldsajf ")
                for element in self.academician:                                        # Comparing the data fetched in previous step.
                    if element:
                        if element['Name'] not in [['404: Page not found'], ['No data']]:
                            if self.academician_data['Name'] == ['No data']:
                                self.academician_data['Name'] = element['Name']
                            else:
                                self.academician_data['Name'].extend(element['Name'])
                        if element['h2'] != ['No data']:
                            if self.academician_data['h2'] == ['No data']:
                                self.academician_data['h2'] = element['h2']
                            else:
                                self.academician_data['h2'].extend(element['h2'])
                        if element['h3'] != ['No data']:
                            if self.academician_data['h3'] == ['No data']:
                                self.academician_data['h3'] = element['h3']
                            else:
                                self.academician_data['h3'].extend(element['h3'])
                        if element['h4'] != ['No data']:
                            if self.academician_data['h4'] == ['No data']:
                                self.academician_data['h4'] = element['h4']
                            else:
                                self.academician_data['h4'].extend(element['h4'])
                        if element['h5'] != ['No data']:
                            if self.academician_data['h5'] == ['No data']:
                                self.academician_data['h5'] = element['h5']
                            else:
                                self.academician_data['h5'].extend(element['h5'])
                        if element['h6'] != ['No data']:
                            if self.academician_data['h6'] == ['No data']:
                                self.academician_data['h6'] = element['h6']
                            else:
                                self.academician_data['h6'].extend(element['h6'])

                        self.academician_data['url'] = self.academician_data['url']+", "+element['url']
                    # print(self.academician_data)

                yield self.academician_data
                self.academician = list() # empty list for each academician.
                self.initialize_academician_data()

                # fetch next row of excel file
                print("row_number",self.row_number)
                print("Total Rows",self.no_of_rows)
                if self.row_number <= self.no_of_rows:

                    data_row = self.data.iloc[[self.row_number]]

                    for i, row in data_row.iterrows():
                        row0 = row[0].split(',')
                        self.row_urls_0 = list(map(str.strip, row0))
                        print("row_urls_0", self.row_urls_0)
                        row1 = [row.split("://")[1] for row in self.row_urls_0 if row]
                        # row_urls = list(map(str.strip, row1))
                        self.row_urls = dict.fromkeys(row1, False)

                    print("row_urls", self.row_urls)
                    for link in self.row_urls_0:
                        yield response.follow(link, callback=self.parse)
                    self.row_number += 1


    def Linkedin_crawler(self, response):
        print("inside fucntion",response)
        yield None

    def initialize_academician_data(self):
        self.academician_data = {
        'Name':['No data'],
        'h2':['No data'],
        'h3':['No data'],
        'h4':['No data'],
        'h5':['No data'],
        'h6':['No data'],
        'url':''
        }
