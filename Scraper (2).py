import requests
import time
import smtplib
from email.mime.text import MIMEText

def search_google_serpapi(query, num_articles=30):
    api_key = "api-key-serpapi"
    url = "https://serpapi.com/search"
    articles = []
    page = 0

    while len(articles) < num_articles:
        params = {
            "engine": "google",
            "q": query,
            "api_key": api_key,
            "tbs": "qdr:w",  # חיפוש מוגבל לשבוע האחרון
            "start": page * 10  # דפדוף בין עמודים
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            results = response.json().get("organic_results", [])
            for item in results:
                if len(articles) >= num_articles:
                    break
                title = item.get("title")
                link = item.get("link")
                snippet = item.get("snippet")
                articles.append({"title": title, "summary": snippet, "link": link})
            page += 1
            time.sleep(1)
        else:
            print(f"Error: {response.status_code}")
            break

    return articles

def format_articles_for_email(articles):
    content = "Latest AI News Articles from the Past Week:\n\n"
    for idx, article in enumerate(articles, start=1):
        content += f"{idx}. Title: {article['title']}\n"
        content += f"Summary: {article['summary']}\n"
        content += f"Link: {article['link']}\n\n"
    return content

def send_email(content, recipient_email):
    msg = MIMEText(content)
    msg['Subject'] = "AI News Summary - Weekly Update"
    msg['From'] = "mail@gmail.com"
    msg['To'] = recipient_email

    smtp_server = 'smtp.gmail.com'
    port = 587
    your_email = "mail@gmail.com"
    your_password = "password"  # הכנס כאן את סיסמת האפליקציה שלך

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(your_email, your_password)
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# פונקציה ראשית
def main():
    articles = search_google_serpapi("AI news", num_articles=30)
    email_content = format_articles_for_email(articles)
    recipient_email = "mail@gmail.com"  # הכנס את כתובת המייל שלך
    send_email(email_content, recipient_email)

if __name__ == "__main__":
    main()
