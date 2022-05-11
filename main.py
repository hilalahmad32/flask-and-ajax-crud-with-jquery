from flask import Flask, render_template, request 
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SECRET_KEY']=''
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///crud.sqlite'
db=SQLAlchemy(app)
# create table
class Product(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(255), nullable=False)
    content=db.Column(db.Text(), nullable=False)
    price=db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Product("{self.title},{self.content},{self.price},{self.id}")'

db.create_all()
@app.route('/')
def index():
    return render_template('index.html',title="Index Page")

# insert - data
@app.route('/insert-data',methods=['POST'])
def insertData():
    if request.method == 'POST':
        title=request.form.get('title')
        content=request.form.get('content')
        price=request.form.get('price')
        data=Product(title=title,content=content,price=price)
        db.session.add(data)
        db.session.commit()
        return '1'
       
# select data
@app.route('/select-data')
def selectData():
    products=Product.query.all()
    output=""
    for product in products:
        output +=f"<tr><td>{product.id}</td><td>{product.title}</td><td>{product.content}</td><td>{product.price}</td><td><button class='btn btn-success' data-toggle='modal' data-target='#update-product' id='edit' data-id='{product.id}'>Edit</button></td><td><button id='delete' data-id='{product.id}' class='btn btn-danger'>Delete</button></td><tr>"
    return output
# get total count
@app.route('/total-data')
def totalData():
    products=Product.query.count()
    return f'{products}'

# delete data
@app.route('/delete-data')
def deleteData():
    id=request.args.get('id')
    product=Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return '1'

# edit data
@app.route('/edit-data')
def editData():
    id=request.args.get('id')
    products=Product.query.filter_by(id=id).first()
    output=""
    output +=f'''<div class="form-group">
                        <label for="title">Product Title</label>
                        <input type="text" class="form-control" value="{products.title}" id="edit_title" aria-describedby="edit_title"
                            placeholder="Enter email">
                        <input type="hidden" class="form-control" value="{products.id}" id="id" aria-describedby="title"
                            placeholder="Enter email">
                    </div>
                    <div class="form-group">
                        <label for="content">Product Content</label>
                        <input type="text" class="form-control" value="{products.content}" id="edit_content" placeholder="edit_content">
                    </div>
                    <div class="form-group">
                        <label for="price">Product Price</label>
                        <input type="number" class="form-control" value="{products.price}" id="edit_price" placeholder="price">
                    </div>'''
    return output

# update-data
@app.route('/update-data',methods=['POST'])
def updateData():
    if request.method =='POST':
        id=request.form.get('id')
        content=request.form.get('content')
        price=request.form.get('price')
        title=request.form.get('title')
        Product.query.filter_by(id=id).update(dict(content=content,price=price,title=title))
        db.session.commit()
        return '1'

if __name__=="__main__":
    app.run(debug=True)