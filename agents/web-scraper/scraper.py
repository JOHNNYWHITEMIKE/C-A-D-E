"""
Web Scraper AI Agent
Autonomous agent for web scraping tasks
"""
import os
import json
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScraperAgent:
    """Autonomous web scraping agent"""
    
    def __init__(self, task_data: dict):
        """
        Initialize the scraper agent
        
        Args:
            task_data: Dictionary containing:
                - target_urls: List of URLs to scrape
                - data_fields: List of fields to extract
                - output_format: 'csv', 'json', or 'excel'
                - use_javascript: Whether to use Selenium (True) or BeautifulSoup (False)
        """
        self.task_data = task_data
        self.target_urls = task_data.get('target_urls', [])
        self.data_fields = task_data.get('data_fields', [])
        self.output_format = task_data.get('output_format', 'csv')
        self.use_javascript = task_data.get('use_javascript', False)
        self.output_dir = os.getenv('OUTPUT_DIR', '/output')
        
        logger.info(f"Initialized Web Scraper Agent for {len(self.target_urls)} URLs")
    
    def setup_driver(self):
        """Setup Selenium WebDriver for JavaScript-heavy sites"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    
    def scrape_with_selenium(self, url: str) -> list:
        """Scrape a URL using Selenium (for JavaScript-heavy sites)"""
        logger.info(f"Scraping {url} with Selenium...")
        driver = self.setup_driver()
        results = []
        
        try:
            driver.get(url)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Get page source
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Extract data based on fields
            results = self._extract_data(soup)
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
        finally:
            driver.quit()
        
        return results
    
    def scrape_with_beautifulsoup(self, url: str) -> list:
        """Scrape a URL using BeautifulSoup (for static sites)"""
        logger.info(f"Scraping {url} with BeautifulSoup...")
        results = []
        
        try:
            import requests
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            results = self._extract_data(soup)
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
        
        return results
    
    def _extract_data(self, soup: BeautifulSoup) -> list:
        """
        Extract data from parsed HTML
        
        This is a generic implementation. In production, you'd customize
        based on specific site structure or use AI to intelligently detect
        and extract data.
        """
        results = []
        
        # Example: Extract product data (customize based on actual site structure)
        # This is a placeholder - real implementation would need site-specific selectors
        
        # Try common e-commerce patterns
        products = soup.find_all(['div', 'article', 'li'], class_=lambda x: x and any(
            keyword in str(x).lower() for keyword in ['product', 'item', 'card']
        ))
        
        for product in products[:50]:  # Limit to first 50 items
            item_data = {}
            
            # Extract fields
            for field in self.data_fields:
                field_lower = field.lower()
                
                if 'name' in field_lower or 'title' in field_lower:
                    # Look for title/name
                    title_elem = product.find(['h1', 'h2', 'h3', 'h4', 'a'])
                    item_data[field] = title_elem.get_text(strip=True) if title_elem else 'N/A'
                
                elif 'price' in field_lower:
                    # Look for price
                    price_elem = product.find(class_=lambda x: x and 'price' in str(x).lower())
                    if not price_elem:
                        price_elem = product.find(['span', 'div'], string=lambda x: x and '$' in str(x))
                    item_data[field] = price_elem.get_text(strip=True) if price_elem else 'N/A'
                
                elif 'rating' in field_lower:
                    # Look for rating
                    rating_elem = product.find(class_=lambda x: x and 'rating' in str(x).lower())
                    item_data[field] = rating_elem.get_text(strip=True) if rating_elem else 'N/A'
                
                elif 'description' in field_lower:
                    # Look for description
                    desc_elem = product.find(['p', 'div'], class_=lambda x: x and 'desc' in str(x).lower())
                    item_data[field] = desc_elem.get_text(strip=True) if desc_elem else 'N/A'
                
                else:
                    # Generic field extraction
                    elem = product.find(string=lambda x: x and field.lower() in str(x).lower())
                    item_data[field] = elem if elem else 'N/A'
            
            if item_data:
                results.append(item_data)
        
        logger.info(f"Extracted {len(results)} items")
        return results
    
    def scrape_all(self) -> list:
        """Scrape all target URLs"""
        all_results = []
        
        for url in self.target_urls:
            if self.use_javascript:
                results = self.scrape_with_selenium(url)
            else:
                results = self.scrape_with_beautifulsoup(url)
            
            all_results.extend(results)
        
        logger.info(f"Total items scraped: {len(all_results)}")
        return all_results
    
    def save_results(self, data: list):
        """Save scraped data in specified format"""
        if not data:
            logger.warning("No data to save")
            return
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Generate output filename
        task_id = self.task_data.get('task_id', 'unknown')
        
        if self.output_format == 'csv':
            output_file = os.path.join(self.output_dir, f'{task_id}_results.csv')
            df.to_csv(output_file, index=False)
            logger.info(f"Saved results to {output_file}")
        
        elif self.output_format == 'json':
            output_file = os.path.join(self.output_dir, f'{task_id}_results.json')
            df.to_json(output_file, orient='records', indent=2)
            logger.info(f"Saved results to {output_file}")
        
        elif self.output_format == 'excel':
            output_file = os.path.join(self.output_dir, f'{task_id}_results.xlsx')
            df.to_excel(output_file, index=False)
            logger.info(f"Saved results to {output_file}")
        
        # Also save metadata
        metadata = {
            'task_id': task_id,
            'urls_scraped': self.target_urls,
            'total_items': len(data),
            'fields': self.data_fields,
            'output_file': output_file
        }
        
        metadata_file = os.path.join(self.output_dir, f'{task_id}_metadata.json')
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Saved metadata to {metadata_file}")
    
    def run(self):
        """Execute the scraping task"""
        logger.info("Starting web scraping task...")
        
        try:
            # Scrape all URLs
            results = self.scrape_all()
            
            # Save results
            self.save_results(results)
            
            logger.info("Scraping task completed successfully!")
            return 0
        
        except Exception as e:
            logger.error(f"Scraping task failed: {e}")
            return 1


def main():
    """Main entry point for the agent"""
    # Get task data from environment variable (set by orchestrator)
    task_data_str = os.getenv('TASK_DATA', '{}')
    
    try:
        task_data = json.loads(task_data_str)
    except json.JSONDecodeError:
        logger.error("Invalid TASK_DATA format")
        sys.exit(1)
    
    # Validate required fields
    if not task_data.get('target_urls'):
        logger.error("No target URLs specified")
        sys.exit(1)
    
    # Create and run agent
    agent = WebScraperAgent(task_data)
    exit_code = agent.run()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
