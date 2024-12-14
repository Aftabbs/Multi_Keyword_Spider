import scrapy
import os
import pandas as pd
from urllib.parse import urlparse, urljoin, parse_qs, urlencode
import signal
import sys
import time

df = pd.read_csv(r"C:\Users\Mohammed Aftab\Downloads\Administrators - URLs - Part 1 (1).csv")

class MultiAdminKeywordSpider(scrapy.Spider):
    name = "multi_scraper"

    admin_urls = [
        {"name": row["Administrator"], "url": row["Website URL"]}
        for _, row in df.iterrows()
    ]
    search_terms = {
        "NIST": ["nist-", " nist ", "nist -"],
        "ISO-27001": ["iso-27001", "iso 27001", " 27001 "],
        "ISO-22301": ["iso 22301", " 22301 "],
        "ISO-9001": ["iso 9001", " 9001 "],
        "SOC": ["soc 1", "soc 2", "soc 3", "system and organization controls",
                "system & organization controls", "soc compliance", "service organization control"],
        "GDPR": [" gdpr ", "general data protection regulation"],
        "ESG": [" esg ", "environmental, social and governance",
                "environmental, social, governance", "environmental, social & governance",
                "environmental social & governance", "environmental social governance"],
    }

    def __init__(self):
        self.results = []
        self.visited_urls = set()
        self.start_time = time.time()
        signal.signal(signal.SIGINT, self.handle_interrupt)

    def start_requests(self):
        for admin in self.admin_urls:
            domain = urlparse(admin["url"]).netloc
            self.allowed_domains = [domain]
            self.log(f"Processing Admin_Name: {admin['name']} - URL: {admin['url']}")
            yield scrapy.Request(
                url=admin["url"],
                callback=self.parse,
                meta={"admin_name": admin["name"], "base_url": admin["url"], "allowed_domain": domain},
            )

    def parse(self, response):
        admin_name = response.meta["admin_name"]
        allowed_domain = response.meta["allowed_domain"]
        base_url = response.meta["base_url"]

        try:
            if not response.headers.get("Content-Type", b"").decode("utf-8").startswith("text"):
                self.log(f"Skipping non-text response from URL: {response.url}")
                self.add_result(admin_name, response.url, base_url, error_comment="Non-text response")
                return

            page_content = response.xpath("//body//text()").getall()
            content = " ".join(page_content).lower()

            raw_terms_found = []
            standardized_terms = []
            category_counts = {category: 0 for category in self.search_terms}

            for category, terms in self.search_terms.items():
                for term in terms:
                    count = content.count(term.lower())
                    if count > 0:
                        raw_terms_found.append(term)
                        if category not in standardized_terms:
                            standardized_terms.append(category)
                        category_counts[category] += count

            self.add_result(
                admin_name, response.url, base_url, raw_terms=",".join(raw_terms_found) if raw_terms_found else None,
                std_terms=",".join(standardized_terms) if standardized_terms else None, **category_counts
            )

            for href in response.xpath("//a/@href").extract():
                next_page = self.clean_url(urljoin(response.url, href))
                if self.is_within_allowed_domain(next_page, allowed_domain) and next_page not in self.visited_urls:
                    self.visited_urls.add(next_page)
                    yield scrapy.Request(
                        url=next_page,
                        callback=self.parse,
                        meta={"admin_name": admin_name, "base_url": base_url, "allowed_domain": allowed_domain},
                    )
                else:
                    self.log(f"Skipped duplicate or out-of-domain URL: {next_page}")

        except Exception as e:
            self.add_result(admin_name, response.url, base_url, error_comment=str(e))

    def closed(self, reason):
        self.save_results()
        elapsed_time = time.time() - self.start_time
        self.log(f"Results saved to 'multi_admin_results.xlsx' in {elapsed_time:.2f} seconds. Reason: {reason}")

    def handle_interrupt(self, signum, frame):
        self.log("Interrupt received. Saving results...")
        self.save_results()
        sys.exit(0)

    def add_result(self, admin_name, crawled_url, base_url, raw_terms=None, std_terms=None, error_comment=None, **categories):
        result = {
            "Admin Name": admin_name,
            "Base URL": base_url,
            "Crawled URL": crawled_url,
            "RAW Keyword": raw_terms,
            "Standard Keyword": std_terms,
            "Error Comment": error_comment,
        }
        result.update(categories)
        self.results.append(result)

    def save_results(self):
        df = pd.DataFrame(self.results)
        output_file = "multi_admin_results_enhanced_approach_part2urls.xlsx"
        df.to_excel(output_file, index=False)
        self.log(f"Results saved to {output_file}")

    @staticmethod
    def is_within_allowed_domain(url, allowed_domain):
        domain = urlparse(url).netloc
        return domain.endswith(allowed_domain)

    @staticmethod
    def clean_url(url):
        """Remove query parameters for consistent URL comparison."""
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        cleaned_query = urlencode({k: v[0] for k, v in query_params.items()})
        return parsed_url._replace(query=cleaned_query).geturl()










