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
    fields = list()

    def __init__(self):
        self.initialize_academician_data()
        self.fields = ['designation', 'designation_detail', 'major_area', 'address', 'contact', 'education', 'image', 'h5', 'h6']


    # file = '../stanford/stanford.xlsx'
    # file = '../Imperial/imperial.xlsx'
    # file = '../ETH/eth.xlsx'
    file = '../Chicago/chicago.xlsx'

    data = pd.read_excel(file, usecols=['Name','URL'],
                         index_col = 0, skiprows =[2])

    # fetch 1st row of every excel file >> start_urls
    print(data)
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

    handle_httpstatus_list = [302, 307, 401, 403, 404, 410, 500, 502, 999]

    def initialize_academician_data(self):
        self.academician_data = {
        'Name':['No data'],
        'designation':['No data'],
        'designation_detail':['No data'],
        'major_area':['No data'],
        'University':['No data'],
        'address':['No data'],
        'contact':['No data'],
        'education':['No data'],
        'image':['No data'],
        'h5':['No data'],
        'h6':['No data'],
        'url':''
        }

    def parse(self, response):
        print("\n-----------------------------------\nStart --> row_urls", self.row_urls,end="\n\n")
        print("current URL: ",response.request.url)
        print("Status: ",response.status,end="\n\n")
        try:
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
                item['designation'] = ['No data']
                item['designation_detail'] = ['No data']
                item['major_area'] = ['No data']
                item['address'] = ['No data']
                item['contact'] = ['No data']
                item['education'] = ['No data']
                item['image'] = ['No data']
                item['h5'] = ['No data']
                item['h6'] = ['No data']
                # yield item

                
            elif response.status != 500 and response.status != 502 and response.status != 403 and response.status != 401: ## TODO: Handle 403 seperatly

                # name = list(set(map(str.strip, response.xpath("/html/head/meta[contains(@name,'name') or (contains(@property,'name') and not(contains(@property,'site_name'))) or contains(@name,'title')]/@content").extract())))
                name = list(map(str.strip, response.xpath("//h1/text() | (//*)[not(ancestor::ul)][contains(@class, 'name') or contains(@id, 'name') or contains(@itemprop, 'name')]/text()").extract()))
                if not name:
                    name = ['No data']

                designation = list(set(map(str.strip, response.xpath('(//*)[not(ancestor::ul)][(contains(@class, "title") or contains(@id, "title") or contains(@itemprop, "title")) and (contains(@class, "job") or contains(@itemprop,"job") )]/text()').extract())))
                if not designation:
                    designation = ['No data']

                designation_detail = list(set(map(str.strip, response.xpath('/html/head/meta[@name="description"]/@content').extract())))
                if not designation_detail:
                    designation_detail = ['No data']

                major_area = list(set(map(str.strip, response.xpath('(//*)[not(ancestor::ul)][contains(@class, "special") or contains(@id, "special") or contains(@itemprop, "special")]/text()').extract())))
                if not major_area:
                    major_area = ['No data']

                address = list(set(map(str.strip, response.xpath('(//*)[not(ancestor::ul)][contains(@class, "address") or contains(@id, "address") or contains(@itemprop, "address")]//*/text()').extract())))
                if not address:
                    address = ['No data']

                contact = list(set(map(str.strip, response.xpath('(//*)[contains(@class, "contact") or contains(@id, "contact") or contains(@itemprop, "contact")]//*/text()').extract())))
                if not contact:
                    contact = ['No data']

                education = list(set(map(str.strip, response.xpath('(//*)[contains(@class, "education") or contains(@id, "education") or contains(@itemprop, "education")]//*/text()').extract())))
                if not education:
                    education = ['No data']

                image = list(set(map(str.strip, response.xpath('/html/head/meta[contains(@name,"image") or contains(@property,"image")]/@content').extract())))
                if not image:
                    image = ['No data']

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
                item['designation'] = designation
                item['designation_detail'] = designation_detail
                item['major_area'] = major_area
                item['address'] = address
                item['contact'] = contact
                item['education'] = education
                item['image'] = image
                item['h5'] = h5
                item['h6'] = h6
                # yield item
            self.academician.append(item)                                             # Storing the data fetched by all URLs for each academician.

            self.row_urls[response.request.url.split("://")[1]] = True
            print("\nbefore enterting: ", self.row_urls)
            if all(value == True for value in self.row_urls.values()):

                self.all_true_block()

                yield self.academician_data

                print("\n...................................................")
                for key, value in self.academician_data.items():
                    print("{0:>20} ......... {1}".format(key,value))
                self.academician = list() # empty list for each academician.
                self.initialize_academician_data()


                self.print_row_number()

                # print("Total Rows",self.no_of_rows)
                # fetch next row of excel file
                if self.row_number < 4: # self.no_of_rows

                    data_row = self.data.iloc[[self.row_number]]
                    # print(data_row)
                    for i, row in data_row.iterrows():
                        # print(data_row)
                        # if isinstance(row[0], float):
                        #     print("skipping row")
                        #     self.row_number += 1
                        #     data_row = self.data.iloc[[self.row_number]]
                        #     print(data_row)
                        #     continue

                        print(row[0], type(row[0]))
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




    def print_row_number(self):

        print("\n\t\t-------------------")
        print("\t\t-------------------")
        print("\t\t|| row number",self.row_number," ||")

        print("\t\t-------------------")
        print("\t\t-------------------\n")

    def all_true_block(self):

        '''
        Comparing the data of fetched URLS from one row.
        '''

        print("entered into all True block")
        for element in self.academician:
            if element:
                # print("before conversion")
                # print(element['Name'])
                if element['Name'] != ['No data']:
                    # print("inside IF")
                    # print(element['Name'])
                    if self.academician_data['Name'] == ['No data']:
                        self.academician_data['Name'] = element['Name']
                    elif element['Name'] != ['404: Page not found']:
                        self.academician_data['Name'].extend(element['Name'])
                        try:
                            self.academician_data['Name'].remove('404: Page not found')
                        except Exception:
                            pass

                for field in self.fields:   # Comparing all other fields

                    if element[field] != ['No data']:
                        if self.academician_data[field] == ['No data']:
                            self.academician_data[field] = element[field]
                        else:
                            self.academician_data[field].extend(element[field])


                self.academician_data['url'] = self.academician_data['url']+", "+element['url']
            # print(self.academician_data)
        self.academician_data['University'] = self.file.split('/')[1]


    def Linkedin_crawler(self, response):

        '''
        LinkdedIn crawler
        '''

        print("LinkdedIn Crawler COMMING SOON",response)
        return None


    def errorback(self, failure):

        '''
        Error handling function
        '''

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
