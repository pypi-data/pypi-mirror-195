#!/bin/env python3

import json
import requests

from .UnofficialTypes import SearchAddressResult, RhServices


class VafabUnafficial:
    @staticmethod
    def get_address_identifier(address: str) -> SearchAddressResult:
        response = requests.post(
            "https://services.vafabmiljo.se/FutureWebVKFHus/SimpleWastePickup/SearchAdress",
            data=json.dumps({"searchText": address}),
            headers={'Content-type': 'application/json', 'Accept': 'text/plain'}
        )
        return SearchAddressResult.from_dict(response.json())

    @staticmethod
    def get_service_info(address: str) -> RhServices:
        r = requests.get(
            'https://services.vafabmiljo.se/FutureWebVKFHus/SimpleWastePickup/GetWastePickupSchedule',
            params={'address': address}
        )
        return RhServices.from_dict(r.json())