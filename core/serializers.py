from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
# from store.models import Customer

class UserCreateSerializer(BaseUserCreateSerializer):
    # def save(self, **kwargs):
    #     user = super().save(**kwargs)
    #     Customer.object.create(user=user)
    
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
        

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
