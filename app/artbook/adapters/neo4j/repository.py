import uuid

from artbook.adapters.repository import AbstractRepository
from artbook.domain.models import Artist, Artwork


class ArtistRepository(AbstractRepository):
    def add(self, artist:Artist) -> str:
        return self.db.read_transaction(self.__add_artist, artist)

    def get(self, id) -> Artist:
        result = self.db.read_transaction(self.__get_artist_by_id, id)
        if result:
            return Artist.hydrate(result)
        return None

    def all(self):
        results = self.db.read_transaction(self.__get_all_artists)
        return [Artist.hydrate(record) for record in results]


    @staticmethod
    def __add_artist(tx, artist):
        query = (
            '''
            CREATE (artist:Artist {id: $id, name: $name}) 
            RETURN artist
            '''
        )
        params = {
            'id': str(uuid.uuid4()),
            'name': artist.name
        }
        result = tx.run(query, params).single()

        if result and result.get('artist'):
            return result['artist']['id']
        return None

    @staticmethod
    def __get_artist_by_id(tx, id):
        query = (
            '''
            MATCH (artist:Artist {id: $id}) 
            RETURN artist
            '''
        )
        result = tx.run(query, id=id).single()

        if result and result.get('artist'):
            return result['artist']
        return None 

    @staticmethod
    def __get_all_artists(tx):
        query = (
            '''
            MATCH (artist:Artist) 
            RETURN artist
            '''
        )
        results = list(tx.run(query))

        return [record['artist'] for record in results]


class ArtworkRepository(AbstractRepository):
    def add(self, artwork:Artwork) -> str:
        return self.db.read_transaction(self.__add_artwork, artwork)

    def get(self, id) -> Artwork:
        result = self.db.read_transaction(self.__get_artwork_by_id, id)
        if result:
            return Artwork.hydrate(result)
        return None
    
    def all(self):
        results = self.db.read_transaction(self.__get_all_artworks)
        return [Artwork.hydrate(record) for record in results]
    
    def get_authors(self, artwork_id):
        results = self.db.read_transaction(self.__get_artwork_authors, artwork_id)
        return [Artist.hydrate(record) for record in results]

    def add_author(self, artwork_id, artist_id):
        result = self.db.read_transaction(self.__add_artwork_author, artwork_id, artist_id)
        return result


    @staticmethod
    def __add_artwork(tx, artwork):
        query = (
            '''
            CREATE (artwork:Artwork {id: $id, title: $title, creation: $creation}) 
            RETURN artwork
            '''
        )
        params = {
            'id': str(uuid.uuid4()),
            'title': artwork.title,
            'creation': artwork.creation
        }
        result = tx.run(query, params).single()

        if result and result.get('artwork'):
            return result['artwork']['id']
        return None

    @staticmethod
    def __get_artwork_by_id(tx, id):
        query = (
            '''
            MATCH (artwork:Artwork {id: $id}) 
            RETURN artwork
            '''
        )
        result = tx.run(query, id=id).single()

        if result and result.get('artwork'):
            return result['artwork']
        return None 

    @staticmethod
    def __get_all_artworks(tx):
        query = (
            '''
            MATCH (artwork:Artwork) 
            RETURN artwork
            '''
        )
        results = list(tx.run(query))

        return [record['artwork'] for record in results]

    @staticmethod
    def __get_artwork_authors(tx, artwork_id):
        query = (
            '''
            MATCH (author:Artist)-[:AUTHOR_OF]->(artwork:Artwork {id: $artwork_id}) 
            RETURN author
            '''
        )
        results = list(tx.run(query, artwork_id=artwork_id))

        return [record['author'] for record in results]

    @staticmethod
    def __add_artwork_author(tx, artwork_id, artist_id):
        query = (
            '''
            MATCH (artist:Artist {id: $artist_id}) 
            MATCH (artwork:Artwork {id: $artwork_id}) 
            CREATE (artist)-[:AUTHOR_OF]->(artwork) 
            RETURN artwork, artist
            '''
        )
        params = {
            'artwork_id': artwork_id,
            'artist_id': artist_id
        }
        result = tx.run(query, params)

        return [{"artwork": record["artwork"]["id"], "artist": record["artist"]["id"]} for record in result]
        
