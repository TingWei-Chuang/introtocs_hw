import csv
from crawler import Crawler
from args import get_args


if __name__ == '__main__':
    args = get_args()
    crawler = Crawler()
    content = crawler.crawl(args.start_date, args.end_date)
    content = [["Post Date", "Title", "Content"]] + content
    with open(args.output, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(content)
