from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKeyConstraint
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()
class ModelDescriptor(Base):
    __tablename__ = 'modeldescriptors'
    folder_name	 = Column(String, primary_key=True)
    name = Column(String)
    
class Variable(Base):
    __tablename__ = 'variables'
    model_id= Column(String, ForeignKey('modeldescriptors.folder_name'),
    					primary_key=True)
    symbol= Column(String, primary_key=True)
    modeldescriptor=relationship('ModelDescriptor',back_populates='variables')	

ModelDescriptor.variables=relationship("Variable",back_populates='modeldescriptor')


class StateVectorPosition(Base):
    __tablename__ = 'statevectorpositions'
    variables_model_id= Column(String,primary_key=True)
    variables_symbol= Column(String, primary_key=True)
    ForeignKeyConstraint(['variables_symbol', 'variables_model_id'], ['variables.symbol', 'variables.model_id'])
    #variable=relationship('Variable',foreign_keys=[Variable.symbol,Variable.model_id],back_populates='statevectorposition')	


#Variable.statevectorposition=relationship("StateVectorPosition",foreign_keys=[variable.symbol,Variable.model_id],back_populates='variable')

Base.metadata.create_all(engine)

# insert data
Session = sessionmaker(bind=engine)
session=Session()
m=ModelDescriptor(folder_name='default_1',name="Hilbert")
session.add(m)
session.add_all([
    ModelDescriptor(folder_name='default_2',name="Ceballos"),	
    ModelDescriptor(folder_name='default_3',name="Ceballos_new")
    ]
)	
