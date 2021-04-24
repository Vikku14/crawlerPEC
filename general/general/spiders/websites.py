import scrapy
import pandas as pd
import math
from ..items import GeneralItem
import requests
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, ConnectError
from twisted.internet.error import TimeoutError, TCPTimedOutError


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


    file = '../stanford/stanford.xlsx'
    # file = '../Imperial/imperial.xlsx'
    # file = '../ETH/eth.xlsx'
    # file = '../Chicago/chicago.xlsx'

    data = pd.read_excel(file, usecols=['Name','URL'],
                        index_col = 0)

    # fetch 1st row of every excel file >> start_urls

    data_first = data.iloc[[0]]

    for i, row in data_first.iterrows():
        row0 = row[0].split(',')
        for r in row0:
            if not r.startswith('file://'):
                start_urls.append(r.strip())
        # start_urls = list(map(str.strip, row0))
    row_urls_0 = [row.split("://")[1] for row in start_urls]
    row_urls = dict.fromkeys(row_urls_0, False)

    no_of_rows = int(data.shape[0])

    handle_httpstatus_list = [301, 302, 307, 401, 403, 404, 410, 500, 502, 999]

    def parse(self, response):
        print("\n-----------------------------------\nStart --> row_urls", self.row_urls,end="\n\n")
        print("current URL: ",response.request.url)
        print("Status: ",response.status,end="\n\n")
        try:                                                                                  # Handling redirection
            redirect_url = response.request.meta['redirect_urls'][0].split("://")[1]
            print("url history: ",redirect_url)
            self.row_urls[response.request.url.split("://")[1]] = self.row_urls.pop(redirect_url)
            print(self.row_urls)
        except Exception as e:
            pass


        if self.row_urls[response.request.url.split("://")[1]] == False:
            r = response.request.url
            item = GeneralItem()

            if 'linkedin' in r:
                print("linkedin URL")
                yield scrapy.Request(r, callback=self.Linkedin_crawler)
                # for ar in self.Linkedin_crawler(response):
                #     yield ar
            elif response.request.url.endswith(".pdf"):  # TODO: Handle PDFs
                print("pdf found")
                self.row_urls[response.request.url.split("://")[1]] = True
                print(self.row_urls)
            elif response.status == 404:
                item['url'] = r
                item['Name'] = ["404: Page not found"]
                item['h2'] = ['No data']
                item['h3'] = ['No data']
                item['h4'] = ['No data']
                item['h5'] = ['No data']
                item['h6'] = ['No data']
                # yield item
            elif response.status != 500 and response.status != 502 and response.status != 403 and response.status != 401: ## TODO: Handle 403 seperatly
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

            self.row_urls[response.request.url.split("://")[1]] = True
            print("\nbefore enterting: ", self.row_urls)
            if all(value == True for value in self.row_urls.values()):
                print("entered into all True block")
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

                print("\n\t-------------------")
                print("\t-------------------")
                print("\t|| row number",self.row_number," ||")

                print("\t-------------------")
                print("\t-------------------\n")
                # print("Total Rows",self.no_of_rows)
                if self.row_number < self.no_of_rows:

                    data_row = self.data.iloc[[self.row_number]]
                    print(pd.isna(data_row['URL']) == True)
                    for i, row in data_row.iterrows():
                        row0 = row[0].split(',')
                        self.row_urls_0 = list()
                        for rk in row0:
                            if not rk.startswith('file://'):
                                self.row_urls_0.append(rk.strip())

                        # self.row_urls_0 = list(map(str.strip, row0))
                        print("row_urls_0", self.row_urls_0)
                        row1 = [row.split("://")[1] for row in self.row_urls_0 if row]
                        # row_urls = list(map(str.strip, row1))
                        self.row_urls = dict.fromkeys(row1, False)

                    print("row_urls", self.row_urls,end="\n\n")
                    for link in self.row_urls_0:
                        if link:
                            print("link "+str(link))
                            yield response.follow(link, callback=self.parse,errback=self.errorback)
                    print("done with links")

                    self.row_number += 1



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

    def Linkedin_crawler(self, response):
        print("inside fucntion",response)
        return None

    def errorback(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.row_urls[request.url.split("://")[1]] = True
            print(self.row_urls, end="\n\n")
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.row_urls[request.url.split("://")[1]] = True
            print(self.row_urls, end="\n\n")
            self.logger.error('TimeoutError on %s', request.url)
            self.row_number += 1


        elif failure.check(ConnectError):
            request = failure.request
            self.row_urls[request.url.split("://")[1]] = True
            print(self.row_urls, end="\n\n")
            self.logger.error('ConnectError on %s', request.url)
