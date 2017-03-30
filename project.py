
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Catalog, Base, Category, Item

#New Imports for OAuth
from flask import session as login_session
import random, string

#imports for auth step
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(open('client_secrets.json','r').read())['web']['client_id']

app = Flask(__name__)

engine = create_engine('sqlite:///productcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# @app.route('/catalogs/<int:catalog_id>/categories/JSON')
# def catalogCategoriesJSON(restaurant_id):
#     restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
#     items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
#     return jsonify(MenuItems=[i.serialize for i in items])

"""Google Connect authentication Method"""
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['label'] = 'logout'

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

"""Google Disonnect authentication Method"""
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['credentials']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: ' 
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['credentials']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['credentials'] 
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
    return render_template('main.html')

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html')
    #return "The current session state is %s" %login_session['state']

@app.route('/logout')
def showLogout():
    return render_template('logout.html')

@app.route('/JSON')
def catalogMainPageJSON():
    catalogs = session.query(Catalog).all()
    return jsonify(Catalogs=[cat.serializeCat for cat in catalogs])

"""The Main Page"""
@app.route('/main')
@app.route('/')
def catalogMainPage():
    catalogs = session.query(Catalog).all()
    if 'username' not in login_session:
        loggedin='False'
        return render_template('main.html',catalogs=catalogs,logged_in=loggedin)
    else:
        loggedin='True'
        return render_template('main.html',catalogs=catalogs,logged_in=loggedin)

@app.route('/<int:catalog_id>/categories')
def categoriesByCatalog(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    catalogs = session.query(Catalog).all()
    categories = session.query(Category).filter_by(catalog_id=catalog_id).all()
    return render_template('catalog.html',catalog=catalog,catalogs=catalogs,categories=categories)

@app.route('/<int:catalog_id>/categories/<int:category_id>/items')
def itemsByCategory(catalog_id,category_id):
    """
    Shows the Categories belonging to the Selected Catalog.
    Also shows the Selected Catalog as a highlighted selection in the list
    of Catalogs.
    """
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    catalogs = session.query(Catalog).all()
    category = session.query(Category).filter_by(catalog_id=catalog_id,id=category_id).one()
    categories = session.query(Category).filter_by(catalog_id=catalog_id).all()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('itemsList.html',catalog=catalog,catalogs=catalogs,category=category,categories=categories,items=items)

@app.route('/items/<int:item_id>/description')
def descByItem(item_id):
    """
    Shows the detailed information about the item on a separate page from the
    selections screens.
    """
    item = session.query(Item).filter_by(id=item_id).one()
    return(render_template('itemdescription.html',item=item))

@app.route('/newcatalog',methods=['GET','POST'])
def newCatalog():
    """
    Requires a user to be logged in. If they are not logged in, they are
    automatically redirected to the login page.
    """
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCatalog = Catalog(name=request.form['name'],description=request.form['description'])
        session.add(newCatalog)
        session.commit()
        catalogs=session.query(Catalog).all()
        flash("New Catalog Created!")
        return render_template('main.html',catalogs=catalogs)
    else:
        return render_template('newcatalog.html')

@app.route('/<int:catalog_id>/newcategory',methods=['GET','POST'])
def newCategory(catalog_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'],description=request.form['description'],catalog_id=catalog_id)
        session.add(newCategory)
        session.commit()
        catalogs = session.query(Catalog).all()
        catalog = session.query(Catalog).filter_by(id=catalog_id).one()
        categories=session.query(Category).filter_by(catalog_id=catalog_id)
        flash("New Category Created!")
        return render_template('catalog.html',catalog=catalog,catalogs=catalogs,categories=categories)
    else:
        catalog = session.query(Catalog).filter_by(id=catalog_id).one()
        return render_template('newcategory.html',catalog=catalog)

@app.route('/<int:catalog_id>/<int:category_id>/newitem',methods=['GET','POST'])
def newItem(catalog_id,category_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newItem = Item(name=request.form['name'],description=request.form['description'],price=request.form['price'],category_id=category_id)
        session.add(newItem)
        session.commit()
        catalogs = session.query(Catalog).all()
        catalog = session.query(Catalog).filter_by(id=catalog_id).one()
        categories=session.query(Category).filter_by(catalog_id=catalog_id)
        category = session.query(Category).filter_by(id=category_id).one()
        items = session.query(Item).filter_by(category_id=category_id).all()
        flash("New Item Created!")
        return render_template('itemsList.html',catalog=catalog,catalogs=catalogs,category=category,categories=categories,items=items)
    else:
        return render_template('newitem.html',catalog_id=catalog_id,category_id=category_id)


@app.route('/<int:catalog_id>/editcatalog',methods=['GET','POST'])
def editCatalog(catalog_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedCatalog = session.query(Catalog).filter_by(id=catalog_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCatalog.name = request.form['name']
        if request.form['description']:
            editedCatalog.description = request.form['description']
        session.add(editedCatalog)
        session.commit()
        catalogs=session.query(Catalog).all()
        flash("Catalog Edits Saved!")
        return render_template('main.html',catalogs=catalogs)
    else:
        catalog = session.query(Catalog).filter_by(id=catalog_id).one()
        return render_template('editcatalog.html',catalog=catalog)

@app.route('/<int:category_id>/editcategory',methods=['GET','POST'])
def editCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
        if request.form['description']:
            editedCategory.description = request.form['description']
        session.add(editedCategory)
        session.commit()
        category = session.query(Category).filter_by(id=category_id).one()
        ctlg_id = category.catalog_id
        catalogs = session.query(Catalog).all()
        catalog = session.query(Catalog).filter_by(id=ctlg_id).one()
        categories=session.query(Category).filter_by(catalog_id=ctlg_id).all()
        flash("Category Edits Saved!")
        return render_template('catalog.html',catalog=catalog,catalogs=catalogs,categories=categories)
    else:
        category = session.query(Category).filter_by(id=category_id).one()
        return render_template('editcategory.html',category=category)

@app.route('/<int:item_id>/edititem',methods=['GET','POST'])
def editItem(item_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        itm = session.query(Item).filter_by(id=item_id).one()
        ctgry_id = itm.category_id
        category = session.query(Category).filter_by(id=ctgry_id).one()
        ctlg_id = category.catalog_id
        catalog = session.query(Catalog).filter_by(id=ctlg_id).one()
        catalogs = session.query(Catalog).all()
        categories=session.query(Category).filter_by(catalog_id=ctlg_id).all()
        items = session.query(Item).filter_by(category_id=ctgry_id).all()
        flash("Item Edits Saved!")
        return render_template('itemsList.html',catalog=catalog,catalogs=catalogs,category=category,categories=categories,items=items)
    else:
        item = session.query(Item).filter_by(id=item_id).one()
        category = session.query(Category).filter_by(id=item.category_id).one()
        catalog = session.query(Catalog).filter_by(id=category.catalog_id).one()
        return render_template('edititem.html',item=item,category=category,catalog=catalog)


@app.route('/<int:catalog_id>/deletecatalog',methods=['GET','POST'])
def deleteCatalog(catalog_id):
    if 'username' not in login_session:
        return redirect('/login')
    deletedCatalog = session.query(Catalog).filter_by(id=catalog_id).one()
    if request.method == 'POST':
        categories = session.query(Category).filter_by(catalog_id=catalog_id).all()
        for c in categories:
            items = session.query(Item).filter_by(category_id=c.id).all()
            for i in items:
                session.delete(i)
            session.delete(c)
        session.delete(deletedCatalog)
        session.commit()
        catalogs=session.query(Catalog).all()
        flash("Catalog Deleted!")
        return render_template('main.html',catalogs=catalogs)
    else:
        catalog = session.query(Catalog).filter_by(id=catalog_id).one()
        return render_template('deletecatalog.html',catalog=deletedCatalog)

@app.route('/<int:category_id>/deletecategory',methods=['GET','POST'])
def deleteCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    deletedCategory = session.query(Category).filter_by(id=category_id).one()
    ctlg_id = deletedCategory.catalog_id
    if request.method == 'POST':
        items = session.query(Item).filter_by(category_id = category_id).all()
        for i in items:
            session.delete(i)
        session.delete(deletedCategory)
        session.commit()
        catalogs = session.query(Catalog).all()
        catalog = session.query(Catalog).filter_by(id=ctlg_id).one()
        categories=session.query(Category).filter_by(catalog_id=ctlg_id).all()
        flash("Category Deleted!")
        return render_template('catalog.html',catalog=catalog,catalogs=catalogs,categories=categories)
    else:
        category = session.query(Category).filter_by(id=category_id).one()
        return render_template('deletecategory.html',category=category)

@app.route('/<int:item_id>/deleteitem',methods=['GET','POST'])
def deleteItem(item_id):
    if 'username' not in login_session:
        return redirect('/login')
    deletedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        ctgry_id = deletedItem.category_id
        session.delete(deletedItem)
        session.commit()
        items = session.query(Item).filter_by(category_id=ctgry_id).all()
        category = session.query(Category).filter_by(id=ctgry_id).one()
        ctlg_id = category.catalog_id
        categories=session.query(Category).filter_by(catalog_id=ctlg_id).all()
        catalog = session.query(Catalog).filter_by(id=ctlg_id).one()
        catalogs = session.query(Catalog).all()
        
        flash("Item Edits Saved!")
        return render_template('itemsList.html',catalog=catalog,catalogs=catalogs,category=category,categories=categories,items=items)
    else:
        item = session.query(Item).filter_by(id=item_id).one()
        return render_template('deleteitem.html',item=item)

"""Secret Key for Google Login"""
if __name__ == '__main__':
    app.secret_key = 'Cjp0ufWo5dRf9KLR5K-4jRkk'
    app.debug = True
    app.run(host='0.0.0.0', port=5555)
