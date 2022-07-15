from rest_framework import serializers
from watchlist_app.models import Movie

#------3. Validator function ----------- we have to write before class otherwise we get "name_length" not defined Error
def description_length(value):
    if len(value) < 5:
        raise serializers.ValidationError("Description is too short!!")
    else:
        return value  


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(validators=[description_length])
    active = serializers.BooleanField()
    
    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
    
    def update(self, instance, validated_data):  #instance carries old values
        instance.name = validated_data.get('name', instance.name)  # validated_data carries new values 
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance
    
    #--------------Validations----------------   
    #------1. Field Level Validation (here is for name)
    def validate_name(self,value):
        if len(value) < 2:
            raise serializers.ValidationError("Name is too short!")
        else:
            return value
        
    #------2. Object Level Validation (here is for name)
    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError('name and description should be different!')
        else:
            return data
        
    
   