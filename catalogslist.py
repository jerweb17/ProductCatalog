from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Catalog, Base, Category, Item
 
engine = create_engine('sqlite:///productcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()



#Catalog 1
catalog1 = Catalog(name = "Sporting South", description = "Your Source for the best Sporting goods available!")
session.add(catalog1)
session.commit()

catalog2 = Catalog(name = "Fishing Source", description = "If it swims in the water and is a fish, we have stuff to help you get it!")
session.add(catalog2)
session.commit()

catalog3 = Catalog(name = "Greatest Outdoors", description = "If it is a bear, we have stuff to help you get it!")
session.add(catalog3)
session.commit()

catalog4 = Catalog(name = "Leisure Games", description = "If iyou relax by looking at birds, we have stuff to help you get it!")
session.add(catalog4)
session.commit()

#Categories----------------------------------------------------------------------------------------------
category1 = Category(name = "Shoes", description = "Athletic shoes for men, women and children",  catalog = catalog1)
session.add(category1)
session.commit()

category2 = Category(name = "Apparel", description = "Looking your best while working out!",  catalog = catalog1)
session.add(category2)
session.commit()

category3 = Category(name = "Equipment", description = "Treadmills, weight benches, punching bags, and more!",  catalog = catalog1)
session.add(category3)
session.commit()

category4 = Category(name = "Accessories", description = "Sunglasses, headbands, gloves, and more!",  catalog = catalog1)
session.add(category4)
session.commit()

category5= Category(name = "Rods and Reels", description = "Top of the line Fish and Tackle",  catalog = catalog2)
session.add(category5)
session.commit()

category6 = Category(name = "Lures", description = "Here Fishy Fishy!",  catalog = catalog2)
session.add(category6)
session.commit()

category7 = Category(name = "Boat Accessories", description = "Nets, Reel Rods, Fish Finders and more!",  catalog = catalog2)
session.add(category7)
session.commit()

category8 = Category(name = "Hiking", description = "Packs, Boots and Walking Sticks",  catalog = catalog3)
session.add(category8)
session.commit()

category9 = Category(name = "Hunting", description = "Guns and Ammo",  catalog = catalog3)
session.add(category9)
session.commit()

category10 = Category(name = "Boating", description = "Canoes, Kayaks, and more!",  catalog = catalog3)
session.add(category10)
session.commit()

category11 = Category(name = "Optics", description = "See the World!",  catalog = catalog3)
session.add(category11)
session.commit()

category12 = Category(name = "Back Yard Fun", description = "Put me in coach!",  catalog = catalog4)
session.add(category12)
session.commit()

category13 = Category(name = "Bowling", description = "The Latest and Greatest!",  catalog = catalog4)
session.add(category13)
session.commit()

category14 = Category(name = "Arcade", description = "Looking your Best!",  catalog = catalog4)
session.add(category14)
session.commit()

category15 = Category(name = "Carnival", description = "Put me in coach!",  catalog = catalog4)
session.add(category15)
session.commit()

#Items----------------------------------------------------------------------------------------------------------------------------
item1 = Item(name = "Spalding Never Flat", description = "Men\'s Basketball with pump", price = "$35.99", category  = category1)
session.add(item1)
session.commit()

item2 = Item(name = "Wilson Evolution", description = "America\'s Favorite Indoor Ball", price = "$55.99", category  = category1)
session.add(item2)
session.commit()

item3 = Item(name = "Nick Junior Bucket Ball", description = "Not that cool", price = "$5.99", category  = category1)
session.add(item3)
session.commit()

item4 = Item(name = "Epic Series Pro X", description = "Women\'s Basketball with pump", price = "$35.99", category  = category2)
session.add(item4)
session.commit()

item5 = Item(name = "T54B Straight Shooter", description = "Womens Soccer Cleats", price = "$35.99", category  = category2)
session.add(item5)
session.commit()

item6 = Item(name = "Chicken Wire", description = "Kids shin guards", price = "$3.99", category  = category3)
session.add(item6)
session.commit()

item7 = Item(name = "Fluffy Penguin", description = "Kids Eye Protectors", price = "$15.99", category  = category3)
session.add(item7)
session.commit()

item8 = Item(name = "Wilted Flower", description = "Justin Bieber Pool Towel", price = "$32.99", category  = category3)
session.add(item8)
session.commit()

item9 = Item(name = "Duck Beaks", description = "Pokemon Dive Toys", price = "$7.99", category  = category4)
session.add(item9)
session.commit()

item5 = Item(name = "Chocolate Raspberries", description = "Womens Soccer Cleats", price = "$35.99", category  = category4)
session.add(item5)
session.commit()

item6 = Item(name = "Kitten Mittens", description = "Kids shin guards", price = "$3.99", category  = category5)
session.add(item6)
session.commit()

item7 = Item(name = "Turbo Socks", description = "Kids Eye Protectors", price = "$15.99", category  = category6)
session.add(item7)
session.commit()

item8 = Item(name = "Captain Gregory Sprinklers", description = "Justin Bieber Pool Towel", price = "$32.99", category  = category6)
session.add(item8)
session.commit()

item9 = Item(name = "Snickety Sneaks", description = "Pokemon Dive Toys", price = "$7.99", category  = category6)
session.add(item9)
session.commit()

item5 = Item(name = "Paris Scopes", description = "Womens Soccer Cleats", price = "$35.99", category  = category6)
session.add(item5)
session.commit()

item6 = Item(name = "Rancho Cucamunga Corderoys", description = "Kids shin guards", price = "$3.99", category  = category7)
session.add(item6)
session.commit()

item7 = Item(name = "Meatball Maker", description = "Kids Eye Protectors", price = "$15.99", category  = category8)
session.add(item7)
session.commit()

item8 = Item(name = "Pheasant Pheet", description = "Justin Bieber Pool Towel", price = "$32.99", category  = category8)
session.add(item8)
session.commit()

item9 = Item(name = "Playschool Batteries", description = "Pokemon Dive Toys", price = "$7.99", category  = category9)
session.add(item9)
session.commit()

item5 = Item(name = "Chicken Wing Makers", description = "Womens Soccer Cleats", price = "$35.99", category  = category9)
session.add(item5)
session.commit()

item6 = Item(name = "Pretend Sunglasses", description = "Kids shin guards", price = "$3.99", category  = category10)
session.add(item6)
session.commit()

item7 = Item(name = "Landscape Sandals", description = "Kids Eye Protectors", price = "$15.99", category  = category11)
session.add(item7)
session.commit()

item8 = Item(name = "Rotating Flippers", description = "Justin Bieber Pool Towel", price = "$32.99", category  = category12)
session.add(item8)
session.commit()

item9 = Item(name = "Chinese Leg Warmers", description = "Pokemon Dive Toys", price = "$7.99", category  = category13)
session.add(item9)
session.commit()

item5 = Item(name = "Aristocratic Training Gloves", description = "Womens Soccer Cleats", price = "$35.99", category  = category13)
session.add(item5)
session.commit()

item6 = Item(name = "Realistic Duck Noises", description = "Kids shin guards", price = "$3.99", category  = category14)
session.add(item6)
session.commit()

item7 = Item(name = "Carnival Animals", description = "Kids Eye Protectors", price = "$15.99", category  = category15)
session.add(item7)
session.commit()

item8 = Item(name = "Pudding Slinger", description = "Justin Bieber Pool Towel", price = "$32.99", category  = category14)
session.add(item8)
session.commit()

item9 = Item(name = "Baby-mate Curb Cleaner", description = "Pokemon Dive Toys", price = "$7.99", category  = category15)
session.add(item9)
session.commit()
print "Added some stuff to the catalog stuff!"
