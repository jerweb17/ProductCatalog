import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
  
Base = declarative_base()
  
class Catalog(Base):
	__tablename__ = 'catalog'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	description = Column(String(250))
	 #we blah 
	@property
	def serializeCat(self):

	   return {
			'name'         : self.name,
			'id'    : self.id,
			'description'   : self.description,
	   }
 
class Category(Base):
	__tablename__ = 'category'

	name =Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	description = Column(String(250))
	catalog_id = Column(Integer,ForeignKey('catalog.id'))
	catalog = relationship(Catalog) 

	 #we blah 
	@property
	def serialize(self):

	   return {
			'name'         : self.name,
			'description'   : self.description,
			'id'    : self.id,
	   }
 
class Item(Base):
	__tablename__ = 'item'

	name =Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	description = Column(String(250))
	price = Column(String(8))
	category_id = Column(Integer,ForeignKey('category.id'))
	category = relationship(Category) 

 #we blah 
	@property
	def serialize(self):

	   return {
			'name'         : self.name,
			'description'   : self.description,
			'id'    : self.id,
			'price' :self.price,
	   }

 
 
engine = create_engine('sqlite:///productcatalog.db')
Base.metadata.create_all(engine)