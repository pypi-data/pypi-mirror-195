from typing import List, Tuple
from functools import partial
from purolator_lib.tracking_service_1_2_2 import (
    TrackPackagesByPinRequest,
    PIN,
    ArrayOfPIN,
    RequestContext,
    TrackingInformation,
    Depot,
)
from karrio.core.models import (
    TrackingRequest,
    TrackingDetails,
    Message,
    TrackingEvent,
)
from karrio.core.utils import Element, DF, XP
from karrio.core.utils.soap import create_envelope
from pysoap.envelope import Envelope
from karrio.core.utils.serializable import Serializable
from karrio.providers.purolator.utils import Settings, standard_request_serializer
from karrio.providers.purolator.error import parse_error_response


def parse_tracking_response(
    response: Element, settings: Settings
) -> Tuple[List[TrackingDetails], List[Message]]:
    track_infos = response.xpath(
        ".//*[local-name() = $name]", name="TrackingInformation"
    )
    return (
        [_extract_tracking(node, settings) for node in track_infos],
        parse_error_response(response, settings),
    )


def _extract_tracking(node: Element, settings: Settings) -> TrackingDetails:
    track = XP.to_object(TrackingInformation, node)

    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=str(track.PIN.Value),
        events=[
            TrackingEvent(
                date=DF.fdate(scan.ScanDate),
                time=DF.ftime(scan.ScanTime, "%H%M%S"),
                description=scan.Description,
                location=scan.Depot.Name,
                code=scan.ScanType,
            )
            for scan in track.Scans.Scan
        ],
        delivered=any(scan.ScanType == "Delivery" for scan in track.Scans.Scan),
    )


def tracking_request(
    payload: TrackingRequest, settings: Settings
) -> Serializable[Envelope]:
    request = create_envelope(
        header_content=RequestContext(
            Version="1.2",
            Language=settings.language,
            GroupID="",
            RequestReference="",
            UserToken=settings.user_token,
        ),
        body_content=TrackPackagesByPinRequest(
            PINs=ArrayOfPIN(PIN=[PIN(Value=pin) for pin in payload.tracking_numbers])
        ),
    )

    return Serializable(request, partial(standard_request_serializer, version="v1"))
