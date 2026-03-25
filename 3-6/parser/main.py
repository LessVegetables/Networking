from playwright.sync_api import sync_playwright

BASE_URL = 'https://t.me/s/'
CHANNEL = 'd_code'



def main():
    with sync_playwright() as p:
        browser =  p.webkit.launch()
        page =  browser.new_page()
        page.goto(BASE_URL + CHANNEL)

        all_posts = page.query_selector_all('.tgme_widget_message_wrap')

        for post in all_posts:
            text = post.query_selector('.tgme_widget_message_text').inner_text()
            time = post.query_selector('.tgme_widget_message_date').inner_text()
            print({'Text': text, 'Time': time})

        page.wait_for_timeout(10000)
        browser.close()


if __name__ == '__main__':
    main()