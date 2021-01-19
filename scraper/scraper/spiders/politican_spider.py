import scrapy
# run:
# scrapy crawl politicanOW -O politicanOW.csv
# -O = overwrite

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

        yield {
            'first_name': extract_with_css_name('#nameBehoerdeMitgliedTitle b::text', 0),
            'last_name': extract_with_css_name('#nameBehoerdeMitgliedTitle b::text', 1),
            'date_of_birth': extract_with_css('#birthdayBehoerdeMitgliedContent::text'),
            'profession': extract_with_css('#gegwBerufPartContent::text'),
            'email': extract_with_css('#emailPartContent a::text'),
            'jurisdiction': extract_with_css('#wahlkreisPartContent span::text'),
            'fraction': extract_with_css('#fraktionenPartContent a::text'),
            
        }