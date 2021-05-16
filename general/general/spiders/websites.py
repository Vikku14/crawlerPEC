from linkedin_api import Linkedin
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


    academician = list()
    fields = list()
    url_status = dict()

    def __init__(self):
        self.initialize_academician_data()
        self.fields = ['designation', 'designation_detail', 'major_area', 'address', 'contact', 'education', 'image', 'email', 'Phone_No']



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


    row_number = 1
    no_of_rows = 2


    # no_of_rows = int(data.shape[0])

    handle_httpstatus_list = [307, 401, 403, 404, 410, 500, 502, 999]

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
        'email':['No data'],
        'Phone_No':['No data'],
        'url':''
        }

    def parse(self, response):
        print("\n-----------------------------------\nStart --> row_urls", self.row_urls,end="\n\n")
        print("current URL: ",response.request.url)
        print("Status: ",response.status,end="\n\n")

        self.url_status[response.request.url] = response.status

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
            elif ".pdf" in response.request.url:  # TODO: Handle PDFs
                print("PDF found: Ignoring")
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
                item['email'] = ['No data']
                item['Phone_No'] = ['No data']
                # yield item


            elif response.status != 500 and response.status != 502 and response.status != 403 and response.status != 401: ## TODO: Handle 403 seperatly

                # name = list(set(map(str.strip, response.xpath("/html/head/meta[contains(@name,'name') or (contains(@property,'name') and not(contains(@property,'site_name'))) or contains(@name,'title')]/@content").extract())))
                name = list(set(map(str.strip, response.xpath("//h1/descendant-or-self::*[not(self::style)] /text() | (//*)[not(ancestor::ul)][contains(@class, 'name') or contains(@id, 'name') or contains(@itemprop, 'name')]/text()").extract())))
                if not name:
                    name = ['No data']
                print(name)
                designation = list(set(map(str.strip, response.xpath('(//*)[not(ancestor::ul)][(contains(@class, "title") or contains(@id, "title") or contains(@itemprop, "title")) and (contains(@class, "job") or contains(@itemprop,"job") )]/text()').extract())))
                if not designation:
                    designation = ['No data']

                designation_detail = list(set(map(str.strip, response.xpath('/html/head/meta[@name="description"]/@content | //h2/descendant-or-self::*/text()').extract())))
                if not designation_detail:
                    designation_detail = ['No data']

                major_area = list(set(map(str.strip, response.xpath('(//*)[not(ancestor::ul)][contains(@class, "special") or contains(@id, "special") or contains(@itemprop, "special")]/text()').extract())))
                print(" >>  major_area", major_area)
                if not major_area:
                    major_area = ['No data']

                print(" >>  major_area", major_area)

                address = list(set(map(str.strip, response.xpath('//address/descendant-or-self::*/text() | ' \
                                                                '(//*)[not(ancestor::ul)][contains(@class, "address") or contains(@id, "address") or contains(@itemprop, "address")]/descendant-or-self::*/text()').extract())))
                if not address:
                    address = ['No data']

                contact = list(set(map(str.strip, response.xpath('(//*)[contains(@class, "contact") or contains(@id, "contact") or contains(@itemprop, "contact")]/descendant-or-self::*/text()').extract())))
                if not contact:
                    contact = ['No data']

                education = list(set(map(str.strip, response.xpath('(//*)[contains(@class, "education") or contains(@id, "education") or contains(@itemprop, "education")]/descendant-or-self::*/text()').extract())))
                if not education:
                    education = ['No data']

                pre_image = list(set(map(str.strip, response.xpath('/html/head/meta[contains(@name,"{0}") or contains(@property,"{0}")]/@content'.format("image")).extract())))
                for each_name in name:
                    print(each_name)
                    if each_name:
                        for partial_name in each_name.split(' '):
                            pre_image.append(response.xpath('//img[contains(translate(@title, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),"{0}") or '\
                            'contains(translate(@src, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),"{0}")]/@src'.format(partial_name.lower())).extract())
                        # print("pre_image",pre_image)
                image = list()
                for img in pre_image:
                    if img:
                        if isinstance(img, list):
                            for y in img:
                                image.append(requests.compat.urljoin(response.request.url, y))
                        else:
                            image.append(requests.compat.urljoin(response.request.url, img))

                if not image:
                    image = ['No data']

                email = list(set(map(str.strip, response.xpath('//a[contains(@href, "mailto")]/@href |' \
                '(//*)[not(ancestor::ul) and not(ancestor::table)][contains(@class, "mail") or contains(@id, "mail") or contains(@itemprop, "mail")]/descendant-or-self::*/text()').extract())))
                print("email ",email)
                if not email:
                    email = ['No data']
                Phone_No = list(set(map(str.strip, response.xpath(
                    '(//*)[contains(@class, "phone") or contains(@id, "phone") or contains(@itemprop, "phone")]/descendant-or-self::*/text()').extract())))
                if not Phone_No:
                    Phone_No = ['No data']
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
                item['email'] = email
                item['Phone_No'] = Phone_No
                # yield item
            self.academician.append(item)                                             # Storing the data fetched by all URLs for each academician.

            self.row_urls[response.request.url.split("://")[1]] = True
            print("\nbefore enterting: ", self.row_urls)
            if all(value == True for value in self.row_urls.values()):

                self.all_true_block()


                print("\n................................................................................................................................")
                for key, value in self.academician_data.items():
                    if key in self.fields:
                        self.academician_data[key] = list(set(value))
                    print("{0:>20} ......... {1}".format(key,self.academician_data[key]))
                print("\n................................................................................................................................\n")

                for key, value in self.url_status.items():
                    print("\t| {0} ......... {1}".format(key,value))
                print()

                yield self.academician_data



                self.academician = list() # empty list for each academician.
                self.url_status = dict()
                self.initialize_academician_data()


                self.print_row_number()

                # print("Total Rows",self.no_of_rows)
                # fetch next row of excel file
                if self.row_number < self.no_of_rows:

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
                        if self.academician_data[field] == ['No data'] and element[field] != ['']:
                            self.academician_data[field] = element[field]
                        else:
                            self.academician_data[field].extend(element[field])


                self.academician_data['url'] = self.academician_data['url']+element['url']+"\n"
            # print(self.academician_data)
        self.academician_data['University'] = self.file.split('/')[1]


    def Linkedin_crawler(self, response):

        '''
        LinkdedIn crawler
        '''
        print("LinkdedIn Crawler\n",response)


        from linkedin_api import Linkedin

        # Authenticate using any Linkedin account credentials
        api = Linkedin('viveksharma.mtcse19@pec.edu.in', 'vivek@pec')
        profile_id = response.request.url.split("/")[-1]
        # GET a profile
        profile = api.get_profile(profile_id)
        for key, value in profile.items():
            print("{0:>20} ......... {1}".format(key,value))

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
