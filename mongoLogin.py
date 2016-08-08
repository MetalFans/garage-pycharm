from pymongo import MongoClient
connection = MongoClient("ds015962.mlab.com", 15962)
db = connection["hellomongo"]
db.authenticate("ab101", "1234")
collection = db.books
book = {
    "_id" : 5.0,
    "isbn" : "0131002872",
    "title" : "Thinking in Java",
    "releaseDate" : "2002-12-01",
    "listPrice" : 100.99,
    "pubId" : "PH"
}
collection.insert(book)