import json, os, sys, traceback

def to_jsonable(x):
    if hasattr(x, "model_dump"):
        try:
            return x.model_dump(by_alias=True)
        except Exception:
            pass
    if hasattr(x, "dict"):
        try:
            return x.dict()
        except Exception:
            pass
    return x

def headers_to_obj(h):
    try:
        return dict(h)
    except Exception:
        pass
    try:
        return dict(h.items())
    except Exception:
        return None

def normalize_err(e):
    out = {
        "name": e.__class__.__name__,
        "message": str(e),
        "stack": traceback.format_exc(),
    }
    status_code = getattr(e, "status_code", None)
    if status_code is not None:
        out["statusCode"] = status_code
    body = getattr(e, "body", None)
    if body is not None:
        out["body"] = body
        if isinstance(body, str):
            try:
                out["bodyJson"] = json.loads(body)
            except Exception:
                pass
    raw = getattr(e, "raw_response", None)
    if raw is not None:
        try:
            out["contentType"] = raw.headers.get("content-type")
        except Exception:
            pass
        try:
            out["headers"] = headers_to_obj(raw.headers)
        except Exception:
            pass
        try:
            out["url"] = str(raw.url)
        except Exception:
            pass
    if getattr(e, "__cause__", None) is not None:
        out["cause"] = str(getattr(e, "__cause__"))
    return out

payload = json.load(sys.stdin)
op = payload.get("operationId")
req = payload.get("request") or {}
base_url = payload.get("baseUrl")
username = payload.get("username")
password = payload.get("password")

try:
    from fastpix_python import Fastpix, models
except Exception as e:
    print(json.dumps({"ok": False, "error": {"name": "PythonImportError", "message": str(e), "stack": traceback.format_exc()}}))
    sys.exit(0)

sdk = Fastpix(security=models.Security(username=username, password=password), server_url=base_url)

def g(k): return req.get(k)

try:
    if op == "list-media":
        res = sdk.manage_videos.list_media(limit=g("limit"), offset=g("offset"), order_by=g("orderBy"))
    elif op == "get-media":
        res = sdk.media.get(media_id=g("mediaId"))
    elif op == "get-media-summary":
        res = sdk.manage_videos.get_summary(media_id=g("mediaId"))
    elif op == "retrieveMediaInputInfo":
        res = sdk.media.get_input_info(media_id=g("mediaId"))
    elif op == "list-uploads":
        res = sdk.manage_videos.list_unused_upload_urls(limit=g("limit"), offset=g("offset"), order_by=g("orderBy"))
    elif op == "get-media-clips":
        res = sdk.manage_videos.get_clips(media_id=g("mediaId"))
    elif op == "list-live-clips":
        res = sdk.media.list_live_clips(livestream_id=g("livestreamId"))
    elif op == "get-all-playlists":
        res = sdk.playlists.get_all(limit=g("limit"), offset=g("offset"))
    elif op == "get-playlist-by-id":
        res = sdk.playlist.get(playlist_id=g("playlistId"))
    elif op == "list-playback-ids":
        res = sdk.playback.list_playback_ids(media_id=g("mediaId"))
    elif op == "get-playback-id":
        res = sdk.playback.get_by_id(media_id=g("mediaId"), playback_id=g("playbackId"))
    elif op == "getDrmConfiguration":
        res = sdk.drm_configurations.get(limit=g("limit"), offset=g("offset"))
    elif op == "getDrmConfigurationById":
        res = sdk.drm_configurations.get_by_id(drm_configuration_id=g("drmConfigurationId"))
    elif op == "get-all-streams":
        res = sdk.live_streams.list(limit=g("limit"), offset=g("offset"), order_by=g("orderBy"))
    elif op == "get-live-stream-by-id":
        res = sdk.manage_live_stream.get(stream_id=g("streamId"))
    elif op == "get-live-stream-viewer-count-by-id":
        res = sdk.manage_live_stream.get_viewer_count(stream_id=g("streamId"))
    elif op == "get-live-stream-playback-id":
        res = sdk.live_playback.get_playback_id_details(stream_id=g("streamId"), playback_id=g("playbackId"))
    elif op == "get-specific-simulcast-of-stream":
        res = sdk.simulcast_stream.get_simulcast(stream_id=g("streamId"), simulcast_id=g("simulcastId"))
    elif op == "list_signing_keys":
        res = sdk.signing_keys.list_signing_keys(limit=g("limit"), offset=g("offset"))
    elif op == "get-signing_key_by_id":
        res = sdk.signing_keys.get_signing_key_by_id(signing_key_id=g("signingKeyId"))
    elif op == "list_video_views":
        res = sdk.views.list_video_views(timespan=g("timespan"), limit=g("limit"), offset=g("offset"))
    elif op == "get_video_view_details":
        res = sdk.views.get_video_view_details(view_id=g("viewId"))
    elif op == "list_by_top_content":
        res = sdk.views.list_by_top_content(timespan=g("timespan"), limit=g("limit"))
    elif op == "list_dimensions":
        res = sdk.dimensions.list()
    elif op == "list_filter_values_for_dimension":
        res = sdk.dimensions.list_filter_values(dimensions_id=g("dimensionsId"))
    elif op == "list_breakdown_values":
        res = sdk.metrics.list_breakdown_values(metric_id=g("metricId"), timespan=g("timespan"), group_by=g("groupBy"))
    elif op == "list_overall_values":
        res = sdk.metrics.list_overall_values(metric_id=g("metricId"), timespan=g("timespan"))
    elif op == "get_timeseries_data":
        res = sdk.metrics.get_timeseries_data(metric_id=g("metricId"), timespan=g("timespan"), group_by=g("groupBy"))
    elif op == "list_comparison_values":
        res = sdk.metrics.list_comparison_values(timespan=g("timespan"), dimension=g("dimension"), value=g("value"))
    elif op == "list_errors":
        res = sdk.errors.list(timespan=g("timespan"), limit=g("limit"))
    else:
        print(json.dumps({"ok": False, "error": {"name": "SDKMappingError", "message": "No Python SDK method mapping for this operationId"}}))
        sys.exit(0)

    print(json.dumps({"ok": True, "value": to_jsonable(res)}, default=str))
except Exception as e:
    print(json.dumps({"ok": False, "error": normalize_err(e)}, default=str))