# Below is v2 code
# import scrapy
# import os
# import pandas as pd
# from urllib.parse import urlparse, urljoin


# df = pd.read_csv(r"C:\Users\Mohammed Aftab\Downloads\Administrators - URLs - Part 1 (1).csv")


# class MultiAdminKeywordSpider(scrapy.Spider):
#     name = "multi_scraper"

#     admin_urls = [
#         {"name": row["Administrator"], "url": row["Website URL"]}
#         for _, row in df.iterrows()
#     ]
#     search_terms = {
#         "NIST": ["nist-", " nist ", "nist -"],
#         "ISO-27001": ["iso-27001", "iso 27001", " 27001 "],
#         "ISO-22301": ["iso 22301", " 22301 "],
#         "ISO-9001": ["iso 9001", " 9001 "],
#         "SOC": ["soc 1", "soc 2", "soc 3", "system and organization controls",
#                 "system & organization controls", "soc compliance", "service organization control"],
#         "GDPR": [" gdpr ", "general data protection regulation"],
#         "ESG": [" esg ", "environmental, social and governance",
#                 "environmental, social, governance", "environmental, social & governance",
#                 "environmental social & governance", "environmental social governance"],
#     }

#     def start_requests(self):
#         for admin in self.admin_urls:
#             domain = urlparse(admin["url"]).netloc
#             self.allowed_domains = [domain]
#             self.log(f"Processing Admin_Name: {admin['name']} - URL: {admin['url']}")
#             yield scrapy.Request(
#                 url=admin["url"],
#                 callback=self.parse,
#                 meta={"admin_name": admin["name"], "allowed_domain": domain},
#             )

#     def parse(self, response):
#         admin_name = response.meta["admin_name"]
#         allowed_domain = response.meta["allowed_domain"]

#         try:
#             # Check if the response is text
#             if not response.headers.get("Content-Type", b"").decode("utf-8").startswith("text"):
#                 self.log(f"Skipping non-text response from URL: {response.url}")
#                 return

#             page_content = response.xpath("//body//text()").getall()
#             content = " ".join(page_content).lower()

#             raw_terms_found = []
#             standardized_terms = []
#             category_counts = {category: 0 for category in self.search_terms}

#             for category, terms in self.search_terms.items():
#                 for term in terms:
#                     count = content.count(term.lower())
#                     if count > 0:
#                         raw_terms_found.append(term)
#                         if category not in standardized_terms:
#                             standardized_terms.append(category)
#                         category_counts[category] += count

#             self.results.append({
#                 "Admin Name": admin_name,
#                 "Crawled URL": response.url,
#                 "RAW Keyword": ",".join(raw_terms_found) if raw_terms_found else None,
#                 "Standard Keyword": ",".join(standardized_terms) if standardized_terms else None,
#                 "ESG": category_counts.get("ESG", 0),
#                 "SOC": category_counts.get("SOC", 0),
#                 "GDPR": category_counts.get("GDPR", 0),
#                 "ISO-27001": category_counts.get("ISO-27001", 0),
#                 "ISO-22301": category_counts.get("ISO-22301", 0),
#                 "ISO-9001": category_counts.get("ISO-9001", 0),
#                 "NIST": category_counts.get("NIST", 0),
#             })

#             for href in response.xpath("//a/@href").extract():
#                 next_page = urljoin(response.url, href)
#                 if self.is_within_allowed_domain(next_page, allowed_domain) and next_page not in self.visited_urls:
#                     self.visited_urls.add(next_page)
#                     yield scrapy.Request(
#                         url=next_page,
#                         callback=self.parse,
#                         meta={"admin_name": admin_name, "allowed_domain": allowed_domain},
#                     )
#         except Exception as e:
#             self.log(f"Error processing URL: {response.url}. Error: {str(e)}")

#     def closed(self, reason):
#         df = pd.DataFrame(self.results)

