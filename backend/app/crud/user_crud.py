from app.database import Database
from app.crud.score_crud import register_user

import pandas as pd
from sqlalchemy import text

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
        register_user(user_id=user_info["user_id"])

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
            SET username = :username, student_id = :student_id,
            department = :department, major = :major, profile_pic = :profile_pic
            WHERE user_id = :user_id
            """
            update_params = {
                'username': user_info['username'], 
                'student_id': user_info['student_id'], 
                'department': user_info['department'],
                'major': user_info['major'],
                'profile_pic': user_info['profile_pic'],
                'user_id': user_id
            }
            
            with engine.connect() as connection:
                with connection.begin():  # 트랜잭션 시작
                    connection.execute(text(update_query), update_params)

        else:
            # user_id가 없는 경우 False 반환 및 오류 메시지 출력
            print(f"Error: user_id {user_id} not found.")
            return False
    except Exception as e:
        # 예외 발생 시 False 반환
        print(f"Error occurred: {e}")
        return False