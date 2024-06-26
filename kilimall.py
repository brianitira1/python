import asyncio
from playwright.async_api import async_playwright
import nltk  # type: ignore
from nltk.sentiment.vader import SentimentIntensityAnalyzer  # type: ignore

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_sentiment(self, comment):
        sentiment_score = self.analyzer.polarity_scores(comment)
        for key in sentiment_score:
            sentiment_score[key] = sentiment_score[key] * 100
        return sentiment_score        

class Review:
    def __init__(self, user_name, user_comment):
        self.user_name = user_name
        self.user_comment = user_comment

class Scraper:
    def __init__(self, url):
        self.url = url
        self.reviews = []
        self.sentiment_analyzer = SentimentAnalyzer()
        
        

    async def get_product_title(self, page):
        """Retrieve the product title from the page."""
        try:
            return await page.locator('div.product-title').inner_text()
        except Exception as e:
            print(f"Error retrieving product title: {e}")
            return None

    async def get_reviews(self, page):
        """Retrieve reviews from the page."""
        reviews = []
        try:
            await page.wait_for_selector('div.reviews-item')  # Wait for reviews items to load
            review_elements = await page.locator('div.reviews-item').all()
            for review_element in review_elements:
                user_name = await review_element.locator('div.user-name').inner_text()
                user_comment = await review_element.locator('p.content-text').inner_text()
                reviews.append(Review(user_name, user_comment))
        except Exception as e:
            print(f"Error retrieving reviews: {e}")
        return reviews

    async def click_next_button(self, page):
        """Click on the Next button."""
        next_button = await page.query_selector('//button[contains(text(),"Next")]')
        if next_button:
            try:
                await next_button.click()
                await page.wait_for_load_state("domcontentloaded")
                return True
            except Exception as e:
                print(f"Error clicking Next button: {e}")
                return False
        else:
            print("Next button not found or no more pages.")
            return False

    async def run(self, pw):
        """Connect to a scraping browser, navigate, and retrieve the product title and reviews."""
        browser = await pw.chromium.launch()
        try:
            page = await browser.new_page()
            print(f'Connected! Navigating to {self.url}...')
            await page.goto(self.url, wait_until='domcontentloaded')

            product_title = await self.get_product_title(page)
            if not product_title:
                return
            print(f"Product Title: {product_title}")

            while True:
                reviews = await self.get_reviews(page)
                self.reviews.extend(reviews)

                for review in reviews:
                    print(f"Username: {review.user_name}")
                    print(f"UserComment: {review.user_comment}")

                    sentiment_score = self.sentiment_analyzer.analyze_sentiment(review.user_comment)

                    print(f"Sentiment Score:  {sentiment_score}")
                    print("---------")
                if not await self.click_next_button(page):
                    break

        finally:
            await browser.close()

    async def start(self):
        async with async_playwright() as pw:
            await self.run(pw)

if __name__ == "__main__":
    url = "https://www.kilimall.co.ke/listing/2430024?sku_id=17870301&title=Ladies+Shoes+Fish+Mouth+Sandals+Women%27s+Style+Roman+Women+Thick+Heels+Versatile+Mid-heel+Thick+Comfortable+Non-slip+Deodorant+Beach+Fashion+Beautiful+Girls+Shoe+Heel+Open+Shoes+Black+Lady+Official&image=https://image.kilimall.com/kenya/shop/store/goods/6151/2023/12/1701684951557b60a6ae36d5e490591e0123899d914fc_360.jpg.webp%23&source=search|hotSearch|Heels&skuId=17870301#pc__product-detail__reviews"
    scraper = Scraper(url)
    asyncio.run(scraper.start())
