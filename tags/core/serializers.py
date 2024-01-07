from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer,UserSerializer as BaseUaserSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
     class Meta(BaseUserCreateSerializer.Meta):
         fields=['email','username','password','first_name','last_name']
         
         
class UserSerializer(BaseUaserSerializer):
    class Meta(BaseUaserSerializer.Meta):
        fields=['id','username','email','first_name','last_name']         