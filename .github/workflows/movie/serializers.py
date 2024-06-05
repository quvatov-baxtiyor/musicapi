from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Actor,Movie
from datetime import datetime

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

    def validate_birthdate(self, birthdate):
        if birthdate.year < 1950:
            raise ValidationError(detail='Tug\'ilgan yili 1950 dan katta bo\'lishi kerak.')
        return birthdate

    def validate(self, data):
        birthdate = data.get('birthdate')
        if birthdate:
            birthdate = self.validate_birthdate(birthdate)
            data['birthdate'] = birthdate
        return data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'text', 'created_date', 'todo_id', 'user')
        read_only_fields = ('user',)