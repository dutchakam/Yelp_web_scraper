import requests
from bs4 import BeautifulSoup
import time

filename = 'yelp_scrape_reviews.csv'
f = open(filename, 'w')
heads = 'Restaurant_Name,Food_Type,Price_Range,Average_Rating,Review_Count,Phone_Number,Address\n'
f.write(heads)

for start in range(0, 51, 10):

    # Top restaurants in Capitol Hill, Denver, CO
    url = f'https://www.yelp.com/search?cflt=restaurants&find_loc=Capitol%20Hill%2C%20Denver%2C%20CO&start={start}'

    headers = {'user-agent': 'Chrome/91.0.4469.4'}
    html_req = requests.get(url, headers=headers)

    time.sleep(10)

    soup = BeautifulSoup(html_req.content, 'lxml')

    names_lst = []
    content = soup.select('[class*=businessName]')
    for item in content:
        name = item.text[3:].replace(', ', '-').strip()
        names_lst.append(name)

    price_lst = []
    cuisine_lst = []
    cuisine_price = soup.select('[class*=priceCategory]')
    for item in cuisine_price:
        cp_lst = item.text.split('$')
        price_lst.append(''.join(['$' for x in cp_lst if x == '']))
        cuisine_lst.append(cp_lst[-1].replace(', ', '-'))

    rating_lst = []
    ratings = soup.select('[aria-label*=rating]')
    for item in ratings:
        stars = item['aria-label'].split(' ')[0]
        rating_lst.append(f'{stars} stars')

    rev_count_lst = []
    rev_counts = soup.select('[class*=reviewCount]')
    for item in rev_counts:
        rev_count_lst.append(item.text)

    phone_lst = []
    address_lst = []
    phone_add = soup.select('[class*=secondaryAttributes]')
    for item in phone_add:
        phone_lst.append(item.text[:14].strip())
        address_lst.append(item.text[14:].strip())

    zipped_lst = [(a, b, c, d, e, f, g) for a, b, c, d, e, f, g in zip(names_lst,
                                                                       cuisine_lst,
                                                                       price_lst,
                                                                       rating_lst,
                                                                       rev_count_lst,
                                                                       phone_lst,
                                                                       address_lst)]

    for i in zipped_lst:
        try:
            f.write(i[0] + ',' + i[1] + ',' + i[2] + ',' + i[3] + ',' + i[4] + ',' + i[5] + ',' + i[6] + '\n')
        except UnicodeEncodeError:
            pass

f.close()



