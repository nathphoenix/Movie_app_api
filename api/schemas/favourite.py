from ..ma import ma 
from ..models.favourite import FavouriteModel

class FavouriteSchema(ma.ModelSchema):
    class Meta:
        model = FavouriteModel  
        load_only = ("id") 
        dump_only = ("id")
        #include_fk = True
        
        
class FavouriteItemSchema(ma.ModelSchema):
    class Meta:
        model = FavouriteModel  
        load_only = ("id") 
        dump_only = ("id")