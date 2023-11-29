import pandas as pd
import pathlib
from typing import List, Dict

class BlogsService:
    """Service that interacts with blogs data; allowing basic CRUD operations
    """

    def __init__(self):
        # data path string can live in a settings file or config.yml
        data_path = pathlib.Path("src/data")
        self.blogs = pd.read_csv(data_path / "blogs.csv")

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
            raise ValueError(f"Blog with name: {name} not found.")
        
        return self.__convert_to_dict(blog)[0]

        



