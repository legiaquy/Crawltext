import scrapy
import pudb
from ..items import MtItem

class moitruong(scrapy.Spider):
    name = "mt"
    start_urls = [
#         "https://moitruong.net.vn/moi-truong-tai-nguyen/bao-ve-moi-truong/"
#         "https://moitruong.net.vn/moi-truong-tai-nguyen/tai-nguyen-va-phat-trien/"
#         "https://moitruong.net.vn/moi-truong-tai-nguyen/o-nhiem-moi-truong/"
#         "https://moitruong.net.vn/bien-doi-khi-hau/"
#         "http://doanthanhnien.vn/tin-tuc/chien-dich-tinh-nguyen-he"
#         "http://doanthanhnien.vn/tin-tuc/tiep-suc-mua-thi"
#         "http://doanthanhnien.vn/tin-tuc/mua-he-xanh"
#         "http://doanthanhnien.vn/tin-tuc/hoa-phuong-do"
#         "http://doanthanhnien.vn/tin-tuc/ky-nghi-hong"
#         "http://doanthanhnien.vn/tin-tuc/hanh-quan-xanh"
#         "https://lhu.edu.vn/516/717/Su-ra-doi-cua-Doan-TNCS-Ho-Chi-Minh.html?fbclid=IwAR1o-PW4H-NsVH11uACLqHnKqDzXsAw9TiFFE5Ari0qyb6ZGt9q0Bqc2UD0"
#         "http://doanthanhnien.vn/tin-tuc/hoc-tap"
#         "http://doanthanhnien.vn/tin-tuc/khoi-nghiep-lap-nghiep"
#         "http://doanthanhnien.vn/tin-tuc/ky-nang-the-chat-van-hoa"
#         "http://doanthanhnien.vn/tin-tuc/3-phong-trao"
        "http://thanhdoanhaiphong.gov.vn/chuyenmuc/xung-kich-tinh-nguyen-8"
        
    ]
    page=7
    
    def parse(self, response):
#         articles = response.css("div.col-sm-8.col-xs-12.no-padding-right a::attr('href')")
        articles = response.css("div.news-hb.clearfix figcaption a::attr('href')")
#         print(articles.extract())
        for a in articles.extract():
            url = response.urljoin(a)
#             print("OKAY: ", str(self.page))
            yield scrapy.Request(url, callback=self.parse_content)
        next_page = "http://thanhdoanhaiphong.gov.vn/chuyenmuc/xung-kich-tinh-nguyen-8/page/"+str(self.page)
#         print("HIHIHIHI: ",next_page)
        self.page += 1
        if self.page<=200:
            next_url = response.urljoin(next_page)
            yield response.follow(next_url, callback=self.parse)
        
    
    def parse_content(self, response):
        items = MtItem()
        
        # USED TO SCRAPE CONTENT
        
#         summary = response.css("p[style='text-align:justify'] span::text").extract()
#         summary = [" ".join(summary)]
# #         print("LENGTHHH: " + str(len(summary[0])))
#         if len(summary[0]) < 10:
#             summary = response.css("p[style='text-align:justify']::text").extract()
#             summary = [" ".join(summary)]
#             if len(summary[0]) < 10:
#                 summary = response.css("span[style='font-family: Arial;']::text").extract() 
#                 summary = [" ".join(summary)]
#                 if len(summary[0]) < 10:
#                     summary = response.css("div[style='text-align: justify;'] *::text").extract()
                    
        summary = response.css("div.text.clearfix *::text").extract()
        summary = [" ".join(summary)]
        
        # THESE SCRIPT USED TO SCRAPE SUMMARY
#         summary = response.css("div.des_single h2[style='text-align: justify;'] span::text").extract()
#         if not summary:
#             summary = response.css("div.des_single h2[style='text-align: justify;'] strong::text").extract()
#             if not summary:
#                 summary = response.css("div.des_single p[style='text-align: justify;'] strong::text").extract()
        if summary:
            items['summary'] = summary
            items['tag'] = "CTTN"
            yield items
        else:
            return True

