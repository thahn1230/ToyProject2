from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sshtunnel import SSHTunnelForwarder

from app.secure.db_config import db_config

Base = declarative_base()

# DB 연결
def create_db_connection():
    # SSH 터널 설정
    tunnel = SSHTunnelForwarder(
        (db_config["ssh_host"], db_config["ssh_port"]),
        ssh_username=db_config["ssh_user"],
        ssh_pkey=db_config["ssh_pkey"],  # PEM 파일을 사용한 SSH 키 인증
        remote_bind_address=(db_config["remote_host"], db_config["remote_port"]),
        local_bind_address=('localhost', 10022)  # 로컬에서 사용할 포트 (임의로 설정 가능)
    )

    tunnel.start()

    # 로컬에서 생성된 터널을 통해 DB에 연결
    db_url = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@127.0.0.1:{tunnel.local_bind_port}/{db_config['database']}"
    engine = create_engine(db_url)

    try:
        connection = engine.connect()
        if connection:
            print(f"Successfully connected to database {db_config['database']}")
            return engine, tunnel
        else:
            print("Failed to create connection")
            tunnel.stop()
            exit()
    except Exception as e:
        print(f"An error occurred when trying to connect to database {db_config['database']}: {str(e)}")
        tunnel.stop()
        exit()

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.engine, cls._instance.tunnel = create_db_connection()
            Base.metadata.create_all(bind=cls._instance.engine)
        return cls._instance

    def get_db(self):
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def get_engine(self):
        return self.engine

    def close_tunnel(self):
        if self.tunnel:
            self.tunnel.stop()