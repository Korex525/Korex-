from django.core.management.base import BaseCommand
from articles.models import Article
from scraper.news_scraper import TechNewsScraper

class Command(BaseCommand):
    help = 'Scrapes tech news headlines and saves them to the Django database'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Starting automated tech news scraper..."))
        
        scraper = TechNewsScraper("https://news.ycombinator.com/")
        articles_data = scraper.fetch_articles()

        if not articles_data:
            self.stdout.write(self.style.ERROR("No articles fetched."))
            return

        added_count = 0
        for item in articles_data:
            title = item.get('title')
            source_url = item.get('source_url')
            content = item.get('content')

            article, created = Article.objects.get_or_create(
                title=title,
                defaults={
                    'content': content,
                    'source_url': source_url
                }
            )
            if created:
                added_count += 1
                self.stdout.write(f"Saved: {title}")

        self.stdout.write(
            self.style.SUCCESS(f"Successfully scraped and saved {added_count} new articles to the database!")
        )