import unittest
from dataclasses import dataclass
from dataclasses import field
from blogs.blogs_service import BlogsService
from typing import Dict


class BlogsServiceTestData:
    eggs_blog_name = "how-to-cook-eggs-in-10-seconds"
    eggs_blog = {
        "name": f"{eggs_blog_name}",
        "display_name": "How To Cook Eggs in 10 Seconds",
        "author_name": "Jiminy Cricket",
        "body": "Cooking eggs is easy. All you have to do is throw them in the pan!",
        "created_on": "2021-01-01",
        "rating": 5
    }

class BlogsServiceTests(unittest.TestCase):
    """Tests for BlogsService
    """
    @classmethod
    def setUpClass(cls):
        cls.service = BlogsService()

    def test_get_blogs(self):
        blogs = self.service.get_blogs()
        self.assertTrue(len(blogs) > 1)
        self.assertDictEqual(BlogsServiceTestData.eggs_blog, blogs[0])
        
    def test_get_blog(self):
        blog = self.service.get_blog(BlogsServiceTestData.eggs_blog_name)
        self.assertDictEqual(BlogsServiceTestData.eggs_blog, blog)

if __name__ == "__main__":
    unittest.main()
