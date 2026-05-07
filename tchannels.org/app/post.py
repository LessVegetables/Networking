from datetime import datetime, timezone
import regex

from playwright.sync_api import Locator

class Post():
    FIELDS = {
        "post_id":              lambda self: self.post_id,
        "post_link":            lambda self: self.post_link,
        "author_name":          lambda self: self.author_name,
        "author_link":          lambda self: self.author_link,
        "datetime":             lambda self: self.post_datetime,
        "last_scrape_datetime": lambda self: self.last_scrape_datetime,
        "views":                lambda self: self.views,
        "content_text":         lambda self: ' '.join(self.content_text.split()),
        "content_img":          lambda self: self.content_img,
    }

    def __init__(self, post_data:Locator):
        self.post_id = post_data.locator('.tgme_widget_message.text_not_supported_wrap').get_attribute('data-post')
        self.post_link = post_data.locator('.tgme_widget_message_date').get_attribute('href')
        
        self.author_name = post_data.locator('.tgme_widget_message_owner_name').inner_text()
        self.author_link = post_data.locator('.tgme_widget_message_owner_name').get_attribute('href')

        self.post_datetime = post_data.locator("time[datetime]").get_attribute("datetime")

        self.last_scrape_datetime = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

        self.content_text = post_data.locator('.tgme_widget_message_text.js-message_text').inner_text()

        content_img = [] # including video thumbnails
        content_img_data = post_data.locator('.tgme_widget_message_photo_wrap').all()
        for img_data in content_img_data:
            style = img_data.get_attribute("style")
            url = regex.findall(r"^.*:url\('(.*)'\).*$", style)
            content_img.append(url[0])
        self.content_img = content_img

        # todo: add reactions
        # reactions = {}
        # reactions_data = post_data.locator('.tgme_widget_message_reactions').locator('.tgme_widget_message_bubble')
        # react_data = reactions_data.locator(".tgme_reaction").all()
        # reaction_loc = post_data.locator(".tgme_reaction")

        # for i in range (reaction_loc.count()):
        #     react = reaction_loc.nth(i)
        #     emoji = react.locator("b").inner_text()
        #     count = react.inner_text()
        #     reactions.update({emoji: count})
        # self.reactions = reactions

        self.views = post_data.locator(".tgme_widget_message_views").inner_text()
        # todo: convert the str to int
        # whole = 
        # decimal = 
        # magnitude = str_views[-1]
        # if str_views[-1] == 'M':
        #     splat = str_views.split('.')
        #     self.views = int(splat[0]) * 1000000 + int(splat[1][:-1]) * pow(10, 6 - len(splat[1][:-1]))
        # elif str_views[-1] == 'K':
        #     splat = str_views.split('.')
        #     self.views = int(splat[0]) * 1000 + int(splat[1][:-1]) * pow(10, 3 - len(splat[1][:-1]))
        # else:
        #     self.views = int(str_views)

    def serialize(self, wanted: set[str] = None):
        fields = self.FIELDS if wanted is None else {
            k: v for k, v in self.FIELDS.items() if k in wanted
        }
        return ",".join(str(fn(self)) for fn in fields.values())
    
    def serialize_json(self, wanted: set[str] = None):
        pass

    def __str__(self):
        # out = f"{self.post_id},{self.post_link},{self.author_name},{self.author_link},{self.post_datetime},{self.last_scrape_datetime},\({' '.join((self.content_text).split())}\),{self.content_img},{self.views}"
        return self.serialize()

    def _parse_views(self, s: str) -> int:
        s = s.strip()
        if s.endswith("K"):
            return round(float(s[:-1]) * 1_000)
        elif s.endswith("M"):
            return round(float(s[:-1]) * 1_000_000)
        return int(s)
    
    def to_db(self) -> dict:
        channel_id, post_id = self.post_id.split("/")

        return {
            "post_id":              self.post_id,
            "channel_id":           channel_id,
            "author_name":          self.author_name,
            "post_datetime":        datetime.fromisoformat(self.post_datetime),
            "last_scrape_datetime": datetime.fromisoformat(self.last_scrape_datetime),
            "views":                self._parse_views(self.views),
            "content_text":        ' '.join(self.content_text.split()),
            "content_img":          self.content_img,
        }

