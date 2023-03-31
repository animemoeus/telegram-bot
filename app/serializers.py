from rest_framework import serializers


class TelegramUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    is_bot = serializers.BooleanField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255, required=False, default="")
    username = serializers.CharField(max_length=255, required=False, default="")
    language_code = serializers.CharField(max_length=50, required=False, default="")

    def validate_is_bot(self, value):
        if value:
            raise serializers.ValidationError("Cannot process messages from the bot")

        return value
