from scrape_list import scrape_main


def main():
    print("Enter the spotify playlist link: ")
    spotify_link = str(input())
    scrape_main(spotify_link)


if __name__ == "__main__":
    main()