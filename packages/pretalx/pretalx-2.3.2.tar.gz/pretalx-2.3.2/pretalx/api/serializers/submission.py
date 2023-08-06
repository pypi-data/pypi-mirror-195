from functools import partial

from i18nfield.rest_framework import I18nAwareModelSerializer
from rest_framework.serializers import (
    Field,
    ModelSerializer,
    SerializerMethodField,
    SlugRelatedField,
)

from pretalx.api.serializers.question import AnswerSerializer
from pretalx.api.serializers.speaker import SubmitterSerializer
from pretalx.schedule.models import Schedule, TalkSlot
from pretalx.submission.models import Resource, Submission, SubmissionStates, Tag


class FileField(Field):
    """Serializer class for Django Restframework."""

    read_only = True
    write_only = False
    label = None
    source = "*"

    def to_representation(self, value):
        return value.url


class ResourceSerializer(ModelSerializer):
    resource = FileField()

    class Meta:
        model = Resource
        fields = ("resource", "description")


class SlotSerializer(I18nAwareModelSerializer):
    room = SlugRelatedField(slug_field="name", read_only=True)
    end = SerializerMethodField()

    @staticmethod
    def get_end(obj):
        return obj.real_end

    class Meta:
        model = TalkSlot
        fields = ("room", "start", "end")


class SubmissionSerializer(I18nAwareModelSerializer):
    submission_type = SlugRelatedField(slug_field="name", read_only=True)
    track = SlugRelatedField(slug_field="name", read_only=True)
    slot = SlotSerializer(
        TalkSlot.objects.none().filter(is_visible=True), read_only=True
    )
    duration = SerializerMethodField()
    speakers = SerializerMethodField()
    resources = ResourceSerializer(Resource.objects.none(), read_only=True, many=True)
    title = SerializerMethodField()
    abstract = SerializerMethodField()
    description = SerializerMethodField()

    @staticmethod
    def get_duration(obj):
        return obj.get_duration()

    def get_speakers(self, obj):
        has_slots = (
            obj.slots.filter(is_visible=True)
            and obj.state == SubmissionStates.CONFIRMED
        )
        if has_slots or self.can_view_speakers:
            return SubmitterSerializer(
                obj.speakers.all(),
                many=True,
                context=self.context,
                event=self.event,
            ).data
        return []

    def get_attribute(self, obj, attribute=None):
        if self.can_view_speakers:
            return getattr(obj, attribute, None)
        return obj.anonymised.get(attribute) or getattr(obj, attribute, None)

    def __init__(self, *args, **kwargs):
        self.can_view_speakers = kwargs.pop("can_view_speakers", False)
        self.event = kwargs.pop("event", None)
        super().__init__(*args, **kwargs)
        for field in ("title", "abstract", "description"):
            setattr(self, f"get_{field}", partial(self.get_attribute, attribute=field))

    class Meta:
        model = Submission
        fields = [
            "code",
            "speakers",
            "title",
            "submission_type",
            "track",
            "state",
            "abstract",
            "description",
            "duration",
            "slot_count",
            "do_not_record",
            "is_featured",
            "content_locale",
            "slot",
            "image",
            "resources",
        ]


class TagSerializer(I18nAwareModelSerializer):
    class Meta:
        model = Tag
        fields = ["tag", "description", "color"]


class SubmissionOrgaSerializer(SubmissionSerializer):
    answers = AnswerSerializer(many=True)
    tags = SerializerMethodField()
    created = SerializerMethodField()

    def get_created(self, obj):
        return obj.created.astimezone(obj.event.tz).isoformat()

    def get_tags(self, obj):
        return list(obj.tags.all().values_list("tag", flat=True))

    class Meta(SubmissionSerializer.Meta):
        fields = SubmissionSerializer.Meta.fields + [
            "created",
            "pending_state",
            "answers",
            "notes",
            "internal_notes",
            "tags",
        ]


class SubmissionReviewerSerializer(SubmissionOrgaSerializer):
    answers = AnswerSerializer(many=True, source="reviewer_answers")

    class Meta(SubmissionOrgaSerializer.Meta):
        pass


class ScheduleListSerializer(ModelSerializer):
    version = SerializerMethodField()

    @staticmethod
    def get_version(obj):
        return obj.version or "wip"

    class Meta:
        model = Schedule
        fields = ("version", "published")


class ScheduleSerializer(ModelSerializer):
    slots = SubmissionSerializer(
        Submission.objects.none().filter(state=SubmissionStates.CONFIRMED), many=True
    )

    class Meta:
        model = Schedule
        fields = ("slots", "version")
