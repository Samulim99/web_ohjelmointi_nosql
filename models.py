import pymongo
from bson.objectid import ObjectId
from pymongo.server_api import ServerApi
from passlib.hash import pbkdf2_sha256 as sha256

from errors.not_found import NotFound

client = pymongo.MongoClient('mongodb+srv://Samulim99:Masipallo1@cluster0.xyopk.mongodb.net/Projekti1?retryWrites=true&w=majority')
db = client.group2

class User:
    

    def __init__(self, username, password=None, role='user', _id=None):
        self.username = username
        self.password = password
        self.role = role
        if _id is not None:
            _id = str(_id)
        self._id = _id

    def update(self):
        db.users.update_one({'_id': ObjectId(self._id)},
        {
            '$set': {'username': self.username}
        })

    @staticmethod
    def update_by_id(_id, new_username):
        db.users.update_one({'_id': ObjectId(_id)},{
            '$set': {'username': new_username}
        })

        user = User.get_by_id(_id)
        return user

    def delete(self):
        db.users.delete_one({'_id': ObjectId(self._id)})

    """ @staticmethod
    def delete_by_id(_id):
        db.users.delete_one({'_id': ObjectId(_id)}) """

    #CRUD:n R (READ) => haetaan kaikki käyttäjät
    @staticmethod
    def get_all():
        users = []
        users_cursor = db.users.find()
        for user in users_cursor:
            users.append(User(user['username'], _id=user['_id']))
        return users

    @staticmethod
    def get_by_username(username):
        user_dictionary = db.users.find_one({'username': username})
        if user_dictionary is None:
            raise NotFound(message='User not found')
        user = User(username, password=user_dictionary['password'], _id=user_dictionary['_id'])
        return user

    @staticmethod
    def get_by_id(_id):
        user_dictionary = db.users.find_one({'_id': ObjectId(_id)})
        user = User(user_dictionary['username'], _id=_id)
        return user

    #CRUD:n C (lisätään käyttäjä)
    def create(self):
        result = db.users.insert_one({
            'username': self.username,
            'password': sha256.hash(self.password),
            'role': self.role
        })
        self._id = str(result.inserted_id)

    #to_json:iin ei salasanoja!
    def to_json(self):
        user_in_json_format = {
            '_id': str(self._id),
            'username': self.username,
            'role': self.role
        }

        return user_in_json_format

    @staticmethod
    def list_to_json(users):
        users_list_in_json = []
        for user in users:
            users_list_in_json.append(user.to_json())
        return users_list_in_json

class Publication:
    def __init__(self, title, description, url, owner=None, likes=[], shares=0,tags=[], comments=[], visibility=2, share_link=None, _id=None):
            self.title = title
            self.description = description
            self.url = url
            self.owner = owner
            self.likes = likes
            self.shares = shares
            self.tags = tags
            self.comments = comments
            self.visibility = visibility # näkyvyys 2:kaikille, 1: kirjautuneelle, 0: itselle
            self.share_link = share_link
            if _id is not None:
                _id = str(_id)
            self._id = _id

    @staticmethod
    def get_by_owner_and_visibility(user={}, visibility=[2]):
        publications_cursor = db.publications.find({
            '$or': [
                {'visibility': {'$in':visibility}},
                {'owner': ObjectId(user['sub'])}
            ]
        })
        publications = []
        for publication_dictionary in publications_cursor:
            title = publication_dictionary['title']
            description = publication_dictionary['description']
            url = publication_dictionary['url']
            owner = publication_dictionary['owner']
            likes = publication_dictionary['likes']
            tags = publication_dictionary['tags']
            comments = publication_dictionary['comments']
            visibility = publication_dictionary['visibility']
            share_link = publication_dictionary['share_link']
            shares = publication_dictionary['shares']
            _id = publication_dictionary['_id']
            publication = Publication(
                title, 
                description, 
                url, 
                owner=owner, 
                likes=likes, tags=tags, 
                comments=comments, 
                visibility=visibility,
                share_link=share_link, 
                shares=shares,
                _id=_id
            )

            publications.append(publication)

        return publications

                

    def create(self):
        result = db.publications.insert_one({
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'owner': self.owner,
            'likes': self.likes,
            'shares': self.shares,
            'tags': self.tags,
            'comments':self. comments,
            'visibility': self.visibility,
            'share_link': self.share_link
            
        })

        self._id = str(result.inserted_id)

    @staticmethod
    def get_all():
        publications = []
        publications_cursor = db.publications.find()
        for publication in publications_cursor:
            title = publication['title']
            description = publication['description']
            url = publication['url']
            publication_object = Publication(title, description, url)
            publications.append(publication_object)
        
        return publications_cursor

    @staticmethod
    def list_to_json(publications_list):
        publications_in_json_format = []
        for publication in publications_list:
            publication_in_json_format = publication.to_json
            publications_in_json_format.append(publication_in_json_format)
        return publications_in_json_format




    def to_json(self):
        publication_in_json_format = {
            '_id': self._id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'owner': self.owner,
            'likes': self.likes,
            'shares': self.shares,
            'tags': self.tags,
            'comments':self. comments,
            'visibility': self.visibility,
            'share_link': self.share_link

        }
        return publication_in_json_format