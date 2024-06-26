import asyncio
from playwright.async_api import async_playwright

class JumiaProduct:
    def __init__(self):
        self.title = None
        self.product_details = None
        self.key_features = None
        self.reviews = []
        self.in_the_box = None
        self.promotions = None
        self.product_specifications = None

    def __repr__(self):
        return f"JumiaProduct(title='{self.title}', product_details='{self.product_details}', ...)"

async def scrape_jumia_product(url):
    # Launch the browser using the chromium engine
    async with async_playwright() as p:
        # Create a new browser instance
        browser = await p.chromium.launch()
        # Create a new page in the browser
        page = await browser.new_page()
        # Navigate to the specified URL
        await page.goto(url, wait_until='domcontentloaded')

        # Create a new instance of the JumiaProduct class
        product = JumiaProduct()

        # Extract the title of the product from the page
        product.title = await page.locator('h1.-fs20.-pts.-pbxs').inner_text()
        print("Title:", product.title)

        # Extract the product details from the page
        product.product_details = await page.locator('div.markup.-mhm.-pvl.-oxa.-sc').inner_text()
        print("Product Details:", product.product_details)

        # Extract the reviews of the product from the page
        review_elements = await page.locator('div.cola.-phm.-df.-d-co article.-pvs.-hr._bet').all()
        for review_element in review_elements:
            # Extract the rating of the review from the page
            rating = await review_element.locator('div.stars').inner_text()
            # Extract the title of the review from the page
            review_title = await review_element.locator('h3.-m.-fs16.-pvs').inner_text()
            # Extract the content of the review from the page
            review_content = await review_element.locator('p.-pvs').inner_text()
            # Extract the date of the review from the page
            review_date = await review_element.locator('div.-df.-j-bet.-i-ctr.-gy5 span.-prs').inner_text()
            # Check if the review is verified on the page
            is_verified = await review_element.locator('div.-df.-i-ctr.-gn5.-fsh0 svg.ic.-f-gn5').is_visible()
            # Store the extracted data in the product instance
            product.reviews.append({
                'rating': rating,
                'title': review_title,
                'content': review_content,
                'date': review_date,
                'verified': is_verified,
            })

        # Extract Key Features of the product from the page
        product.key_features = await page.locator('main.-pvs:nth-child(5) div.row:nth-child(2) div.col12 section.card.aim.-mtm.-fs16:nth-child(2) > div.row.-pas').inner_text()
        print("Key Features:", product.key_features)

        # Extract what is in the box of the product from the page
        product.in_the_box = await page.locator('main.-pvs:nth-child(5) div.row:nth-child(2) div.col12 section.card.aim.-mtm.-fs16:nth-child(2) div.row.-pas > article.col8.-pvs:nth-child(2)').inner_text()
        print("What is in the Box:", product.in_the_box)

        # Extract promotions related to the product from the page
        product.promotions = await page.locator('main.-pvs:nth-child(5) div.row:nth-child(1) section.col12.-df.-d-co div.row.card._no-g.-fg1.-pas div.col10 > section.-phs.-pts.-fs14:nth-child(4)').inner_text()
        print("Promotions:", product.promotions)

        # Extract specifications of the product from the page
        product.product_specifications = await page.locator('main.-pvs:nth-child(5) div.row:nth-child(1) section.col12.-df.-d-co div.row.card._no-g.-fg1.-pas div.col10 > section.-phs.-pts.-fs14:nth-child(4)').inner_text()
        print("Specifications:", product.product_specifications)

        # Close the browser
        await browser.close()

        return product

# Define the URL to scrape
url = "https://www.jumia.co.ke/hisense-hs2100-2.1ch-soundbar-with-wireless-subwoofer-240w-2yrs-wrty-157603683.html"

# Run the scraping function
product = asyncio.run(scrape_jumia_product(url))

# Print the JumiaProduct instance
print(product)