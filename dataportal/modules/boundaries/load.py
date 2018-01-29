from django.contrib.gis.utils import LayerMapping


def run(model, shp, mapping, verbose=True):
    lm = LayerMapping(
        model, shp, mapping,
        transform=False, encoding='utf-8',
    )
    lm.save(strict=True, verbose=verbose)
