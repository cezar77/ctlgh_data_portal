import json

from dataportal.modules.boundaries.models import SecondAdministrativeLevel
from dataportal.modules.chickens.models import Farm

farms = Farm.objects.all()

locations = []
for farm in farms:
    locations.append(
        SecondAdministrativeLevel.objects.get(
            geom__contains=farm.geolocation
        )
    )

result = []
pk = 13
for i, l in enumerate(locations):
    item = {}
    item["model"] = "boundaries.administrativerouter"
    pk += 1
    item["pk"] = pk
    item["fields"] = {}
    item["fields"]["sampling_content_type"] = ["chickens", "farm"]
    item["fields"]["sampling_object_id"] = i+1
    item["fields"]["adm_content_type"] = ["boundaries", "secondadministrativelevel"]
    item["fields"]["adm_object_id"] = l.pk
    result.append(item)

with open('output.json', 'w') as output:
    output.write(json.dumps(result, indent=4))
