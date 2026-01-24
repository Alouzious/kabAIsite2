from rest_framework import serializers
from .models import TeamMember

class TeamMemberSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    photo_thumbnail_url = serializers.SerializerMethodField()
    is_current = serializers.ReadOnlyField()
    display_title = serializers.ReadOnlyField()

    class Meta:
        model = TeamMember
        fields = [
            'id',
            'name',
            'title',
            'display_title',
            'bio',
            'photo_url',
            'photo_thumbnail_url',
            'email',
            'phone',
            'linkedin_url',
            'twitter_url',
            'github_url',
            'website_url',
            'start_year',
            'end_year',
            'joined_date',
            'is_executive',
            'is_active',
            'order',
            'is_current',
            'created_at',
            'updated_at',
        ]

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.photo.url) if request else obj.photo.url
        return None

    def get_photo_thumbnail_url(self, obj):
        if obj.photo_thumbnail:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.photo_thumbnail.url) if request else obj.photo_thumbnail.url
        return None