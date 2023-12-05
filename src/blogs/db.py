from abc import ABC
from abc import abstractmethod
from typing import Any, Dict, List
import pandas as pd
from pandas import DataFrame

class NotFoundError(Exception):
    """Raises error if item was not found"""
    pass

class ConflictError(Exception):
    """Raises error if item conflicts with current state"""
    pass

class IRepository(ABC):
    """Abstraction that allows for regular db operations
        GET, ADD, SAVE, UPDATE, REMOVE

        Test mode: Adds and Removes are not saved
    """

    @abstractmethod
    def __init__(self, path, is_test=False):
        self.path = path
        self.is_test = is_test

    @abstractmethod
    def get_all(self, params):
        """Get items from database"""
        pass

    @abstractmethod
    def get(self, id: Any):
        """Get item from database"""
        pass

    @abstractmethod
    def add(self, params):
        """Add item to database"""
        pass

    @abstractmethod
    def update(self, id: Any, params):
        """Update item in database"""
        pass

    @abstractmethod
    def remove(self, id: Any):
        """Remove items from database"""
        pass

    @abstractmethod
    def save(self):
        """Save added or removed items to database"""
        pass


class DataFrameRepository(IRepository):
    """Implements IRepository to use a pandas dataframe
    """

    def __init__(self, path, is_test=False):
        self.path = path
        self.is_test = is_test
        self.df = pd.read_csv(path)
        self.df.set_index("id", inplace=True)

    def get_all(self, params=None) -> Dict:
        """Get items from database given queries
        
            Args:
                params (Dict[str,str]): keywords corresponding to queries
            
            Returns:
                Dict containing items from database corresponding to query
        """

        return self.convert_df_to_dict(self.df)

    def get(self, id: str) -> Dict:
        """Get item from database

            Args:
                id (str): id of item to be accessed

            Returns:
                Dict containing item from database

            Raises:
                KeyError if item is not found
        """

        item = self.df.loc[[id]]
        if item.empty:
            raise KeyError
        
        return self.convert_df_to_dict(item)[0]
    
    def add(self, params) -> Dict:
        """Add item to database

            Args:
                params (Dict[str,str]): dictionary containing item to be added

            Returns:
                Dict containing item from database
            
            Raises:
                ConflictError if item with id already exists
        """

        try:
            self.get(params["id"])
        except KeyError:
            pass
        else:
            raise ConflictError(f"Item with name: {params['id']} already exists.")
        
        new_item = pd.DataFrame([params])
        new_item.set_index("id", inplace=True)
        self.df = pd.concat([self.df, new_item], ignore_index=False)
        return self.get(params["id"])
    
    def update(self, id: str, params) -> Dict:
        """Update item in database

            Args:
                id (str): id of item
                params (Dict[str,str]): dictionary with fields to update

            Returns:
                Dict containing item from database
            
            Raises:
                KeyError if item with id doesn't exist
        """

        self.get(id)

        params["id"] = id   
        updated_item = pd.DataFrame([params])
        updated_item.set_index("id", inplace=True) 
        self.df.update(updated_item)
        return self.get(id)

    def remove(self, id: str):
        """Remove item from database

            Args:
                id (str): id of item to be deleted

            Returns:
                None

            Raises:
                KeyError if item not found
        """

        self.get(id)
        self.df.drop(index=id, inplace=True)

    def save(self):
        if not self.is_test:
            self.df.to_csv(self.path)

    def convert_df_to_dict(self, df: DataFrame) -> List[Dict]:
        """Convert pandas dataframe into Dictionary

            Args:
                df (pd.DataFrame): dataframe to convert

            Returns:
                Dictionary representation of df
        """
        new_df = df.reset_index(names="id")
        return new_df.to_dict(orient='records')
