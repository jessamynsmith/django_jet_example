from django.db.utils import IntegrityError
from rest_framework import serializers
from people import models


class TagValueField(serializers.Field):
    def get_attribute(self, obj):
        # We pass the object instance onto `to_representation`,
        # not just the field attribute.
        return obj

    def to_representation(self, obj):
        """
        Serialize the object's class name.
        """
        return obj.tag.value

    def to_internal_value(self, data):
        """
        Transform the *incoming* primitive data into a native value.
        """
        return data


class PersonTagSerializer(serializers.ModelSerializer):
    tag_value = TagValueField()

    class Meta:
        model = models.PersonTag
        fields = ('person', 'tag_value')

    def create(self, validated_data):
        tag_value = validated_data.pop('tag_value')
        tag, created = models.Tag.objects.get_or_create(value=tag_value)
        validated_data['tag'] = tag
        try:
            person_tag = super().create(validated_data)
        except IntegrityError:
            person_tag = self.Meta.model.objects.get(**validated_data)
        return person_tag
