from datetime import datetime, timezone

from playwright.sync_api import sync_playwright, Locator
import regex


BASE_URL = 'https://t.me/s/'
CHANNEL = 'd_code'


class Post():
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

    def __str__(self):
        out = f"{self.post_id},{self.post_link},{self.author_name},{self.author_link},{self.datetime},{self.last_scrape_datetime},\({' '.join((self.content_text).split())}\),{self.content_img},{self.views}"
        return out


def main():

    while True:
        print("Enter the channel username to parse <@username>: ", end="")
        channel_username = input()
        if channel_username[0] != '@':
            print("Invalid format!")
        elif channel_username == '':
            print("That's not a username at all!")
        else:
            break

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
            return

        print("Parsing the posts...")
        all_posts = page.locator('.tgme_widget_message_wrap').all()

        for post in all_posts:
            posts.append(Post(post))

            print(posts[-1])

        # page.wait_for_timeout(10000)
        browser.close()
    

if __name__ == '__main__':
    main()