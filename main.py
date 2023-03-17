from dotenv import load_dotenv
load_dotenv()

from slack import get_posts

def main():
    posts = get_posts()
    print(posts)

if __name__ == "__main__":
    main()
