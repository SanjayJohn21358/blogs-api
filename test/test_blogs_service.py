import unittest
from blogs.blogs_service import BlogsService
from blogs.db import NotFoundError
from typing import Dict
import pathlib

class BlogsServiceTestData:
    eggs_blog_name = "how-to-cook-eggs-in-10-seconds"
    eggs_blog = {
        "id": f"{eggs_blog_name}",
        "display_name": "How To Cook Eggs in 10 Seconds",
        "author_name": "Jiminy Cricket",
        "body": "Cooking eggs is easy. All you have to do is throw them in the pan!",
        "created_on": "2021-01-01",
        "rating": 5
    }
    new_blog_name = "my-new-blog"
    new_blog = {
        "id": f"{new_blog_name}",
        "display_name": "My New Blog",
        "author_name": "Ron Swanson",
        "body": "This blog is meant to distract the government from doing any actual work."
    }
    deleted_blog_name = "my-deleted-blog"
    deleted_blog = {
        "id": f"{deleted_blog_name}",
        "display_name": "My Deleted Blog",
        "author_name": "Ron Sconson",
        "body": "This blog is meant to be deleted."
    }
    updated_blog_name = "my-updated-blog"
    updated_blog = {
        "id": f"{updated_blog_name}",
        "display_name": "My Updated Blog",
        "author_name": "Ron Sponson",
        "body": "This blog is meant to be updated.",
        "rating": 0
    }

class BlogsServiceTests(unittest.TestCase):
    """Tests for BlogsService
    """
    @classmethod
    def setUpClass(cls):
        cls.service = BlogsService(is_test=True)

    def test_get_blogs(self):
        # arrange + act
        blogs = self.service.get_blogs()

        # assert
        self.assertTrue(len(blogs) > 1)
        self.assertDictEqual(BlogsServiceTestData.eggs_blog, blogs[0])
        
    def test_get_blog(self):
        # arrange + act
        blog = self.service.get_blog(BlogsServiceTestData.eggs_blog_name)

        # assert
        self.assertDictEqual(BlogsServiceTestData.eggs_blog, blog)

    def test_get_blog_raises_not_found_error(self):
        with self.assertRaises(NotFoundError):
            self.service.get_blog("foo")

    def test_create_blog(self):
        # arrange + act
        blog = self.service.create_blog(BlogsServiceTestData.new_blog)

        # assert
        self.assertTrue(blog)

    def test_delete_blog(self):
        # arrange
        self.service.create_blog(BlogsServiceTestData.deleted_blog)

        # act
        self.service.delete_blog(BlogsServiceTestData.deleted_blog_name)

        # assert
        with self.assertRaises(NotFoundError):
            self.service.get_blog(BlogsServiceTestData.deleted_blog_name)

    def test_delete_blog_raises_not_found(self):
        with self.assertRaises(NotFoundError):
            self.service.delete_blog("brerbea")

    def test_update_blog(self):
        # arrange
        self.service.create_blog(BlogsServiceTestData.updated_blog)

        updated_blog = BlogsServiceTestData.updated_blog.copy()
        updated_blog["rating"] = 5
        # act
        self.service.update_blog(BlogsServiceTestData.updated_blog_name, updated_blog)

        # assert
        blog = self.service.get_blog(BlogsServiceTestData.updated_blog_name)
        self.assertNotEqual(BlogsServiceTestData.updated_blog["rating"], blog["rating"])
        self.assertEqual(updated_blog["rating"], blog["rating"])
