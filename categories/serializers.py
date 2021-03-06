from rest_framework import serializers

from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    cards = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'mode', 'cards')
        read_only_fields = ('id',)

    def _get_user(self):
        """Try to retrieve the current user
        """
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        return user

    def create(self, validated_data):
        validated_data['owner'] = self._get_user()

        return super().create(validated_data)
