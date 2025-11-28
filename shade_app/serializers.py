from rest_framework import serializers
from .models import User, Smile, OurClient, Ceremonial, LoginHistory, Demonstration

# --------------------- USER SERIALIZER ---------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'phone', 'email', 'created_at']


# --------------------- LOGIN HISTORY SERIALIZER ---------------------
class LoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginHistory
        fields = ['id', 'username', 'login_time', 'ip_address', 'user_agent', 'status']


# --------------------- SMILE SERIALIZER ---------------------
class SmileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Smile
        fields = ['id', 'title', 'description', 'image', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


# --------------------- OUR CLIENT SERIALIZER ---------------------
class OurClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurClient
        fields = ['id', 'title', 'description', 'media_type', 'media_file', 'video_url', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        media_type = data.get('media_type', getattr(self.instance, 'media_type', None))
        media_file = data.get('media_file', getattr(self.instance, 'media_file', None))
        video_url = data.get('video_url', getattr(self.instance, 'video_url', None))

        if media_type == 'image' and not media_file:
            raise serializers.ValidationError("media_file is required for image type")
        
        if media_type == 'video' and not video_url:
            raise serializers.ValidationError("video_url is required for video type")
        
        return data


# --------------------- CEREMONIAL SERIALIZER ---------------------
class CeremonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ceremonial
        fields = ['id', 'title', 'description', 'media_type', 'media_file', 'video_url', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        media_type = data.get('media_type', getattr(self.instance, 'media_type', None))
        media_file = data.get('media_file', getattr(self.instance, 'media_file', None))
        video_url = data.get('video_url', getattr(self.instance, 'video_url', None))

        if media_type == 'image' and not media_file:
            raise serializers.ValidationError("media_file is required for image type")
        
        if media_type == 'video' and not video_url:
            raise serializers.ValidationError("video_url is required for video type")
        
        return data


# --------------------- DEMONSTRATION SERIALIZER ---------------------
class DemonstrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demonstration
        fields = ['id', 'title', 'description', 'media_type', 'media_file', 'video_url', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        media_type = data.get('media_type', getattr(self.instance, 'media_type', None))
        media_file = data.get('media_file', getattr(self.instance, 'media_file', None))
        video_url = data.get('video_url', getattr(self.instance, 'video_url', None))

        if media_type == 'image' and not media_file:
            raise serializers.ValidationError("media_file is required for image type")
        
        if media_type == 'video' and not video_url:
            raise serializers.ValidationError("video_url is required for video type")
        
        return data