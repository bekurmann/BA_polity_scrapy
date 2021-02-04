import scrapy

from scraper.items import ImageItemOW, AffairItemOW, SessionItemOW

# run:
# scrapy crawl politicanOW -O politicanOW.csv
# -O = overwrite


# **********************************************************************************************
# OW (with tel)
# **********************************************************************************************
class PoliticanOWSpider(scrapy.Spider):
    name = 'politicanOW'

    start_urls = [ 'https://www.ow.ch/de/politik/kantonsratmain/legislative/' ]

    def parse(self, response):
        politican_page_links = response.css('#ol-behoerdenpersonen td:nth-child(1) a')
        yield from response.follow_all(politican_page_links, self.parse_politican)

        pagination_links = response.css('.next')
        yield from response.follow_all(pagination_links, self.parse)


    def parse_politican(self, response):
        
        def extract_with_css_name(query, position):
            # first + last name in one field -> separate!
            return response.css(query).re(r'(\w+) (\w+)')[position]

        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        # variables for callback
        first_name = extract_with_css_name('#nameBehoerdeMitgliedTitle b::text', 0)
        last_name = extract_with_css_name('#nameBehoerdeMitgliedTitle b::text', 1)
        jurisdiction = extract_with_css('#wahlkreisPartContent span::text')

         # make new request to tel.search.ch + passing already scraped fields as cb_kwargs
         # api key: 33455d58f107b0ee44720ebbf044c499
        yield scrapy.Request(url=f'https://tel.search.ch/api/?was={first_name}+{last_name}&wo={jurisdiction}&key=33455d58f107b0ee44720ebbf044c499', 
                            callback=self.parse_politican_address,
                            cb_kwargs={
                                'first_name': extract_with_css_name('#nameBehoerdeMitgliedTitle b::text', 0),
                                'last_name': extract_with_css_name('#nameBehoerdeMitgliedTitle b::text', 1),
                                'date_of_birth': extract_with_css('#birthdayBehoerdeMitgliedContent::text'),
                                'profession': extract_with_css('#gegwBerufPartContent::text'),
                                'email': extract_with_css('#emailPartContent a::text'),
                                'jurisdiction': extract_with_css('#wahlkreisPartContent span::text'),
                                'fraction': extract_with_css('#fraktionenPartContent a::text'),      
                            })

    def parse_politican_address(self, response, first_name, last_name, date_of_birth, profession, email, jurisdiction, fraction):
        selector = scrapy.selector.Selector(response)
        selector.remove_namespaces()       
        
        yield { 
            'first_name': first_name,
            'last_name': last_name,
            'date_of_birth': date_of_birth,
            'profession': profession,
            'email': email,
            'jurisdiction': jurisdiction,
            'fraction': fraction,
            'street1': selector.xpath("//street/text()").get(),
            'street2': selector.xpath("//streetno/text()").get(),
            'phone': selector.xpath("//phone/text()").get()
        }

# **********************************************************************************************
# OW Politican Images
# **********************************************************************************************
class PoliticanOWimageSpider(scrapy.Spider):
    name = 'politicanOWimage'

    start_urls = [ 'https://www.ow.ch/de/politik/kantonsratmain/legislative/' ]

    def parse(self, response):
        politican_page_links = response.css('#ol-behoerdenpersonen td:nth-child(1) a')
        yield from response.follow_all(politican_page_links, self.parse_politican)

        pagination_links = response.css('.next')
        yield from response.follow_all(pagination_links, self.parse)


    def parse_politican(self, response):

        def extract_with_css_name(query, position):
            # first + last name in one field -> separate!
            return response.css(query).re(r'(\w+) (\w+)')[position]

        def extract_with_css(query):
            return response.css(query).get(default='').strip()
            

        # variables for callback
        first_name = extract_with_css_name('#nameBehoerdeMitgliedTitle b::text', 0)
        last_name = extract_with_css_name('#nameBehoerdeMitgliedTitle b::text', 1)
        jurisdiction = extract_with_css('#wahlkreisPartContent span::text')
        relative_image_urls = extract_with_css('#contentboxsub img::attr(src)')
        absolute_image_urls = response.urljoin(relative_image_urls)

        yield ImageItemOW(
            first_name=first_name,
            last_name=last_name,
            jurisdiction=jurisdiction,
            image_urls=[absolute_image_urls]
        )
        
# **********************************************************************************************
# OW affairs
# **********************************************************************************************

