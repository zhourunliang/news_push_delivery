from news.cn_nytimes import CnNytimes
from send_mail import send_news_emil

def main():
    CnNytimes.main()
    send_news_emil()
    
if __name__ == '__main__':
    main()