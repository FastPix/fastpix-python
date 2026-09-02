"""Model contract tests: pure pydantic round-trips, no network.

Pins the wire-format contracts of the SDK's request/response models — field
types, aliases, defaults, optionality, and serialized body shapes."""

import json

import pytest
from pydantic import ValidationError

from fastpix_python import models
from fastpix_python.models.createlivestreamrequest import (
    CreateLiveStreamRequest,
    InputMediaSettings,
)
from fastpix_python.models.media import Media
from fastpix_python.models.mediaclipresponse import MediaClipResponseData
from fastpix_python.models.playbackidrequest import PlaybackIDRequest
from fastpix_python.models.playbackidresponse import PlaybackIDResponse
from fastpix_python.models.playbackidsuccessresponse import PlaybackIDSuccessResponse
from fastpix_python.models.playbacksettings import PlaybackSettings
from fastpix_python.models.playlistbyidresponse import PlaylistByIDResponseMediaList
from fastpix_python.models.playlistcreatedschema import PlaylistCreatedSchemaMediaList

RESTRICTIONS = {
    "domains": {"defaultPolicy": "deny", "allow": ["example.com"], "deny": []},
    "userAgents": {"defaultPolicy": "allow", "allow": [], "deny": ["PostmanRuntime/7.29.0"]},
}


# ---------------------------------------------------------------------------
# media duration: float seconds, optional
# ---------------------------------------------------------------------------

DURATION_MODELS = [
    Media,
    MediaClipResponseData,
    PlaylistCreatedSchemaMediaList,
    PlaylistByIDResponseMediaList,
]


@pytest.mark.parametrize("cls", DURATION_MODELS)
def test_duration_accepts_float(cls):
    assert cls.model_validate({"duration": 145.821315}).duration == 145.821315


@pytest.mark.parametrize("cls", DURATION_MODELS)
def test_duration_accepts_int(cls):
    assert cls.model_validate({"duration": 10}).duration == 10.0


@pytest.mark.parametrize("cls", DURATION_MODELS)
def test_duration_optional(cls):
    assert cls.model_validate({}).duration is None


@pytest.mark.parametrize("cls", DURATION_MODELS)
def test_duration_rejects_timestamp_string(cls):
    with pytest.raises(ValidationError, match="duration"):
        cls.model_validate({"duration": "00:02:25"})


def test_media_duration_serializes_numeric():
    dumped = Media.model_validate({"duration": 10.5}).model_dump(
        mode="json", by_alias=True, exclude_unset=True
    )
    assert dumped["duration"] == 10.5


# ---------------------------------------------------------------------------
# enableRecording on create live stream
# ---------------------------------------------------------------------------


def test_enable_recording_defaults_true():
    assert InputMediaSettings().enable_recording is True


def test_enable_recording_alias_round_trip():
    ims = InputMediaSettings.model_validate({"enableRecording": False})
    assert ims.enable_recording is False
    wire = json.loads(ims.model_dump_json(by_alias=True, exclude_none=True))
    assert wire["enableRecording"] is False


def test_create_live_stream_request_carries_enable_recording():
    req = CreateLiveStreamRequest.model_validate(
        {
            "playbackSettings": {"accessPolicy": "public"},
            "inputMediaSettings": {"metadata": {"k": "v"}, "enableRecording": False},
        }
    )
    wire = json.loads(req.model_dump_json(by_alias=True, exclude_none=True))
    assert wire["inputMediaSettings"]["enableRecording"] is False


# ---------------------------------------------------------------------------
# accessRestrictions on playback models
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("cls", [PlaybackIDRequest, PlaybackSettings, PlaybackIDResponse])
def test_access_restrictions_parse(cls):
    obj = cls.model_validate({"accessPolicy": "public", "accessRestrictions": RESTRICTIONS})
    ar = obj.access_restrictions
    assert ar.domains.default_policy == "deny"
    assert ar.domains.allow == ["example.com"]
    assert ar.user_agents.default_policy == "allow"
    assert ar.user_agents.deny == ["PostmanRuntime/7.29.0"]


