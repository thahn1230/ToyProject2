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
    
# Change User Info
def modify_user_info(user_info: dict):
    try:
        # 해당하는 user_id 데이터 찾기
        user_id = user_info["user_id"]

        query = """
        SELECT *
        FROM reskku.User
        WHERE user_id = %s
        """

        params = (user_id, )

        user_info_df = pd.read_sql(query, engine, params=params)

        # 해당 user_id가 있는지 확인
        if not user_info_df.empty:
            # user_id가 있는 경우 데이터 대체 (UPDATE 쿼리 실행)
            update_query = """
            UPDATE reskku.User
            SET username = %s, student_id = %s,
            department = %s, major = %s, profile_pic = %s
            WHERE user_id = %s
            """
            update_params = (user_info['username'], 
                             user_info['student_id'], 
                             user_info['department'],
                             user_info['major'],
                             user_info['profile_pic'],
                             user_id)
            
            with engine.connect() as connection:
                connection.execute(update_query, update_params)
            
            return True
        else:
            # user_id가 없는 경우 False 반환 및 오류 메시지 출력
            print(f"Error: user_id {user_id} not found.")
            return False
    except Exception as e:
        # 예외 발생 시 False 반환
        print(f"Error occurred: {e}")
        return False