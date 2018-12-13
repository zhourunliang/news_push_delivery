from news.cn_nytimes import CnNytimes
from news.cn_bbc import CnBBC
from send_mail import send_news_emil

def main():
    cn_nytimes = CnNytimes()
    cn_nytimes.main()

    cn_bbc = CnBBC()
    cn_bbc.main()

    send_news_emil()
    
if __name__ == '__main__':
    main()