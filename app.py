from flask import Flask
from flask import jsonify
from flask import Response
from flask import request
import json
app=Flask(__name__)


books=[{
    'name':'Harry potter',
    'price':12.99,
    'isbn':123456
},
       {
    'name': 'you can win',
    'price': 89.99,
    'isbn': 656767
}
       ,
       {
    'name': 'Happiness is a state of mind',
    'price': 89.99,
    'isbn': 1234
}
       ]

@app.route('/')
def hello_world():
    return 'test'

@app.route('/books')
def get_books():
    return jsonify(books)

@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    foundBook={}
    for b in books:
        if(b['isbn']==isbn):
            foundBook=b
            break
    return jsonify(foundBook)

@app.route('/books',methods=['POST'])
def add_book():
    new_book = request.get_json()
    books.insert(0,new_book)
    return jsonify(books)

@app.route('/books/<int:isbn>',methods=['PATCH'])
def update_book(isbn):
    request_book = request.get_json()
    foundBook={}
    updatedBook = {}
    response = Response()
    for b in books:
        if(b['isbn']==isbn):
            foundBook=b
            break
    
    if(foundBook!={}):
        if("name" in request_book):
            updatedBook["name"] = request_book["name"]
        if ("price" in request_book):
            updatedBook["price"] = request_book["price"]
        foundBook.update(updatedBook)
        response = Response("",status=204)
        response.headers["Location"] = '/books/'+str(isbn)
    else:
        response = Response("",status=400)
        
    return response
    
@app.route('/books/<int:isbn>',methods=['DELETE'])
def delete_book(isbn):
    response = Response()
    foundBook=None
    for b in books:
        if(b["isbn"]==isbn):
            foundBook = b
            break
    
    if(foundBook==None):
        response=Response(json.dumps("book not found"),status=404)
    else:
        books.remove(foundBook)
        response=Response(json.dumps("book removed"),status=200)
    
    response.headers["Location"]="/books/"
    
    return response
    
        
           
        
print(__name__)
if __name__ == '__main__':
    app.run(debug=True,port=5000)