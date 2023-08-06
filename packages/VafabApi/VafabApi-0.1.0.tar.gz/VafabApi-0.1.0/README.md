# VafabApi
A small api wrapper to handle the complexity of getting the json and converting it to a typed object.

## Warning
Currently this uses a backward engineered API and could therefore break at any moment.

## Installation
```
pip install VafabApi
```

## Get started
How to use:

```Python
# At this point VafabMiljö does not have an official API.
from VafabApi import VafabUnafficial as Vafab

# Call with address
address = "..."
addr_id = Vafab.get_address_identifier(address).buildings[0]
print(addr_id)  # Prints the address id
addr_services = Vafab.get_service_info(addr_id)
print(addr_services)  # Prints the object containing all fetched services
```