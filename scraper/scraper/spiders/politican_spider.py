import scrapy

from scraper.items import ImageItemOW

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