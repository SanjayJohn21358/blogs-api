import unittest
from blogs.blogs_service import BlogsService

class BlogsServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.service = BlogsService()

    def test_get_blogs(self):
        blogs = self.service.get_blogs()
        self.assertTrue(len(blogs) > 1)
        self.assertDictEqual(
            {
                "name": "how-to-cook-eggs-in-10-seconds",
                "display_name": "How To Cook Eggs in 10 Seconds",
                "author_name": "Jiminy Cricket",
                "body": "Cooking eggs is easy. All you have to do is throw them in the pan!",
                "created_on": "2021-01-01",
                "rating": 5
            },
            blogs[0])
        
    def test_get_blog(self):
        blog = self.service.get_blog("how-to-cook-eggs-in-10-seconds")
        self.assertDictEqual(
            {
                "name": "how-to-cook-eggs-in-10-seconds",
                "display_name": "How To Cook Eggs in 10 Seconds",
                "author_name": "Jiminy Cricket",
                "body": "Cooking eggs is easy. All you have to do is throw them in the pan!",
                "created_on": "2021-01-01",
                "rating": 5
            },
            blog)


if __name__ == "__main__":
    unittest.main()
