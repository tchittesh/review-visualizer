import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_reviews(page_url):
    headers = {'Host': 'smile.amazon.com',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Language': 'en-US,en;q=0.5',
               'Accept-Encoding': 'gzip, deflate, br',
               'Connection': 'keep-alive',
               'Cookie': 'session-id=145-6881154-7470600; session-id-time=2082787201l; ubid-main=132-5210855-5582818; x-main=Ujc7dKKM3VDD9D7tNm79Q5zoMyNQbcZH; at-main=Atza|IwEBIJFT3l2nu9ehmBuah0qcMSsXwEQnHqgGu0VTI6qS_Fpp-xFs2xRMFHqDphCK9i6JZhn7t7Wr-5pos1VSmiAhZD6Apbj6333e2ZzMLPHRa4Lp4Bw3aV66y9UnG9R1DXGpdZI0i1NPgUwjVD3VWjyWt1pnIFE8N-qrmRc1m2irZo2zfdq41ngjkrqSBp-rY3Oh4voDnP4Ob3-CVN1GLQDXKIN1; sess-at-main="m3C5MMOac1ZJcU6zI6qHY0WHFmWcU/WfZqzp3JIEpfQ="; sst-main=Sst1|PQGNEgvsyG4AMjuymQb1HWW2C_6RqpMGi6qQ2HO8QyL7JAnT1HD0PsIvjphs8W3b3pv515cenaUFEB1Bdo0Urry0rptmgomUgAobH5nZlVYq0zcO-f88XNdKG3DdKRMrP7LT3J0DeS4Ni7xCnUDicIPr-noBoZUJS56GS68D-d-9TC-BUO13mH54D8CkxICnIjfJcW5Z8WUMLKsah4yqWHqP7L8mtHmc1eU3mBOHYN4cjzexB5odnfpboXnV33ei_57dhwAnNkL0lPE7pPttNXUdNoK-68Tp6X_7b1F0BU3DN43Yni7wO7w5mIC2Vo-tF3NuqPkn5Iys8wXLjM1mpki_Ew; lc-main=en_US; s_vnum=1966704000289%26vn%3D8; s_dslv=1600532668706; spblockdate=1537722359338; i18n-prefs=USD; csm-hit=tb:1EXXXPC607KQ3ZBND781+s-1EXXXPC607KQ3ZBND781|1600532803267&adb:adblk_yes&t:1600532803267; p2dPopoverID_all_A102U1QASMIQ61=1558682040.457; p2dPopoverID_default_A102U1QASMIQ61=1558682040.457; unique_id=mUvLV4Py0r68Cqc8iQebNYNVrpUwNtUF; s_fid=1B5C6AA2C4B75211-0071164036D3F11C; regStatus=registered; aws-priv=eyJ2IjoxLCJldSI6MCwic3QiOjF9; s_nr=1600532668708-Repeat; aws-ubid-main=778-6640647-1348586; aws-account-alias=857299346259; aws-userInfo=%7B%22arn%22%3A%22arn%3Aaws%3Aiam%3A%3A857299346259%3Auser%2Falbert%22%2C%22alias%22%3A%22857299346259%22%2C%22username%22%3A%22albert%22%2C%22keybase%22%3A%22LKHMTtgqpnOJppzHXtpN4C01D23ZXUkAUJB00MB615o%5Cu003d%22%2C%22issuer%22%3A%22http%3A%2F%2Fsignin.aws.amazon.com%2Fsignin%22%2C%22signinType%22%3A%22PUBLIC%22%7D; aws-target-static-id=1592944587495-855215; aws-target-visitor-id=1592944587500-470488; aws-target-data=%7B%22support%22%3A%221%22%7D; s_vn=1624480587678%26vn%3D4; session-token="b6sXZZEkVBGl2US/4SdFsX+gEG6CfOEdD22ZxJOEarWemSNvloBqVyYEGkRlj3DE9/DWoXEh7VwWAqDn1qRZmIj/mMQZe/yLQBmDpy5OeMcpYNMEXkXa3bG8sd4p7u2QQROXVyLIJh/b8KH4ZNU25PXBWJMHE8hAppv5wOhaGULMU47Ub8ecYcZNzMjZJSjAtNFWu9eocdiZU0A7rAMeFQ=="; s_dslv_s=Less%20than%201%20day; s_depth=5; s_invisit=true; s_cc=true; c_m=undefinedwww.google.comSearch%20Engine; aws_lang=en; s_sq=%5B%5BB%5D%5D; skin=noskin',
               'Upgrade-Insecure-Requests': '1',
               'TE': 'Trailers'}
    print(page_url)
    page = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(page.content)
    review_page_url = 'https://smile.amazon.com' + [item["href"] for item in soup.find_all() if ("data-hook" in item.attrs and item["data-hook"] == "see-all-reviews-link-foot")][0]

    page_count = 1
    max_pages = 50
    reviews = []
    missed_reviews = 0
    while page_count <= max_pages:
        page_count += 1
        headers = {'Host': 'smile.amazon.com',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Referer': 'https://smile.amazon.com/Lodge-Skillet-Pre-Seasoned-Ready-Stove/dp/B00006JSUA/ref=sr_1_1?brr=1&dchild=1&qid=1600557802&rd=1&s=kitchen&sr=1-1&th=1',
                    'Connection': 'keep-alive',
                    'Cookie': 'session-id=145-6881154-7470600; session-id-time=2082787201l; ubid-main=132-5210855-5582818; x-main=Ujc7dKKM3VDD9D7tNm79Q5zoMyNQbcZH; at-main=Atza|IwEBIJFT3l2nu9ehmBuah0qcMSsXwEQnHqgGu0VTI6qS_Fpp-xFs2xRMFHqDphCK9i6JZhn7t7Wr-5pos1VSmiAhZD6Apbj6333e2ZzMLPHRa4Lp4Bw3aV66y9UnG9R1DXGpdZI0i1NPgUwjVD3VWjyWt1pnIFE8N-qrmRc1m2irZo2zfdq41ngjkrqSBp-rY3Oh4voDnP4Ob3-CVN1GLQDXKIN1; sess-at-main="m3C5MMOac1ZJcU6zI6qHY0WHFmWcU/WfZqzp3JIEpfQ="; sst-main=Sst1|PQGNEgvsyG4AMjuymQb1HWW2C_6RqpMGi6qQ2HO8QyL7JAnT1HD0PsIvjphs8W3b3pv515cenaUFEB1Bdo0Urry0rptmgomUgAobH5nZlVYq0zcO-f88XNdKG3DdKRMrP7LT3J0DeS4Ni7xCnUDicIPr-noBoZUJS56GS68D-d-9TC-BUO13mH54D8CkxICnIjfJcW5Z8WUMLKsah4yqWHqP7L8mtHmc1eU3mBOHYN4cjzexB5odnfpboXnV33ei_57dhwAnNkL0lPE7pPttNXUdNoK-68Tp6X_7b1F0BU3DN43Yni7wO7w5mIC2Vo-tF3NuqPkn5Iys8wXLjM1mpki_Ew; lc-main=en_US; s_vnum=1966704000289%26vn%3D8; s_dslv=1600532668706; spblockdate=1537722359338; i18n-prefs=USD; csm-hit=tb:ACC7SQQGXE06Z0VSTATK+s-51KHA2EBPSCN9YR48THG|1600558395925&adb:adblk_yes&t:1600558395925; p2dPopoverID_all_A102U1QASMIQ61=1558682040.457; p2dPopoverID_default_A102U1QASMIQ61=1558682040.457; unique_id=mUvLV4Py0r68Cqc8iQebNYNVrpUwNtUF; s_fid=1B5C6AA2C4B75211-0071164036D3F11C; regStatus=registered; aws-priv=eyJ2IjoxLCJldSI6MCwic3QiOjF9; s_nr=1600532668708-Repeat; aws-ubid-main=778-6640647-1348586; aws-account-alias=857299346259; aws-userInfo=%7B%22arn%22%3A%22arn%3Aaws%3Aiam%3A%3A857299346259%3Auser%2Falbert%22%2C%22alias%22%3A%22857299346259%22%2C%22username%22%3A%22albert%22%2C%22keybase%22%3A%22LKHMTtgqpnOJppzHXtpN4C01D23ZXUkAUJB00MB615o%5Cu003d%22%2C%22issuer%22%3A%22http%3A%2F%2Fsignin.aws.amazon.com%2Fsignin%22%2C%22signinType%22%3A%22PUBLIC%22%7D; aws-target-static-id=1592944587495-855215; aws-target-visitor-id=1592944587500-470488; aws-target-data=%7B%22support%22%3A%221%22%7D; s_vn=1624480587678%26vn%3D4; session-token="Jos+OdI+hYYJEIiDu1dVwzT+0hAjp/KtOrL4HVkhWhznHnh8YTdBpcy4IS8/NSmYqG3H9rsG/oOw2Iec7ok63MaSmxw6U3NEVVBhdjNYrc7+E8tFdIkrlIxtf43kVNska/q41CvxwrlbLm3knEpgAJn4497zWNbNkbh22e+kOayv0eRVfcrkhFeb35lDtlpYRSOOUYmKqfIzEbngx8kqP2L+IuoEQoSGr4CkQiraWFc0ePBcfOVP622fModOuCzxbyCo/NGeN0Khtoxbid49SA=="; s_cc=true; c_m=undefinedwww.google.comSearch%20Engine; aws_lang=en; s_sq=%5B%5BB%5D%5D; skin=noskin',
                    'Upgrade-Insecure-Requests': '1',
                    'Cache-Control': 'max-age=0'}
        page = requests.get(review_page_url, allow_redirects=3, verify=False, headers=headers)
        soup = BeautifulSoup(page.content)
        review_divs = soup.find_all('div', id=lambda x: x and x.startswith('customer_review-'))
        for review_div in review_divs:
            try:
                review = {}
                review['review_headline'] = review_div.contents[1].contents[2].contents[1].contents[0]
                review['star_rating'] = review_div.contents[1].contents[0].contents[0].contents[0].contents[0][0]
                review['review_body'] = review_div.contents[4].contents[0].contents[1].contents[0]
                date_words = review_div.contents[2].contents[0].split()
                date = datetime.strptime(date_words[-2] + " " + date_words[-3] + " " + date_words[-1], '%d, %B %Y')
                review['review_date'] = date.strftime('%Y-%m-%d')
                reviews.append(review)
            except:
                missed_reviews += 1

        next_page_divs = [item for item in soup.find_all('a') if item.contents and item.contents[0] == 'Next page']
        if len(next_page_divs) != 0:
            review_page_url = 'https://smile.amazon.com' + next_page_divs[0]['href']
        else:
            break
    return reviews


if __name__ == '__main__':
    get_reviews('https://smile.amazon.com/Lodge-Skillet-Pre-Seasoned-Ready-Stove/dp/B00006JSUA/ref=cm_cr_arp_d_product_top?ie=UTF8')