#         output_file = "Admin_URL_Part1_New_Urls.xlsx"
#         df.to_excel(output_file, index=False)
#         self.log(f"Results saved to {output_file}")

#     def __init__(self):
#         self.results = []
#         self.visited_urls = set()

#     @staticmethod
#     def is_within_allowed_domain(url, allowed_domain):
#         domain = urlparse(url).netloc
#         return domain.endswith(allowed_domain)



# #----------------------------------------- Below is v1 prod Code------------------------------------------------------

# import scrapy
# import os
# import pandas as pd
# from urllib.parse import urlparse, urljoin


# df=pd.read_csv(r"C:\Users\Mohammed Aftab\Downloads\Admin List - 25.csv")


# class MultiAdminKeywordSpider(scrapy.Spider):
#     name = "multi_scraper"

#     admin_urls =[
#     {"name": row["Administrators"], "url": row["Admin Website"]}
#     for _, row in df.iterrows()
# ]
#     search_terms = {
#         "NIST": ["nist-", " nist ", "nist -"],
#         "ISO-27001": ["iso-27001", "iso 27001", " 27001 "],
#         "ISO-22301": ["iso 22301", " 22301 "],
#         "ISO-9001": ["iso 9001", " 9001 "],
#         "SOC": ["soc 1", "soc 2", "soc 3", "system and organization controls",
#                 "system & organization controls", "soc compliance", "service organization control"],
#         "GDPR": [" gdpr ", "general data protection regulation"],
#         # "AML/KYC": [" aml ", "anti-money laundering", " kyc ", "know your customer"],
#         # "FATCA": [" fatca ", "foreign account tax compliance act"],
#         "ESG": [" esg ", "environmental, social and governance",
#                 "environmental, social, governance", "environmental, social & governance",
#                 "environmental social & governance", "environmental social governance"],
#     }

#     def start_requests(self):
#         for admin in self.admin_urls:
#             domain = urlparse(admin["url"]).netloc
#             self.allowed_domains = [domain] 
#             yield scrapy.Request(
#                 url=admin["url"],
#                 callback=self.parse,
#                 meta={"admin_name": admin["name"], "allowed_domain": domain},
#             )

#     def parse(self, response):
#         admin_name = response.meta["admin_name"]
#         allowed_domain = response.meta["allowed_domain"]

#         page_content = response.xpath("//body//text()").getall()
#         content = " ".join(page_content).lower()

#         raw_terms_found = []
#         standardized_terms = []
#         category_counts = {category: 0 for category in self.search_terms}

#         for category, terms in self.search_terms.items():
#             for term in terms:
#                 count = content.count(term.lower())
#                 if count > 0:
#                     raw_terms_found.append(term)
#                     if category not in standardized_terms:
#                         standardized_terms.append(category)
#                     category_counts[category] += count

#         self.results.append({
#             "Admin Name": admin_name,
#             "Crawled URL": response.url,
#             "RAW Keyword": ",".join(raw_terms_found) if raw_terms_found else None,
#             "Standard Keyword": ",".join(standardized_terms) if standardized_terms else None,
#             # "AML/KYC": category_counts.get("AML/KYC", 0),
#             "ESG": category_counts.get("ESG", 0),
#             # "FATCA": category_counts.get("FATCA", 0),
#             "SOC": category_counts.get("SOC", 0),
#             "GDPR": category_counts.get("GDPR", 0),
#             "ISO-27001": category_counts.get("ISO-27001", 0),
#             "ISO-22301": category_counts.get("ISO-22301", 0),
#             "ISO-9001": category_counts.get("ISO-9001", 0),
#             "NIST": category_counts.get("NIST", 0),
#         })

#         for href in response.xpath("//a/@href").extract():
#             next_page = urljoin(response.url, href)
#             if self.is_within_allowed_domain(next_page, allowed_domain) and next_page not in self.visited_urls:
#                 self.visited_urls.add(next_page)
#                 yield scrapy.Request(
#                     url=next_page,
#                     callback=self.parse,
#                     meta={"admin_name": admin_name, "allowed_domain": allowed_domain},
#                 )

#     def closed(self, reason):
#         df = pd.DataFrame(self.results)

#         output_file = "multi_admin_results.xlsx"
#         df.to_excel(output_file, index=False)
#         self.log(f"Results saved to {output_file}")

#     def __init__(self):
#         self.results = []  
#         self.visited_urls = set()  

#     @staticmethod
#     def is_within_allowed_domain(url, allowed_domain):
#         domain = urlparse(url).netloc
#         return domain.endswith(allowed_domain)
