from rest_framework import serializers

from .models import Question, Option, Poll, Reply


class DefaultUser(object):
    def set_context(self, serializer_field):
        self.user_id = serializer_field.context['request'].user.id

    def __call__(self):
        return self.user_id


class ReplySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(default=DefaultUser())
    poll = serializers.SlugRelatedField(queryset=Poll.objects.all(), slug_field='id')
    question = serializers.SlugRelatedField(queryset=Question.objects.all(), slug_field='id')
    option = serializers.SlugRelatedField(queryset=Option.objects.all(), slug_field='id', allow_null=True)
    option_text = serializers.CharField(max_length=300, allow_null=True, required=False)

    class Meta:
        model = Reply
        fields = '__all__'

    def create(self, validated_data):
        return Reply.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class PollSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=500)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()

    class Meta:
        model = Poll
        fields = '__all__'

    def create(self, validated_data):
        return Poll.objects.create(**validated_data)

    def valid_start_date(self, value):
        if self.instance and self.instance.start_date < value:
            raise serializers.ValidationError(
                "Do not alter!"
            )
        return value

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class OptionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    option_text = serializers.CharField(max_length=200)
    question = serializers.SlugRelatedField(queryset=Question.objects.all(), slug_field='id')

    def validate(self, attrs):
        try:
            Option.objects.get(question=attrs['question'].id, option_text=attrs['option_text'])
        except Option.DoesNotExist:
            return attrs
        else:
            raise serializers.ValidationError('Option already done')

    class Meta:
        model = Option
        fields = '__all__'

    def create(self, validated_data):
        return Option.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class QuestionSerializer(serializers.ModelSerializer):
    question_type = serializers.ChoiceField(
        choices=Question.Type.choices, default=Question.Type.TEXT

    )
    id = serializers.IntegerField(read_only=True)
    poll = serializers.SlugRelatedField(queryset=Poll.objects.all(), slug_field='id')
    question_text = serializers.CharField(max_length=200)
    options = OptionSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
