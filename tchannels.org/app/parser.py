import argparse
from datetime import datetime, timezone, timedelta

from playwright.sync_api import sync_playwright

from post import Post

# ADD channel_id PARSE
# INT the view count

BASE_URL = 'https://t.me/s/'
CHANNEL = 'd_code'

FLAGS = ["post_id", "post_link", "author_name", "author_link", "datetime", "last_scrape_datetime", "views", "content_text", "content_img"]

def arg_parser_init():
    parser = argparse.ArgumentParser(
                    prog='TChannel Parser',
                    description='Parses telegram channels. Outputs the contents into csv file.'
                    )
    
    for flag in FLAGS:
        parser.add_argument(f"--{flag}", action="store_true")

    parser.add_argument('channel_username', help='The channel username to parse <@username>')
    parser.add_argument('-o', default='output.csv', help='set the output file')
    parser.add_argument(
        "--last",
        nargs="+",
        metavar=("N", "p|d"),
        help="--last <N> <p|h|d>  e.g. \"--last 5 d\" to parse the last 5 days of posts (h - hours); \"--last 10 p\" for the last 10 posts."
    )

    return parser


def parse(channel_username=None, o=None, last=None, **flags):

    parser = arg_parser_init()

    if channel_username is None: #called directly
        args = parser.parse_args()
    else: # function call
        args = parser.parse_args([channel_username])
        args.last = last
        for flag in FLAGS:
            setattr(args, flag, flags.get(flag, False))

    if args.last:
        try:
            amount = int(args.last[0])
            unit = args.last[1]
            if unit not in ("p", "h", "d"):
                raise ValueError
        except (IndexError, ValueError):
            parser.error("Usage: --last <N> <p|h|d>  e.g. --last 2 d")
    
    # Check if any flag was explicitly passed
    active_flags = {flag for flag in FLAGS if getattr(args, flag)}

    # If none passed — all are on by default
    if not active_flags:
        active_flags = FLAGS
    
    channel_username = args.channel_username
    if channel_username[0] != '@':
        print("Invalid format!")
        parser.print_help()
        return 2

    print(f"Parsing channel: {args.channel_username}")
    print(f"And saving: {' '.join(active_flags)}")

    posts = []

    with sync_playwright() as p:
        print("Starting playwright...")
        browser =  p.webkit.launch()
        page =  browser.new_page()
        print("Loading page...")
        page.goto(BASE_URL + channel_username[1:]) # <–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
        # page.goto("localhost:8000")
        # check to see what ended up loading (the channel page or telegram.org fallback)
        if page.url != (BASE_URL + channel_username[1:]):
            print(f'{page.url} loaded instead! This ain\'t a channel!!! Goodbye')
            return 2

        print("Parsing the posts...")

        if args.last:
            amount = int(args.last[0])
            unit = args.last[1]
            print(f"Parsing the last {amount} {unit}...")
        
            if unit == 'p': # if unit is "posts" keep scrolling up until the count of .tgme_.... is >= the sought ammount
                loaded_posts_count = page.locator('.tgme_widget_message_wrap').count()
                while loaded_posts_count < amount:
                    page.locator('.tgme_widget_message_wrap').first.scroll_into_view_if_needed()
                    loaded_posts_count = page.locator('.tgme_widget_message_wrap').count()
                
                all_posts = page.locator('.tgme_widget_message_wrap').all()
                for i in range(1, amount + 1):
                    post = all_posts[-i]
                    posts.append(Post(post))

            else: # if unit is the time
                oldest_loaded_post_datetime = datetime.fromisoformat(page.locator('.tgme_widget_message_wrap').first.locator("time[datetime]").get_attribute("datetime"))
                datetime_now = datetime.now(timezone.utc).replace(microsecond=0)

                if unit == 'h':
                    datetime_then = datetime_now - timedelta(hours=amount)
                elif unit == 'd':
                    datetime_then = datetime_now - timedelta(days=amount)
                else:
                    print("bro 'h', 'd' or 'p' nothing else")
                    browser.close()
                    return 2

                # print(f"now: {datetime_now}\tthen:{datetime_then}\t{oldest_loaded_post_datetime=}")
                # print(datetime_then < oldest_loaded_post_datetime)

                while oldest_loaded_post_datetime > datetime_then:
                    page.locator('.tgme_widget_message_wrap').first.scroll_into_view_if_needed()
                    oldest_loaded_post_datetime = datetime.fromisoformat(page.locator('.tgme_widget_message_wrap').first.locator("time[datetime]").get_attribute("datetime"))
                

                all_posts = page.locator('.tgme_widget_message_wrap').all()
                for post in all_posts:
                    post_datetime = datetime.fromisoformat(post.locator("time[datetime]").get_attribute("datetime"))

                    # print(f"post_datetime > datetime_then {post_datetime > datetime_then}")

                    if post_datetime < datetime_then:
                        continue
                    posts.append(Post(post))
                

        else: # just parse what gets loaded
            all_posts = page.locator('.tgme_widget_message_wrap').all()
            for post in all_posts:
                posts.append(Post(post))

        browser.close()

    print(f"Saving to: {args.o}")
    # writing posts to output file
    with open(args.o, "w") as f:
        f.write(",".join(active_flags) + "\n")
        
        for post in posts:
            f.write(post.serialize(active_flags) + "\n")

    print(f"Done!\nGoodbye")
    

if __name__ == '__main__':
    parse()
    # ADD channel_id PARSE