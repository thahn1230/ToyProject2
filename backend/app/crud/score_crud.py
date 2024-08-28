from app.database import Database

import pandas as pd
from sqlalchemy import text

engine = Database().get_engine()

# Register User
def register_user(user_id: str):
    try:
        # User 정보 DataFrame 생성
        score_info_df = pd.DataFrame({'user_id': [user_id], 'score': [0]})

        # User 테이블에 데이터 삽입 (테이블이 이미 존재한다고 가정)
        score_info_df.to_sql('Score', con=engine, if_exists='append', index=False, method='multi')
        return True
    
    except Exception as e:
        # 예외 발생 시 False 반환
        print(f"Error occurred: {e}")
        return False