import scrapy

zip = input("Enter zipcode:\n")

class ScreenSpider(scrapy.Spider):
    name = 'screen'
    allowed_domains = ['bigscreen.com']
    start_urls = [
        'https://www.bigscreen.com/Marquee.php?action=chloc&view=nearby&zip=' + zip,
    ]

    def parse(self, response):
        for link in response.css('tr.item a::attr(href)'):
            yield response.follow(link.get(), callback = self.parse_theaters)

    def parse_theaters(self, response):
        movie_theaters = response.css('div.maincontent')
        for movie_theater in movie_theaters:
            yield {
                'theater': movie_theater.css('span.theatername::text').get(),
            }
        theaters1 = response.css('tr.graybar_0')
        for theater in theaters1:
            yield {
                'title': theater.css('a.movieNameList::text').get(),
                'showtime': theater.css('a::text').getall(),
            }
        theaters2 = response.css('tr.graybar_1')
        for theater in theaters2:
            yield {
                'title': theater.css('a.movieNameList::text').get(),
                'showtime': theater.css('a::text').getall(),
            }
        
        #the above loops are going to produce a single array of movie titles
        #Find a way to be able to retrieve the showtimes (which is seemingly only available through response.css('a::text')) and relate them to the corresponding movie
        #Find a way to be able to relate each movie and their respective showtimes to each theater
        #I'm dumb, just realized that I haven't yet procured the names of the individual movie theaters just yet
        
        ##Once I get the theater names, I can retrieve the array returned by the a::text and parse through it to assign to corresponding variables....easy enough
        ###Will most likely end up deleting the above code once I can see how the array is returned as it contyains all information relevant ot each movie being shown at each theater (i.e., showtimes)
        #### Info wanted (from bigscreen.com): 
        #1. Theater name
        #2. Movies being shown at said theater
        #3. Showtimes for said movies
        #### Info wanted (from imdb.com):
        #1. Movie rating
        #2. Rating (1-10 stars)
        #3. Reviews (actual reviews)
        #### Will need movie posters somehow (doesn't seem high priority here)
