from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from utils.host import DOTENV_PATH
import os
import json
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker


load_dotenv(DOTENV_PATH)

CIC_DB_CREDENTIALS = json.loads(os.getenv('CIC_DB_CREDENTIALS', '{}'))
cic_connection_string = str(URL.create(**CIC_DB_CREDENTIALS))
cic_engine = create_engine(cic_connection_string)

Session = sessionmaker(bind=cic_engine)