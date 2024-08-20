from ..database import Database

import pandas as pd

engine = Database.get_engine()

def get_user_df(id: str):
    query = """
    SELECT *
    FROM user_information
    WHERE id = %s
    """

    params = (id, )
    user_df = pd.read_sql(query, engine, params=params)

    return user_df
