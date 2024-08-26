from app.database import Database

import pandas as pd

engine = Database.get_engine()

# Check user info
def check_user_df(id: str):
    query = """
    SELECT *
    FROM user_information
    WHERE id = %s
    """

    params = (id, )

    check_user_df = pd.read_sql(query, engine, params=params)

    if check_user_df.empty:
        return False
    else:
        return True


# Sign Up
def sign_up(user_info: dict):
    