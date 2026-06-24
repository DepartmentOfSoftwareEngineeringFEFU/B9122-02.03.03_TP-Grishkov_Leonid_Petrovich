from rest_framework import serializers
from directories.models import ( 
    Position, WorkSchedule, Competence,
    WorkCategory, OperationType, ExpenseCategory,
    Product, Equipment, Material
)

# from api_utils import DecimalAsFloatModelSerializer

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

    def validate_name(self, value):
        if value == 'Директор':
            raise serializers.ValidationError('Нельзя создать вторую должность Директора')
        return value

class WorkScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSchedule
        fields = '__all__'

class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = '__all__'

class WorkCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkCategory
        fields = '__all__'

class OperationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationType
        fields = '__all__'

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

#----------------------------------СТАРЫЙ ВАРИАНТ-------------------------------------


# from rest_framework import serializers
# from directories.models import (
#     Position, WorkSchedule, Competence, WorkCategory,
#     OperationType, ExpenseCategory, Product, Equipment, Material
# )


# class VerboseNameSerializer(serializers.ModelSerializer):
#     """Базовый сериализатор, подставляющий verbose_name из модели."""
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             try:
#                 model_field = self.Meta.model._meta.get_field(field_name)
#                 if hasattr(model_field, 'verbose_name'):
#                     field.label = str(model_field.verbose_name)
#             except Exception:
#                 pass


# class PositionSerializer(VerboseNameSerializer):
#     class Meta:
#         model = Position
#         fields = '__all__'

#     def validate_name(self, value):
#         if value == 'Директор':
#             raise serializers.ValidationError('Нельзя создать вторую должность Директора')
#         return value


# class WorkScheduleSerializer(VerboseNameSerializer):
#     class Meta:
#         model = WorkSchedule
#         fields = '__all__'


# class CompetenceSerializer(VerboseNameSerializer):
#     class Meta:
#         model = Competence
#         fields = '__all__'


# class WorkCategorySerializer(VerboseNameSerializer):
#     class Meta:
#         model = WorkCategory
#         fields = '__all__'


# class OperationTypeSerializer(VerboseNameSerializer):
#     class Meta:
#         model = OperationType
#         fields = '__all__'


# class ExpenseCategorySerializer(VerboseNameSerializer):
#     class Meta:
#         model = ExpenseCategory
#         fields = '__all__'


# class ProductSerializer(VerboseNameSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'


# class EquipmentSerializer(VerboseNameSerializer):
#     class Meta:
#         model = Equipment
#         fields = '__all__'


# class MaterialSerializer(VerboseNameSerializer):
#     class Meta:
#         model = Material
#         fields = '__all__'