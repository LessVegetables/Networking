from playwright.sync_api import sync_playwright, ElementHandle
import regex

BASE_URL = 'https://t.me/s/'
CHANNEL = 'd_code'


class Post():
    def __init__(self, post_data:ElementHandle):
        pass
    # <thing> <div class>
    # post-time tgme_widget_message_info —> tgme_widget_message_meta —> tgme_widget_message_date —> time (utc0 datetime)
    # post-date tgme_widget_message_service_date
    # view-coutn tgme_widget_message_views
    # reactions tgme_widget_message_reactions


    # reactions
    # post datetime
    # view count
    # Content-text
    # Content-assets (photo and video thumbnails)
    # Message Author name
    # Message Author link
    # Post link
    # Scrape timestamp (utc0)
    # 



def main():

    posts = []

    with sync_playwright() as p:
        browser =  p.webkit.launch()
        page =  browser.new_page()
        page.goto(BASE_URL + CHANNEL)

        all_posts = page.query_selector_all('.tgme_widget_message_wrap')

        with open("output.csv", "w") as f:
            f.write("Text,Time\n")
            for post in all_posts:
                # posts.append(Post(post))
                text = post.query_selector('.tgme_widget_message_text').inner_text()
                time = post.query_selector('.tgme_widget_message_date').inner_text()

                regex.sub(r'\n\s*\n', '\n\n', text)
                collapsedText = ' '.join((text.split('\n')))

                f.write(f'{collapsedText},{time}\n')

        page.wait_for_timeout(10000)
        browser.close()


if __name__ == '__main__':
    main()