@pytest.mark.parametrize("cls", [PlaybackIDRequest, PlaybackSettings])
def test_access_restrictions_serialize_wire_aliases(cls):
    obj = cls.model_validate({"accessPolicy": "public", "accessRestrictions": RESTRICTIONS})
    wire = json.loads(obj.model_dump_json(by_alias=True, exclude_none=True))
    assert wire["accessRestrictions"] == RESTRICTIONS


@pytest.mark.parametrize("cls", [PlaybackIDRequest, PlaybackSettings])
def test_access_restrictions_optional(cls):
    assert cls.model_validate({"accessPolicy": "public"}).access_restrictions is None


def test_playback_id_success_response_with_restrictions():
    resp = PlaybackIDSuccessResponse.model_validate(
        {
            "success": True,
            "data": {
                "id": "8863f89a-eb6c-4729-8d38-594c9dc25ade",
                "accessPolicy": "public",
                "accessRestrictions": RESTRICTIONS,
            },
        }
    )
    assert resp.data.access_restrictions.domains.allow == ["example.com"]


def test_playback_id_success_response_without_restrictions():
    resp = PlaybackIDSuccessResponse.model_validate(
        {"success": True, "data": {"id": "x", "accessPolicy": "public"}}
    )
    assert resp.data.access_restrictions is None


# ---------------------------------------------------------------------------
# live stream restriction endpoint models
# ---------------------------------------------------------------------------

LIVE_OPS = [
    (
        models.UpdateLiveStreamDomainRestrictionsRequest,
        models.UpdateLiveStreamDomainRestrictionsRequestBody,
        models.UpdateLiveStreamDomainRestrictionsResponseBody,
    ),
    (
        models.UpdateLiveStreamUserAgentRestrictionsRequest,
        models.UpdateLiveStreamUserAgentRestrictionsRequestBody,
        models.UpdateLiveStreamUserAgentRestrictionsResponseBody,
    ),
]


@pytest.mark.parametrize("request_cls,body_cls,response_cls", LIVE_OPS)
def test_live_restriction_request_body_serializes_flat(request_cls, body_cls, response_cls):
    body = body_cls(default_policy="deny", allow=["example.com"], deny=[])
    wire = body.model_dump(mode="json", by_alias=True)
    assert wire == {"defaultPolicy": "deny", "allow": ["example.com"], "deny": []}


@pytest.mark.parametrize("request_cls,body_cls,response_cls", LIVE_OPS)
def test_live_restriction_body_default_policy(request_cls, body_cls, response_cls):
    assert body_cls().default_policy == "allow"


@pytest.mark.parametrize("request_cls,body_cls,response_cls", LIVE_OPS)
def test_live_restriction_body_omits_unset_lists(request_cls, body_cls, response_cls):
    wire = body_cls(default_policy="allow").model_dump(mode="json", by_alias=True)
    assert wire == {"defaultPolicy": "allow"}


@pytest.mark.parametrize("request_cls,body_cls,response_cls", LIVE_OPS)
def test_live_restriction_request_uses_stream_id(request_cls, body_cls, response_cls):
    req = request_cls(stream_id="s1", playback_id="p1", body=body_cls())
    assert req.stream_id == "s1"
    assert req.playback_id == "p1"
    assert not hasattr(req, "media_id")


@pytest.mark.parametrize("request_cls,body_cls,response_cls", LIVE_OPS)
def test_live_restriction_response_parses(request_cls, body_cls, response_cls):
    resp = response_cls.model_validate(
        {
            "success": True,
            "data": {"defaultPolicy": "allow", "allow": ["yourdomain.com"], "deny": []},
        }
    )
    assert resp.success is True
    assert resp.data.allow == ["yourdomain.com"]


# ---------------------------------------------------------------------------
# SDK surface: methods exist with sync/async pairs
# ---------------------------------------------------------------------------


def test_sdk_methods_exist():
    from fastpix_python.live_playback import LivePlayback
    from fastpix_python.playback import Playback

    for name in (
        "update_live_stream_domain_restrictions",
        "update_live_stream_domain_restrictions_async",
        "update_live_stream_user_agent_restrictions",
        "update_live_stream_user_agent_restrictions_async",
    ):
        assert hasattr(LivePlayback, name), name
    for name in ("update_domain_restrictions_async", "update_user_agent_restrictions_async"):
        assert hasattr(Playback, name), name
