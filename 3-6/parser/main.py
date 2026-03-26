import argparse
from datetime import datetime, timezone

from playwright.sync_api import sync_playwright, Locator
import regex


BASE_URL = 'https://t.me/s/'
CHANNEL = 'd_code'


class Post():
    FIELDS = {
        "post_id":              lambda self: self.post_id,
        "post_link":            lambda self: self.post_link,
        "author_name":          lambda self: self.author_name,
        "author_link":          lambda self: self.author_link,
        "datetime":             lambda self: self.datetime,
        "last_scrape_datetime": lambda self: self.last_scrape_datetime,
        "content_text":         lambda self: ' '.join(self.content_text.split()),
        "content_img":          lambda self: self.content_img,
        "views":                lambda self: self.views,
    }

    def __init__(self, post_data:Locator):
        self.post_id = post_data.locator('.tgme_widget_message.text_not_supported_wrap').get_attribute('data-post')
        self.post_link = post_data.locator('.tgme_widget_message_date').get_attribute('href')
        
        self.author_name = post_data.locator('.tgme_widget_message_owner_name').inner_text()
        self.author_link = post_data.locator('.tgme_widget_message_owner_name').get_attribute('href')

        self.datetime = post_data.locator("time").get_attribute("datetime")
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

    def __str__(self):
        # out = f"{self.post_id},{self.post_link},{self.author_name},{self.author_link},{self.datetime},{self.last_scrape_datetime},\({' '.join((self.content_text).split())}\),{self.content_img},{self.views}"
        return self.serialize()


def main():

    parser = argparse.ArgumentParser(
                    prog='TChannel Parser',
                    description='Parses telegram channels. Outputs the contents into csv file.'
                    )

    parser.add_argument('channel_username', help='The channel username to parse <@username>')
    parser.add_argument('-o', default='output.csv', help='set the output file')
    parser.add_argument(
        "--last",
        nargs="+",
        metavar=("N", "p|d"),
        help="--last <N> <p|h|d>  e.g. \"--last 5 d\" to parse the last 5 days of posts (h - hours); \"--last 10 p\" for the last 10 posts."
    )

    args = parser.parse_args()

    if args.last:
        try:
            amount = int(args.last[0])
            unit = args.last[1]
            if unit not in ("p", "h", "d"):
                raise ValueError
        except (IndexError, ValueError):
            parser.error("Usage: --last <N> <p|h|d>  e.g. --last 2 d")


    
    channel_username = args.channel_username
    if channel_username[0] != '@':
        print("Invalid format!")
        parser.print_help()
        return 2

    print(f"Parsing channel: {args.channel_username}")

    posts = []

    with sync_playwright() as p:
        print("Starting playwright...")
        browser =  p.webkit.launch()
        page =  browser.new_page()
        print("Loading page...")
        page.goto(BASE_URL + channel_username[1:])

        # check to see what ended up loading (the channel page or telegram.org fallback)
        if page.url != (BASE_URL + channel_username[1:]):
            print(f'{page.url} loaded instead! This ain\'t a channel!!! Goodbye')
            return 2

        print("Parsing the posts...")
        all_posts = page.locator('.tgme_widget_message_wrap').all()

        with open(args.o, "w") as f:
            f.write("post_id,post_link,author_name,author_link,datetime,last_scrape_datetime,(content_text),content_img,views\n")
            for post in all_posts:
                posts.append(Post(post))

                f.write(str(posts[-1])+"\n")

        browser.close()

        print(f"Done! Output saved here: {args.o}\nGoodbye")
    

if __name__ == '__main__':
    main()