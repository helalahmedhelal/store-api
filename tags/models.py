from django.db import models

# ContentType is like any module but made to allow generic relationships
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# this class to create tagitem manger to not duplicate and redundut the code of querying generic relaltion ship
class TaggedItemManger(models.Manager):
    def get_tags_for_items(self,con_tybe,obj_id):
         content_type=ContentType.objects.get_for_model(con_tybe)
         return TagetItem.objects.select_related('tag').filter(content_type=content_type,object_id=obj_id)
        
class Tag(models.Model):
    lable=models.CharField(max_length=255)
    
class TagetItem(models.Model):
    
    objects=TaggedItemManger()
    # what tag applied to what object
    tag=models.ForeignKey(Tag,on_delete=models.CASCADE)  
    
    #contentType model have many tagedItems
    #on deleting object type we delete taged item
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE) 
    object_id=models.PositiveIntegerField()
    # with content_type and content_id we can identify any object in our application
    
    #get the actual object (read the object that the tag applied to)
    content_object= GenericForeignKey() 
