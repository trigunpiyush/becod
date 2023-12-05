from rest_framework import serializers
from .models import User, Challenges, BlogPost


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
        
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class ChallengesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenges
        fields = ["problemstatement","sample_input_1","sample_output_1","image","explanations","stack","level","rating"] 

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ["title","content","writer","created_at"]