# Relevant imports
import attrs
import string

@attr.s
class Crawler:
    Session = attr.ib()
    candidate_list = attr.ib(init=False)
    
    def __attrs_post_init__(self):
        self.search_results_urls = (f'http://media.ethics.ga.gov/search/\
                Campaign/Campaign_Namesearchresults.aspx?CommitteeName=&LastName=\
                {character}&FirstName=&Method=0' for character in string.ascii_lowercase)

        # crawl has to come last in the file because it calls other methods
        def crawl(self):
            navigator = SeleniumNavigator()
            for results in self.crawl_candidates_list(navigator):
                for result in results:
                    navigator.follow_link(result)
                    for office in self.crawl_candidate_profile()
                        office.save_to_db()



        def crawl_candidates_list(self, navigator):
            for url in self.search_results_urls:
                navigator.navigate(url)
                parser = SearchResultsParser(navigator.page_source())
                # Yields list of string ids to be visited
                yield parser.parse()

        def crawl_candidate_profile(self, navigator):
            parser = CandidateProfileParser(navigator.page_source())
            # Returns tuple consisting of a Candidate object and list of
            # either contribution table ids or a single None if no finance 
            # reports  are detected.
            return parser.parse() 
