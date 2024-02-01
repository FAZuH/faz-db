from typing import Any, Callable

import vcr as vcrpy

def _remove_sensitive_data() -> Callable[..., dict[str, Any]]:
    def before_record_response(response: Any) -> dict[str, Any]:
        for header in dict(response["headers"]):
            if header.lower() not in ("cache-control", "date", "expires", "ratelimit-limit", "ratelimit-remaining", "ratelimit-reset"):
                del response["headers"][header]
        return response
    return before_record_response

vcr = vcrpy.VCR(
    before_record_response=_remove_sensitive_data(),
    cassette_library_dir="tests/vcr_cassettes",
    path_transformer=vcrpy.VCR.ensure_suffix(".yaml"),
    record_mode=vcrpy.record_mode.RecordMode.NEW_EPISODES
)