class AffairOWSpider(scrapy.Spider):
    name = 'affairOW'

    start_urls = [ 'https://www.ow.ch/de/politik/kantonsratmain/politbusiness/welcome.php?nr=&sq=&dat1=01.01.2010&dat2=04.02.2021&art=&saction=Suchen' ]

    def parse(self, response):
        affair_page_links = response.css('#ol-politbusiness :nth-child(1) a')
        yield from response.follow_all(affair_page_links, self.parse_affair)

        pagination_links = response.css('.next')
        yield from response.follow_all(pagination_links, self.parse)


    def parse_affair(self, response):

        def extract_with_css(query):
            return response.css(query).get(default='').strip()     

        # variables for callback
        title = extract_with_css('#contentboxsub h2::text')
        identifier = extract_with_css(':nth-child(5) :nth-child(1) .pb_value::text')
        date = extract_with_css('#contentboxsub :nth-child(3) .pb_value::text')
        politican = extract_with_css('#contentboxsub :nth-child(7) a::text')
        affair_type = extract_with_css('#contentboxsub :nth-child(2) .pb_value::text')
        session = extract_with_css('#contentboxsub :nth-child(11) a::text')
        absolute_file_urls = extract_with_css('#contentboxsub li a::attr(href)')
        #absolute_file_urls = response.urljoin(relative_file_urls)

        yield AffairItemOW(
            title=title,
            identifier=identifier,
            date=date,
            politican=politican,
            affair_type=affair_type,
            session=session,
            file_urls=[absolute_file_urls]
        )

# **********************************************************************************************
# OW sessions
# **********************************************************************************************

class SessionOWSpider(scrapy.Spider):
    # inclusive file download for protocolsè
    name = 'sessionOW'

    start_urls = [ 'https://www.ow.ch/de/politik/kantonsratmain/sitzung/?show=all' ]

    def parse(self, response):
        session_page_links = response.css(':nth-child(1) a')
        yield from response.follow_all(session_page_links, self.parse_session)

        pagination_links = response.css('.next')
        yield from response.follow_all(pagination_links, self.parse)


    def parse_session(self, response):

        def extract_with_css(query):
            return response.css(query).get(default='').strip()     

        # variables for callback
        title = extract_with_css('#event_titel b::text')
        date = extract_with_css('#event_datum::text')
        file1 = extract_with_css('#event_dokumente_content a:nth-child(1)::attr(href)')
        file2 = extract_with_css('#event_dokumente_content a:nth-child(4)::attr(href)')
        file3 = extract_with_css('#event_dokumente_content a:nth-child(7)::attr(href)')
        file4 = extract_with_css('#event_dokumente_content a:nth-child(10)::attr(href)')

        yield SessionItemOW(
            title=title,
            date=date,
            file_urls=[file1, file2, file3, file4]
        )

# **********************************************************************************************
# NW (TODO)
# **********************************************************************************************
class PoliticanOWSpider(scrapy.Spider):
    name = 'politicanNW'

    start_urls = [ 'https://www.ow.ch/de/politik/kantonsratmain/legislative/' ]

    def parse(self, response):
        politican_page_links = response.css('#ol-behoerdenpersonen td:nth-child(1) a')
        yield from response.follow_all(politican_page_links, self.parse_politican)

        pagination_links = response.css('.next')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_politican(self, response):
        
        def extract_with_css_name(query, position):
            # first + last name in one field -> separate!
            return response.css(query).re(r'(\w+) (\w+)')[position]

        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        # variables for callback
        first_name = extract_with_css_name('#nameBehoerdeMitgliedTitle b::text', 0)
        last_name = extract_with_css_name('#nameBehoerdeMitgliedTitle b::text', 1)
        jurisdiction = extract_with_css('#wahlkreisPartContent span::text')

         # make new request to tel.search.ch + passing already scraped fields as cb_kwargs
         # api key: 33455d58f107b0ee44720ebbf044c499
        yield scrapy.Request(url=f'https://tel.search.ch/api/?was={first_name}+{last_name}&wo={jurisdiction}&key=33455d58f107b0ee44720ebbf044c499', 
                            callback=self.parse_politican_address,
                            cb_kwargs={
                                'first_name': extract_with_css_name('#nameBehoerdeMitgliedTitle b::text', 0),
                                'last_name': extract_with_css_name('#nameBehoerdeMitgliedTitle b::text', 1),
                                'date_of_birth': extract_with_css('#birthdayBehoerdeMitgliedContent::text'),
                                'profession': extract_with_css('#gegwBerufPartContent::text'),
                                'email': extract_with_css('#emailPartContent a::text'),
                                'jurisdiction': extract_with_css('#wahlkreisPartContent span::text'),
                                'fraction': extract_with_css('#fraktionenPartContent a::text'),      
                            })

    def parse_politican_address(self, response, first_name, last_name, date_of_birth, profession, email, jurisdiction, fraction):
        selector = scrapy.selector.Selector(response)
        selector.remove_namespaces()       
        
        yield { 
            'first_name': first_name,
            'last_name': last_name,
            'date_of_birth': date_of_birth,
            'profession': profession,
            'email': email,
            'jurisdiction': jurisdiction,
            'fraction': fraction,
            'street1': selector.xpath("//street/text()").get(),
            'street2': selector.xpath("//streetno/text()").get(),
            'phone': selector.xpath("//phone/text()").get()
        }