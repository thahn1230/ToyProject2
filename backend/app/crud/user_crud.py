from app.database import Database

import pandas as pd

engine = Database().get_engine()

# Check user info
def check_user_df(id: str):
    query = """
    SELECT *
    FROM reskku.User
    WHERE user_id = %s
    """

    params = (id, )

    check_user_df = pd.read_sql(query, engine, params=params)

    if check_user_df.empty:
        return False
    else:
        check_user_str = check_user_df.to_json(force_ascii=False, orient="records")
        check_user_str = check_user_str.replace('\\/', '/')
        return check_user_str

# Sign Up
def sign_up(user_info: dict):
    try:
        # User 정보 DataFrame 생성
        user_info_df = pd.DataFrame([user_info])

        # User 테이블에 데이터 삽입 (테이블이 이미 존재한다고 가정)
        user_info_df.to_sql('User', con=engine, if_exists='append', index=False, method='multi')

        return True
    except Exception as e:
        # 예외 발생 시 False 반환
        print(f"Error occurred: {e}")
        return False