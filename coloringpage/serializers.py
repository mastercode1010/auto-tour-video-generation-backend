from rest_framework import serializers
from .models import ColoringPage

class ColoringPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColoringPage
        fields = ['id', 'customer', 'camera', 'coloringpage', 'wait_for_sec', 'text', 'date']
        extra_kwargs = {'coloringpage': {'required': False}}  # Initially set to optional

    def validate(self, attrs):
        if self.instance is None and 'coloringpage' not in attrs:
            # This is a create operation and coloringpage is missing
            raise serializers.ValidationError({"coloringpage": ["This field is required for creation."]})
        return attrs

    def create(self, validated_data):
        return ColoringPage.objects.create(**validated_data)

    def update(self, instance, validated_data):
        coloringpage = validated_data.pop('coloringpage', None)

        if coloringpage is not None:
            if instance.coloringpage:
                instance.coloringpage.delete(save=False)  # Optionally delete the old file
            instance.coloringpage = coloringpage

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
