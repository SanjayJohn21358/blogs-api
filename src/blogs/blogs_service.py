import pandas as pd
import pathlib
from typing import List, Dict, Any
from datetime import datetime

class NotFoundError(Exception):
    """Raises error if item was not found"""
    pass

class ConflictError(Exception):
    """Raises error if item conflicts with current state"""
    pass

class BlogsService:
    """Service that interacts with blogs data; allowing basic CRUD operations

        Args:
            path (pathlib.Path): Path to a seeded dataframe containing blogs
            is_test (bool): Boolean flag indicating if service is running in test mode

        Test mode: data operations are not saved to pandas dataframe
    """

    def __init__(self, path: pathlib.Path, is_test: bool=False):
        self.path = path
        self.is_test = is_test
        self.blogs = pd.read_csv(path, index_col=None)

    @staticmethod
    def __convert_to_dict(df) -> List[Dict]:
        """Convert pandas dataframe into Dictionary

            Args:
                df (pd.DataFrame): dataframe to convert

            Returns:
                Dictionary representation of df
        """
        return df.to_dict(orient='records')

    def get_blogs(self) -> List[Dict]:
        """Get blogs

            Returns:
                List of Dicts where each dict is a blog
        """
        return self.__convert_to_dict(self.blogs)
    
    def get_blog(self, name: str) -> Dict:
        """Get blog by url name

            Args:
                name (str): url safe name of blog

            Returns:
                Dict corresponding to blog with name

            Raises:
                NotFoundError if blog is not found
        """
        blog = self.blogs[self.blogs['name'] == name]
        if blog.empty:
            raise NotFoundError(f"Blog with name: {name} not found.")
        
        return self.__convert_to_dict(blog)[0]
    
    def create_blog(self, **kwargs: Dict[str, Any]) -> Dict:
        """Create blog

            Args:
                **kwargs:
                    name (str): url-safe name of blog
                    display_name (str): display name of blog
                    body (str): content of blog
                    author_name (str): name of author
            
            Raises:
                ConflictError if blog with name already exists
        """
        try:
            blog = self.get_blog(kwargs["name"])
        except: NotFoundError
        else:
            raise ConflictError(f"Blog with name: {kwargs['name']} already exists.")
        
        current_date = datetime.today().strftime("%Y-%m-%d")
        rating = 0
        self.blogs.loc[self.blogs.last_valid_index() + 1] = [kwargs["name"], kwargs["display_name"], kwargs["author_name"], kwargs["body"], current_date, rating]
        self.save_blogs_data()
        
        return {
            "name": kwargs["name"],
            "display_name": kwargs["display_name"],
            "author_name": kwargs["author_name"],
            "body": kwargs["body"],
            "created_on": current_date,
            "rating": rating
        }

    def save_blogs_data(self):
        if not self.is_test:
            self.blogs.to_csv(self.path, index=None)
