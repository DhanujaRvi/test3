import os, socket, logging
from sqlalchemy import Column, Integer, String, DateTime, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging.config
DBBASE = declarative_base()
host_name = socket.gethostname()
ipaddress = socket.gethostbyname(host_name)
link = os.getenv('LOCAL_DATABASE_URL')
#link = "oracle+cx_oracle://scott:tiger@hostname:port/?service_name=myservice&encoding=UTF-8&nencoding=UTF-8"
engine = create_engine(link, echo = False)

class Mislogs(DBBASE):
    __tablename__ = 'mislog'
    logid = Column(Integer, primary_key=True, autoincrement=True)
    Ip = Column(String)
    Uid = Column(String)
    ProductName = Column(String)
    UserEmail = Column(String, nullable = False)
    CompanyName = Column(String)
    ApiName = Column(String)
    Asctime = Column(DateTime)
    TimeTaken = Column(Float)
    DocumentCount = Column(Integer)
    PagesCount = Column(Integer)
    StraightProcess = Column(Integer)
    FileName = Column(String, nullable = False)
    FunctionName = Column(String, nullable = False)
    LevelName = Column(String)
    LineNumber = Column(Integer)
    Message = Column(String)
    #TraceBack = Column(String)
    StatusCode = Column(String)
    StatusDescripiton = Column(String)
    Processed = Column(String)
    
    def __init__(self,ip=None, uid=None, ProductName=None, UserEmail=None,CompanyName=None,ApiName=None, Asctime=None,TimeTaken=None, 
                DocumentCount=None, PagesCount=None, StraightProcess=None, FileName=None, FunctionName=None,LevelName=None, LineNumber=None,
                Message =None,  StatusCode=None, StatusDescripiton=None, Processed=None):
        self.Ip = ip
        self.Uid = uid
        self.ProductName = ProductName
        self.FileName = FileName
        self.FunctionName = FunctionName
        self.Asctime = Asctime
        self.UserEmail = UserEmail
        self.CompanyName = CompanyName
        self.Message = Message
        self.LineNumber = LineNumber
        #self.TraceBack = TraceBack
        self.LevelName = LevelName 
        self.ApiName = ApiName
        self.TimeTaken = TimeTaken
        self.DocumentCount = DocumentCount
        self.StraightProcess = StraightProcess
        self.PagesCount = PagesCount
        self.StatusCode = StatusCode
        self.StatusDescripiton = StatusDescripiton
        self.Processed = Processed

class SQLAlchemyHandler(logging.Handler):
    def emit(self, record):
        uid = record.__dict__['args']['uid']
        
        try:
            logger = record.__dict__['args']['logger']
        except:
            print("db error")
        try:
            UserEmail = record.__dict__['args']['user_email']
        except:
            UserEmail = ""
        try:
            CompanyName = record.__dict__['args']['company_name']
        except:
            CompanyName = ""
        try:
            StatusCode = record.__dict__['args']['statuscode']
        except:
            StatusCode = ""
        try:
            StatusDescripiton = record.__dict__['args']['statusdescription']
        except:
            StatusDescripiton = ""
        try:
            Processed = record.__dict__['args']['processed']
        except:
            Processed = ""
        try:
            DocumentCount = record.__dict__['args']['DocumentCount']
        except:
            DocumentCount = 0
        try:
            PagesCount = record.__dict__['args']['PagesCount']
        except:
            PagesCount = 0
        try:
            StraightProcess = record.__dict__['args']['StraightProcess']
        except:
            StraightProcess = 0
        ApiName = record.__dict__['args']['api']
        Asctime = record.__dict__['args']['StartTime']
        TimeTaken = record.__dict__['args']['time_taken']
        FileName = record.__dict__['filename']
        FunctionName = record.__dict__['funcName']
        LevelName = record.__dict__['levelname']
        LineNumber = record.__dict__['lineno']
        Message = record.__dict__['msg']
        ProductName= "PAYABLES"
        try:
            Session = sessionmaker(bind = engine)
            session = Session()
            '''
            logger.info("{0}, {1}, {2}, {3} , {4},{5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18}".format(ipaddress, 
                        uid, ProductName, UserEmail, CompanyName, ApiName, Asctime, TimeTaken, DocumentCount, PagesCount,
                        StraightProcess, FileName, FunctionName, LevelName, LineNumber, Message , StatusCode, StatusDescripiton,
                        Processed))
            '''
            row = Mislogs(ipaddress, uid, ProductName, UserEmail, CompanyName, ApiName, Asctime, TimeTaken, DocumentCount, PagesCount,
                        StraightProcess, FileName, FunctionName, LevelName, LineNumber, Message , StatusCode, StatusDescripiton,
                        Processed)
            session.add(row)
            session.commit()
            session.close()
        except:
            logger.error("'{0}', '{1}', '{2}', '{3}'".format(UserEmail,CompanyName,uid,"insertion into db"), exc_info=True) 
        return True
        
DBBASE.metadata.create_all(engine) 