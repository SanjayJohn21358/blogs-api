import unittest
from dataclasses import dataclass
from dataclasses import field
from blogs.blogs_service import BlogsService
from typing import Dict
import pathlib

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
    new_blog_name = "new-blog"
    new_blog = {
        "name": f"{new_blog_name}",
        "display_name": "My New Blog",
        "author_name": "Ron Swanson",
        "body": "This blog is meant to distract the government from doing any actual work.",
        "created_on": "2023-12-12",
        "rating": 5
    }

class BlogsServiceTests(unittest.TestCase):
    """Tests for BlogsService
    """
    @classmethod
    def setUpClass(cls):
        data_path = pathlib.Path("src/data")
        test_blogs_data_path = data_path / "blogs.csv"
        cls.service = BlogsService(test_blogs_data_path, is_test=True)

    def test_get_blogs(self):
        blogs = self.service.get_blogs()
        self.assertTrue(len(blogs) > 1)
        self.assertDictEqual(BlogsServiceTestData.eggs_blog, blogs[0])
        
    def test_get_blog(self):
        blog = self.service.get_blog(BlogsServiceTestData.eggs_blog_name)
        self.assertDictEqual(BlogsServiceTestData.eggs_blog, blog)

    def test_create_blog(self):
        self.service.create_blog(**BlogsServiceTestData.new_blog)

        new_blog_df = self.service.blogs[self.service.blogs["name"] == BlogsServiceTestData.new_blog_name]
        self.assertFalse(new_blog_df.empty)

if __name__ == "__main__":
    unittest.main()
