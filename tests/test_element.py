import pytest

from OSMPythonTools.element import Element
from OSMPythonTools.nominatim import NominatimResult

@pytest.mark.parametrize(('type', 'id'), [('node', 42467507), ('way', 731168237), ('relation', 175905)])
def test_elementCreate(type, id):
  ns = []
  ns.append(Element.fromId(type + '/' + str(id)))
  ns.append(Element.fromId(type + ' / ' + str(id)))
  ns.append(Element.fromId(type[0] + '/' + str(id)))
  ns.append(Element.fromId(type[0] + ' / ' + str(id)))
  ns.append(Element.fromId(type + '  ' + str(id)))
  ns.append(Element.fromId(type + ' ' + str(id)))
  ns.append(Element.fromId(type + str(id)))
  ns.append(Element.fromId(type[0] + ' ' + str(id)))
  ns.append(Element.fromId(type[0] + str(id)))
  ns.append(Element.fromId(ns[0]))
  ns.append(Element.fromId(NominatimResult([{'osm_type': type, 'osm_id': id}], '', None)))
  for n in ns:
    assert ns[0].type() == n.type()
    assert ns[0].id() == n.id()
    assert ns[0].typeId() == n.typeId()
    assert ns[0].typeIdShort() == n.typeIdShort()
    assert ns[0].areaId() == n.areaId()
