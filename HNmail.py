import emailsender
import webscraping


def main():
    url = 'https://news.ycombinator.com/news'
    soup = webscraping.get_soup_from_url(url)
    links = webscraping.extract_links(soup)
    email_content = emailsender.create_email_content(
        'email_template.html', links)
    emailsender.send_email(emailsender.read_personaldata_file(
        'personaldata.txt'), "News de Hacker News", email_content)


if __name__ == '__main__':
    main()
