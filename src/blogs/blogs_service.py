import pandas as pd
import pathlib
from typing import List, Dict, Any
from datetime import datetime
from blogs.db import DataFrameRepository, NotFoundError

class BlogsService:
    """Service that interacts with blogs data; allowing basic CRUD operations

        Args:
            is_test (bool): Boolean flag indicating if service is running in test mode

        Test mode: data operations are not saved to pandas dataframe
    """

    def __init__(self, is_test: bool=False):
        # data path string can live in a settings file or config.yml
        data_path = pathlib.Path("src/data")
        blogs_data_path = data_path / "blogs.csv"
        self.blogs = DataFrameRepository(path=blogs_data_path, is_test=is_test)
        
    def get_blogs(self) -> List[Dict]:
        """Get blogs

            Returns:
                List of Dicts where each dict is a blog
        """
        return self.blogs.get_all()
    
    def get_blog(self, name: str) -> Dict:
        """Get blog by url name

            Args:
                id (str): url safe id of blog

            Returns:
                Dict corresponding to blog with name

            Raises:
                NotFoundError if blog is not found
        """
        try:
            return self.blogs.get(name)
        except KeyError:
            raise NotFoundError
    
    def create_blog(self, params: Dict[str, Any]) -> Dict:
        """Create blog

            Args:
                params:
                    display_name (str): display name of blog
                    body (str): content of blog
                    author_name (str): name of author
            
            Raises:
                ConflictError if blog with name already exists
        """

        params["id"] = self.__generate_id(params["display_name"])
        params["created_on"] = datetime.today().strftime("%Y-%m-%d")
        params["rating"] = 0

        item = self.blogs.add(params)
        self.blogs.save()

        return item

    def update_blog(self, id: str, params: Dict[str, Any]) -> Dict:
        """Update blog

            Args:
                id (str): id of blog
                params:
                    display_name (str): display name of blog
                    body (str): content of blog
                    author_name (str): name of author
            
            Raises:
                NotFoundError if blog is not found with id
        """
        try:
            blog = self.blogs.update(id, params)
            self.blogs.save()
            return blog
        except KeyError:
            raise NotFoundError
    
    def delete_blog(self, id: str) -> None:
        """Delete blog
        
            Args:
                id (str): id of blog to delete

            Raises:
                NotFoundError if blog is not found
        """
        try:
            self.blogs.remove(id)
            self.blogs.save()
        except KeyError:
            raise NotFoundError

    @staticmethod
    def __generate_id(keyword: str) -> str:
        """Generate id given keyword"""
        id = "-".join(keyword.split(' ')).lower()
        return id
