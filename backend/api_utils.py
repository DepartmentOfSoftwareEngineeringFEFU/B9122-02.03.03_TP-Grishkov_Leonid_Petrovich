from rest_framework import serializers


class DecimalAsFloatModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field, serializers.DecimalField):
                field.coerce_to_string = False
            if isinstance(field, serializers.IntegerField):
                pass  # целые и так нормально