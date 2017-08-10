import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


engine = create_engine('mysql+pymysql://lchen:tiger@localhost:3306/test')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
     __tablename__ = 'users'
#     __table_args__ = {'extend_existing': True} 
     id = Column(Integer, primary_key=True)
     name = Column(String(16))
     fullname = Column(String(16))
     password = Column(String(12))
     def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                             self.name, self.fullname, self.password)

ed_user = User(name='ed', fullname='Ed Jones', password='edspass')
session.add(ed_user)
session.add_all([
    User(name='wendy', fullname='Wendy Williams', password='foobar'),
    User(name='mary', fullname='Mary Contrary', password='xxg527'),
    User(name='fred', fullname='Fred Flinstone', password='blah')])
session.commit()


class Address(Base):
    __tablename__ = 'addresses'
#    __table_args__ = {'extend_existing': True} 
    id = Column(Integer, primary_key=True)
    email_address = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="addresses")
    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address

User.addresses = relationship("Address", order_by=Address.id, back_populates="user")

# now you can use 


Base.metadata.create_all(engine)