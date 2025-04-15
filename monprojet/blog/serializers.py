from rest_framework import serializers
from .models import Article, CustomUser3
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser3
        fields = ['id','username','email','is_verified']





class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # Vérifier si l'utilisateur existe avec cet email
        try:
            user = CustomUser3.objects.get(email=email)
        except CustomUser3.DoesNotExist:
            raise serializers.ValidationError("No user found with this email.")

        # Vérifier le mot de passe
        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password.")

        attrs["username"] = user.username  # Ajouter le username pour SimpleJWT
        return super().validate(attrs)
