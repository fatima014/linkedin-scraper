# LinkedIn Scraper

This is a simple Python script for scraping LinkedIn profiles and extracting posts made by the user.

## Dependencies

- `json`: For handling JSON data.
- `re`: For regular expression operations.
- `os`: For interacting with the operating system.
- `time`: For introducing delays in the script.
- `selenium`: For automating web browser interaction.
- `parsel`: For extracting data from HTML.
- `webdriver_manager`: For managing web drivers automatically.
- `ChromeDriverManager`: For managing Chrome driver.

## Setup

1. Install dependencies: `pip install selenium parsel webdriver_manager`
2. Make sure you have the Chrome browser installed.
3. Set up your LinkedIn credentials as environment variables:
   - `LINKEDIN_USERNAME`: Your LinkedIn email or username.
   - `LINKEDIN_PASSWORD`: Your LinkedIn password.

## Usage

1. Run main.py.
2. The script will log in to LinkedIn using the provided credentials.
3. It will then scrape the specified profile(s) and extract the posts.
4. Extracted posts will be saved in `results.json` file.

## Important Notes

- This script is for educational purposes only. Make sure to respect LinkedIn's terms of service and privacy policies.
- Use responsibly and avoid aggressive scraping that may violate LinkedIn's usage guidelines.
- The script may need adjustments if LinkedIn's HTML structure or classes change.



