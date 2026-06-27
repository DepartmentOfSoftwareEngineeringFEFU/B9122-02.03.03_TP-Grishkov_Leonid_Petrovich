from rest_framework import serializers
from files.models import File
from django.contrib.contenttypes.models import ContentType


# class FileSerializer(serializers.ModelSerializer):
#     content_type = serializers.SlugRelatedField(
#         slug_field='model',
#         queryset=ContentType.objects.all()
#     )
#     uploaded_by_name = serializers.SerializerMethodField()
#     content_type_name = serializers.SerializerMethodField()
#     object_name = serializers.SerializerMethodField()

#     class Meta:
#         model = File
#         fields = ['id', 'content_type', 'object_id', 'file', 'original_name',
#                   'file_category', 'description', 'uploaded_by', 'uploaded_by_name',
#                   'uploaded_at', 'content_type_name', 'object_name']

#     def get_content_type_name(self, obj):
#         type_names = {
#             'request': 'Заявка',
#             'order': 'Заказ',
#             'product': 'Изделие',
#             'employee': 'Сотрудник',
#             'equipment': 'Оборудование',
#             'income': 'Доход',
#             'expense': 'Расход',
#         }
#         return type_names.get(obj.content_type.model, obj.content_type.model)
    
#     def get_uploaded_by_name(self, obj):
#         user = obj.uploaded_by
#         if hasattr(user, 'employee'):
#             return user.employee.full_name
#         if hasattr(user, 'customer'):
#             return user.customer.name
#         return user.username

#     def get_object_name(self, obj):
#         try:
#             target = obj.content_object
#             if not target:
#                 return str(obj.object_id)
#             if hasattr(target, 'description') and hasattr(target, 'customer'):
#                 return f"Заявка №{target.id} от {target.customer.name}"
#             if hasattr(target, 'product_name'):
#                 return f"Заказ №{target.id} — {target.product_name}"
#             if hasattr(target, 'full_name'):
#                 return target.full_name
#             if hasattr(target, 'name'):
#                 return target.name
#             return str(target)
#         except Exception:
#             return str(obj.object_id)

class FileSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all()
    )
    uploaded_by_name = serializers.SerializerMethodField(read_only=True)
    uploaded_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    content_type_name = serializers.SerializerMethodField()
    object_name = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ['id', 'content_type', 'object_id', 'file', 'original_name',
                  'file_category', 'description', 'uploaded_by', 'uploaded_by_name',
                  'uploaded_at', 'content_type_name', 'object_name']

    def get_uploaded_by_name(self, obj):
        user = obj.uploaded_by
        if hasattr(user, 'employee'):
            return user.employee.full_name
        if hasattr(user, 'customer'):
            return user.customer.name
        return user.username

    def get_content_type_name(self, obj):
        type_names = {
            'request': 'Заявка', 'order': 'Заказ', 'product': 'Изделие',
            'employee': 'Сотрудник', 'equipment': 'Оборудование',
            'income': 'Доход', 'expense': 'Расход',
        }
        return type_names.get(obj.content_type.model, obj.content_type.model)

    def get_object_name(self, obj):
        try:
            target = obj.content_object
            if not target:
                return str(obj.object_id)
            if hasattr(target, 'description') and hasattr(target, 'customer'):
                return f"Заявка №{target.id} от {target.customer.name}"
            if hasattr(target, 'product_name'):
                return f"Заказ №{target.id} — {target.product_name}"
            if hasattr(target, 'full_name'):
                return target.full_name
            if hasattr(target, 'name'):
                return target.name
            return str(target)
        except Exception:
            return str(obj.object_id)