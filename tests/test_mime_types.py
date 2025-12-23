import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.mime_types import (
    Application,
    Audio,
    Font,
    Haptics,
    Image,
    Message,
    MimeType,
    Model,
    Multipart,
    Text,
    Video,
    _index_by_category,
    _index_by_mime_type,
)


@pytest.fixture(scope='module', name='ResponseModel')
def response_model_fixture():
    class Response(BaseModel):
        content_type: MimeType

    return Response


class TestMimeTypeValidation:
    """Test MimeType validation."""

    def test_valid_mime_type_application_json(self, ResponseModel):
        """Test validation of application/json."""
        response = ResponseModel(content_type='application/json')
        assert response.content_type == 'application/json'
        assert response.content_type.category == 'application'

    def test_valid_mime_type_text_html(self, ResponseModel):
        """Test validation of text/html."""
        response = ResponseModel(content_type='text/html')
        assert response.content_type == 'text/html'
        assert response.content_type.category == 'text'

    def test_valid_mime_type_image_png(self, ResponseModel):
        """Test validation of image/png."""
        response = ResponseModel(content_type='image/png')
        assert response.content_type == 'image/png'
        assert response.content_type.category == 'image'

    def test_valid_mime_type_video_mp4(self, ResponseModel):
        """Test validation of video/mp4."""
        response = ResponseModel(content_type='video/mp4')
        assert response.content_type == 'video/mp4'
        assert response.content_type.category == 'video'

    def test_valid_mime_type_audio_mpeg(self, ResponseModel):
        """Test validation of audio/mpeg."""
        response = ResponseModel(content_type='audio/mpeg')
        assert response.content_type == 'audio/mpeg'
        assert response.content_type.category == 'audio'

    def test_case_insensitive_lowercase(self, ResponseModel):
        """Test case-insensitive validation with lowercase input."""
        response = ResponseModel(content_type='application/json')
        assert response.content_type == 'application/json'

    def test_case_insensitive_uppercase(self, ResponseModel):
        """Test case-insensitive validation with uppercase input."""
        response = ResponseModel(content_type='APPLICATION/JSON')
        assert response.content_type == 'application/json'

    def test_case_insensitive_mixed_case(self, ResponseModel):
        """Test case-insensitive validation with mixed case input."""
        response = ResponseModel(content_type='ApPlIcAtIoN/JsOn')
        assert response.content_type == 'application/json'

    def test_invalid_mime_type(self, ResponseModel):
        """Test that invalid MIME types raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ResponseModel(content_type='invalid/mimetype')
        assert 'Invalid MIME type' in str(exc_info.value)

    def test_invalid_format(self, ResponseModel):
        """Test that incorrectly formatted MIME types raise ValidationError."""
        with pytest.raises(ValidationError):
            ResponseModel(content_type='not-a-mime-type')

    def test_empty_string(self, ResponseModel):
        """Test that empty string raises ValidationError."""
        with pytest.raises(ValidationError):
            ResponseModel(content_type='')

    def test_mime_type_with_special_characters(self, ResponseModel):
        """Test MIME type with special characters like application/vnd.api+json."""
        response = ResponseModel(content_type='application/vnd.api+json')
        assert response.content_type == 'application/vnd.api+json'
        assert response.content_type.category == 'application'


class TestMimeTypeProperties:
    """Test MimeType properties."""

    def test_category_property_application(self):
        """Test category property returns correct category for application."""

        class Model(BaseModel):
            mime: MimeType

        m = Model(mime='application/json')
        assert m.mime.category == 'application'

    def test_category_property_text(self):
        """Test category property returns correct category for text."""

        class Model(BaseModel):
            mime: MimeType

        m = Model(mime='text/plain')
        assert m.mime.category == 'text'

    def test_category_property_image(self):
        """Test category property returns correct category for image."""

        class Model(BaseModel):
            mime: MimeType

        m = Model(mime='image/jpeg')
        assert m.mime.category == 'image'


class TestBackwardCompatibility:
    """Test backward compatibility with enum classes."""

    def test_application_enum_exists(self):
        """Test that Application enum still exists."""
        assert hasattr(Application, 'APPLICATION_JSON')
        assert Application.APPLICATION_JSON == 'application/json'

    def test_audio_enum_exists(self):
        """Test that Audio enum still exists."""
        assert hasattr(Audio, 'AUDIO_MPEG')
        assert Audio.AUDIO_MPEG == 'audio/mpeg'

    def test_image_enum_exists(self):
        """Test that Image enum still exists."""
        assert hasattr(Image, 'IMAGE_PNG')
        assert Image.IMAGE_PNG == 'image/png'

    def test_video_enum_exists(self):
        """Test that Video enum still exists."""
        assert hasattr(Video, 'VIDEO_MP4')
        assert Video.VIDEO_MP4 == 'video/mp4'

    def test_text_enum_exists(self):
        """Test that Text enum still exists."""
        assert hasattr(Text, 'TEXT_HTML')
        assert Text.TEXT_HTML == 'text/html'

    def test_font_enum_exists(self):
        """Test that Font enum still exists."""
        assert Font is not None

    def test_haptics_enum_exists(self):
        """Test that Haptics enum still exists."""
        assert Haptics is not None

    def test_message_enum_exists(self):
        """Test that Message enum still exists."""
        assert Message is not None

    def test_model_enum_exists(self):
        """Test that Model enum still exists."""
        assert Model is not None

    def test_multipart_enum_exists(self):
        """Test that Multipart enum still exists."""
        assert Multipart is not None


class TestHelperFunctions:
    """Test helper/indexing functions."""

    def test_index_by_mime_type_has_entries(self):
        """Test that _index_by_mime_type returns a populated dictionary."""
        index = _index_by_mime_type()
        assert len(index) > 0
        assert 'application/json' in index

    def test_index_by_category_has_all_categories(self):
        """Test that _index_by_category has all expected categories."""
        index = _index_by_category()
        expected_categories = [
            'application',
            'audio',
            'font',
            'haptics',
            'image',
            'message',
            'model',
            'multipart',
            'text',
            'video',
        ]
        for category in expected_categories:
            assert category in index
            assert len(index[category]) > 0

    def test_index_by_category_application_has_json(self):
        """Test that application category includes application/json."""
        index = _index_by_category()
        assert 'application/json' in index['application']


class TestMimeTypeInModels:
    """Test MimeType usage in various model scenarios."""

    def test_optional_mime_type(self):
        """Test optional MimeType field."""
        from typing import Optional

        class Model(BaseModel):
            content_type: Optional[MimeType] = None

        m1 = Model()
        assert m1.content_type is None

        m2 = Model(content_type='application/json')
        assert m2.content_type == 'application/json'

    def test_list_of_mime_types(self):
        """Test list of MimeType fields."""
        from typing import List

        class Model(BaseModel):
            accepted_types: List[MimeType]

        m = Model(accepted_types=['application/json', 'text/html', 'image/png'])
        assert len(m.accepted_types) == 3
        assert m.accepted_types[0] == 'application/json'
        assert m.accepted_types[1] == 'text/html'
        assert m.accepted_types[2] == 'image/png'

    def test_mime_type_serialization(self):
        """Test that MimeType serializes correctly."""

        class Model(BaseModel):
            content_type: MimeType

        m = Model(content_type='application/json')
        assert m.model_dump() == {'content_type': 'application/json'}
        assert m.model_dump_json() == '{"content_type":"application/json"}'
