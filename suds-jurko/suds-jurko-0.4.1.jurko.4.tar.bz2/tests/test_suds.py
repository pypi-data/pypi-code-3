# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the (LGPL) GNU Lesser General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library Lesser General Public License for more details at
# ( http://www.gnu.org/licenses/lgpl.html ).
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# written by: Jurko Gospodnetić ( jurko.gospodnetic@pke.hr )

"""
General suds Python library unit tests.

Implemented using the 'pytest' testing framework.

This whole module should be refactored into more specialized modules as more
tests get added to it and it acquires more structure.

"""

if __name__ == "__main__":
    try:
        import pytest
        pytest.main(["--pyargs", __file__])
    except ImportError:
        print("'py.test' unit testing framework not available. Can not run "
            "'{}' directly as a script.".format(__file__))
    import sys
    sys.exit(-2)


import os
import re

import pytest

import suds.client
import suds.store
import xml.sax


def test_converting_client_to_string_must_not_raise_an_exception():
    client = _client_from_wsdl(
        "<?xml version='1.0' encoding='UTF-8'?><root />")
    str(client)


def test_converting_metadata_to_string():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:complexType name="AAA">
        <xsd:sequence>
          <xsd:element name="u1" type="xsd:string" />
          <xsd:element name="u2" type="xsd:string" />
          <xsd:element name="u3" type="xsd:string" />
        </xsd:sequence>
      </xsd:complexType>
    </xsd:schema>
  </wsdl:types>
  <wsdl:portType name="dummyPortType">
  </wsdl:portType>
  <wsdl:binding name="dummy" type="ns:dummyPortType">
    <soap:binding style="document"
    transport="http://schemas.xmlsoap.org/soap/http" />
  </wsdl:binding>
  <wsdl:service name="dummy">
    <wsdl:port name="dummy" binding="ns:dummy">
      <soap:address location="https://localhost/dummy" />
    </wsdl:port>
  </wsdl:service>
</wsdl:definitions>
""")
    # Metadata with empty content.
    metadata = client.wsdl.__metadata__
    assert len(metadata) == 0
    assert "<empty>" == str(metadata)

    # Metadata with non-empty content.
    metadata = client.factory.create("AAA").__metadata__
    assert len(metadata) == 2
    metadata_string = str(metadata)
    assert re.search(" sxtype = ", metadata_string)
    assert re.search(" ordering\[\] = ", metadata_string)


def test_empty_invalid_wsdl():
    try:
        client = _client_from_wsdl("")
        pytest.fail("Excepted exception xml.sax.SAXParseException not thrown.")
    except xml.sax.SAXParseException, e:
        assert e.getMessage() == "no element found"


def test_empty_valid_wsdl():
    client = _client_from_wsdl(
        "<?xml version='1.0' encoding='UTF-8'?><root />")
    assert not client.wsdl.services, "No service definitions must be read "  \
        "from an empty WSDL."


def test_enumeration_type_string_should_contain_its_value():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:simpleType name="AAA">
        <xsd:restriction base="xsd:string">
          <xsd:enumeration value="One" />
          <xsd:enumeration value="Two" />
          <xsd:enumeration value="Thirty-Two" />
        </xsd:restriction>
      </xsd:simpleType>
    </xsd:schema>
  </wsdl:types>
  <wsdl:portType name="dummyPortType">
  </wsdl:portType>
  <wsdl:binding name="dummy" type="ns:dummyPortType">
    <soap:binding style="document"
    transport="http://schemas.xmlsoap.org/soap/http" />
  </wsdl:binding>
  <wsdl:service name="dummy">
    <wsdl:port name="dummy" binding="ns:dummy">
      <soap:address location="https://localhost/dummy" />
    </wsdl:port>
  </wsdl:service>
</wsdl:definitions>
""")
    enumeration_data = client.wsdl.schema.types["AAA", "my-namespace"]
    # Legend:
    #   eX - enumeration element.
    #   aX - ancestry for the enumeration element.
    (e1, a1), (e2, a2), (e3, a3) = enumeration_data
    assert isinstance(e1, suds.xsd.sxbasic.Enumeration)
    assert isinstance(e2, suds.xsd.sxbasic.Enumeration)
    assert isinstance(e3, suds.xsd.sxbasic.Enumeration)
    assert e1.name == "One"
    assert e2.name == "Two"
    assert e3.name == "Thirty-Two"
    assert re.match('<Enumeration:0x[0-9a-f]+ name="One" />$', e1.str())
    assert re.match('<Enumeration:0x[0-9a-f]+ name="Two" />$', e2.str())
    assert re.match('<Enumeration:0x[0-9a-f]+ name="Thirty-Two" />$', e3.str())


def test_function_parameters_global_sequence_in_a_sequence():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:complexType name="UngaBunga">
        <xsd:sequence>
          <xsd:element name="u1" type="xsd:string" />
          <xsd:element name="u2" type="xsd:string" />
          <xsd:element name="u3" type="xsd:string" />
        </xsd:sequence>
      </xsd:complexType>
      <xsd:element name="Elemento">
        <xsd:complexType>
          <xsd:sequence>
            <xsd:element name="x1" type="xsd:string" />
            <xsd:element name="x2" type="UngaBunga" />
            <xsd:element name="x3" type="xsd:string" />
          </xsd:sequence>
        </xsd:complexType>
      </xsd:element>
    </xsd:schema>
  </wsdl:types>
  <wsdl:message name="fRequestMessage">
    <wsdl:part name="parameters" element="ns:Elemento" />
  </wsdl:message>
  <wsdl:portType name="dummyPortType">
    <wsdl:operation name="f">
      <wsdl:input message="ns:fRequestMessage" />
    </wsdl:operation>
  </wsdl:portType>
  <wsdl:binding name="dummy" type="ns:dummyPortType">
    <soap:binding style="document"
    transport="http://schemas.xmlsoap.org/soap/http" />
    <wsdl:operation name="f">
      <soap:operation soapAction="f" style="document" />
      <wsdl:input><soap:body use="literal" /></wsdl:input>
      <wsdl:output><soap:body use="literal" /></wsdl:output>
    </wsdl:operation>
  </wsdl:binding>
  <wsdl:service name="dummy">
    <wsdl:port name="dummy" binding="ns:dummy">
      <soap:address location="https://localhost/dummy" />
    </wsdl:port>
  </wsdl:service>
</wsdl:definitions>
""")

    service = client.sd[0]
    assert len(service.types) == 1

    # Method parameters as read from the service definition.
    assert len(service.params) == 3
    assert service.params[0][0].name == "x1"
    assert service.params[0][0].type[0] == "string"
    assert service.params[0][0].type[1] == "http://www.w3.org/2001/XMLSchema"
    assert isinstance(service.params[0][1], suds.xsd.sxbuiltin.XString)
    assert service.params[1][0].name == "x2"
    assert service.params[1][0].type[0] == "UngaBunga"
    assert service.params[1][0].type[1] == "my-namespace"
    assert isinstance(service.params[1][1], suds.xsd.sxbasic.Complex)
    assert service.params[2][0].name == "x3"
    assert service.params[2][0].type[0] == "string"
    assert service.params[2][0].type[1] == "http://www.w3.org/2001/XMLSchema"
    assert isinstance(service.params[2][1], suds.xsd.sxbuiltin.XString)

    # Method parameters as read from a method object.
    assert len(service.ports) == 1
    port, methods = service.ports[0]
    assert len(methods) == 1
    method = methods[0]
    assert len(method) == 2
    method_name = method[0]
    assert method_name == "f"
    method_params = method[1]
    assert len(method_params) == 3
    assert method_params[0][0] == "x1"
    assert method_params[0][1] is service.params[0][0]
    assert method_params[1][0] == "x2"
    assert method_params[1][1] is service.params[1][0]
    assert method_params[2][0] == "x3"
    assert method_params[2][1] is service.params[2][0]


def test_function_parameters_local_choice():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:element name="Elemento">
        <xsd:complexType>
          <xsd:choice>
            <xsd:element name="u1" type="xsd:string" />
            <xsd:element name="u2" type="xsd:string" />
          </xsd:choice>
        </xsd:complexType>
      </xsd:element>
    </xsd:schema>
  </wsdl:types>
  <wsdl:message name="fRequestMessage">
    <wsdl:part name="parameters" element="ns:Elemento" />
  </wsdl:message>
  <wsdl:portType name="dummyPortType">
    <wsdl:operation name="f">
      <wsdl:input message="ns:fRequestMessage" />
    </wsdl:operation>
  </wsdl:portType>
  <wsdl:binding name="dummy" type="ns:dummyPortType">
    <soap:binding style="document"
    transport="http://schemas.xmlsoap.org/soap/http" />
    <wsdl:operation name="f">
      <soap:operation soapAction="f" style="document" />
      <wsdl:input><soap:body use="literal" /></wsdl:input>
      <wsdl:output><soap:body use="literal" /></wsdl:output>
    </wsdl:operation>
  </wsdl:binding>
  <wsdl:service name="dummy">
    <wsdl:port name="dummy" binding="ns:dummy">
      <soap:address location="https://localhost/dummy" />
    </wsdl:port>
  </wsdl:service>
</wsdl:definitions>
""")

    service = client.sd[0]
    assert not service.types

    # Method parameters as read from the service definition.
    assert len(service.params) == 2
    assert service.params[0][0].name == "u1"
    assert service.params[0][0].type[0] == "string"
    assert service.params[0][0].type[1] == "http://www.w3.org/2001/XMLSchema"
    assert isinstance(service.params[0][1], suds.xsd.sxbuiltin.XString)
    assert service.params[1][0].name == "u2"
    assert service.params[1][0].type[0] == "string"
    assert service.params[1][0].type[1] == "http://www.w3.org/2001/XMLSchema"
    assert isinstance(service.params[1][1], suds.xsd.sxbuiltin.XString)

    # Method parameters as read from a method object.
    assert len(service.ports) == 1
    port, methods = service.ports[0]
    assert len(methods) == 1
    assert len(methods[0]) == 2
    method_name, method_params = methods[0]
    assert method_name == "f"
    assert len(method_params) == 2
    assert method_params[0][0] == "u1"
    assert method_params[0][1] is service.params[0][0]
    assert method_params[1][0] == "u2"
    assert method_params[1][1] is service.params[1][0]

    # Construct method parameter element object.
    paramOut = client.factory.create("Elemento")
    _assert_dynamic_type(paramOut, "Elemento")
    assert not paramOut.__keylist__


def test_function_parameters_local_choice_in_a_sequence():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:element name="Elemento">
        <xsd:complexType>
          <xsd:sequence>
            <xsd:element name="x1" type="xsd:string" />
            <xsd:element name="x2">
              <xsd:complexType>
                <xsd:choice>
                  <xsd:element name="u1" type="xsd:string" />
                  <xsd:element name="u2" type="xsd:string" />
                  <xsd:element name="u3" type="xsd:string" />
                </xsd:choice>
              </xsd:complexType>
            </xsd:element>
            <xsd:element name="x3" type="xsd:string" />
          </xsd:sequence>
        </xsd:complexType>
      </xsd:element>
    </xsd:schema>
  </wsdl:types>
  <wsdl:message name="fRequestMessage">
    <wsdl:part name="parameters" element="ns:Elemento" />
  </wsdl:message>
  <wsdl:portType name="dummyPortType">
    <wsdl:operation name="f">
      <wsdl:input message="ns:fRequestMessage" />
    </wsdl:operation>
  </wsdl:portType>
  <wsdl:binding name="dummy" type="ns:dummyPortType">
    <soap:binding style="document"
    transport="http://schemas.xmlsoap.org/soap/http" />
    <wsdl:operation name="f">
      <soap:operation soapAction="f" style="document" />
      <wsdl:input><soap:body use="literal" /></wsdl:input>
      <wsdl:output><soap:body use="literal" /></wsdl:output>
    </wsdl:operation>
  </wsdl:binding>
  <wsdl:service name="dummy">
    <wsdl:port name="dummy" binding="ns:dummy">
      <soap:address location="https://localhost/dummy" />
    </wsdl:port>
  </wsdl:service>
</wsdl:definitions>
""")

    service = client.sd[0]
    assert not service.types

    # Method parameters as read from the service definition.
    assert len(service.params) == 3
    assert service.params[0][0].name == "x1"
    assert service.params[0][0].type[0] == "string"
    assert service.params[0][0].type[1] == "http://www.w3.org/2001/XMLSchema"
    assert isinstance(service.params[0][1], suds.xsd.sxbuiltin.XString)
    assert service.params[1][0].name == "x2"
    assert service.params[1][0].type is None
    assert isinstance(service.params[1][1], suds.xsd.sxbasic.Element)
    assert service.params[2][0].name == "x3"
    assert service.params[2][0].type[0] == "string"
    assert service.params[2][0].type[1] == "http://www.w3.org/2001/XMLSchema"
    assert isinstance(service.params[2][1], suds.xsd.sxbuiltin.XString)

    # Method parameters as read from a method object.
    assert len(service.ports) == 1
    port, methods = service.ports[0]
    assert len(methods) == 1
    method = methods[0]
    assert len(method) == 2
    method_name = method[0]
    assert method_name == "f"
    method_params = method[1]
    assert len(method_params) == 3
    assert method_params[0][0] == "x1"
    assert method_params[0][1] is service.params[0][0]
    assert method_params[1][0] == "x2"
    assert method_params[1][1] is service.params[1][0]
    assert method_params[2][0] == "x3"
    assert method_params[2][1] is service.params[2][0]

    # Construct method parameter element object.
    paramOut = client.factory.create("Elemento")
    _assert_dynamic_type(paramOut, "Elemento")
    assert paramOut.x1 is None
    _assert_dynamic_type(paramOut.x2, "x2")
    assert not paramOut.x2.__keylist__
    assert paramOut.x3 is None

    # Construct method parameter objects with a locally defined type.
    paramIn = client.factory.create("Elemento.x2")
    _assert_dynamic_type(paramIn, "x2")
    assert not paramOut.x2.__keylist__
    assert paramIn is not paramOut.x2


def test_function_parameters_local_sequence_in_a_sequence():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:element name="Elemento">
        <xsd:complexType>
          <xsd:sequence>
            <xsd:element name="x1" type="xsd:string" />
            <xsd:element name="x2">
              <xsd:complexType>
                <xsd:sequence>
                  <xsd:element name="u1" type="xsd:string" />
                  <xsd:element name="u2" type="xsd:string" />
                  <xsd:element name="u3" type="xsd:string" />
                </xsd:sequence>
              </xsd:complexType>
            </xsd:element>
            <xsd:element name="x3" type="xsd:string" />
          </xsd:sequence>
        </xsd:complexType>
      </xsd:element>
    </xsd:schema>
  </wsdl:types>
  <wsdl:message name="fRequestMessage">
    <wsdl:part name="parameters" element="ns:Elemento" />
  </wsdl:message>
  <wsdl:portType name="dummyPortType">
    <wsdl:operation name="f">
      <wsdl:input message="ns:fRequestMessage" />
    </wsdl:operation>
  </wsdl:portType>
  <wsdl:binding name="dummy" type="ns:dummyPortType">
    <soap:binding style="document"
    transport="http://schemas.xmlsoap.org/soap/http" />
    <wsdl:operation name="f">
      <soap:operation soapAction="f" style="document" />
      <wsdl:input><soap:body use="literal" /></wsdl:input>
      <wsdl:output><soap:body use="literal" /></wsdl:output>
    </wsdl:operation>
  </wsdl:binding>
  <wsdl:service name="dummy">
    <wsdl:port name="dummy" binding="ns:dummy">
      <soap:address location="https://localhost/dummy" />
    </wsdl:port>
  </wsdl:service>
</wsdl:definitions>
""")

    service = client.sd[0]
    assert not service.types

    # Method parameters as read from the service definition.
    assert len(service.params) == 3
    assert service.params[0][0].name == "x1"
    assert service.params[0][0].type[0] == "string"
    assert service.params[0][0].type[1] == "http://www.w3.org/2001/XMLSchema"
    assert isinstance(service.params[0][1], suds.xsd.sxbuiltin.XString)
    assert service.params[1][0].name == "x2"
    assert service.params[1][0].type is None
    assert isinstance(service.params[1][1], suds.xsd.sxbasic.Element)
    assert service.params[2][0].name == "x3"
    assert service.params[2][0].type[0] == "string"
    assert service.params[2][0].type[1] == "http://www.w3.org/2001/XMLSchema"
    assert isinstance(service.params[2][1], suds.xsd.sxbuiltin.XString)

    # Method parameters as read from a method object.
    assert len(service.ports) == 1
    port, methods = service.ports[0]
    assert len(methods) == 1
    method = methods[0]
    assert len(method) == 2
    method_name = method[0]
    assert method_name == "f"
    method_params = method[1]
    assert len(method_params) == 3
    assert method_params[0][0] == "x1"
    assert method_params[0][1] is service.params[0][0]
    assert method_params[1][0] == "x2"
    assert method_params[1][1] is service.params[1][0]
    assert method_params[2][0] == "x3"
    assert method_params[2][1] is service.params[2][0]

    # Construct method parameter element object.
    paramOut = client.factory.create("Elemento")
    _assert_dynamic_type(paramOut, "Elemento")
    assert paramOut.x1 is None
    _assert_dynamic_type(paramOut.x2, "x2")
    assert paramOut.x2.u1 is None
    assert paramOut.x2.u2 is None
    assert paramOut.x2.u3 is None
    assert paramOut.x3 is None

    # Construct method parameter objects with a locally defined type.
    paramIn = client.factory.create("Elemento.x2")
    _assert_dynamic_type(paramIn, "x2")
    assert paramIn.u1 is None
    assert paramIn.u2 is None
    assert paramIn.u3 is None
    assert paramIn is not paramOut.x2


def test_function_parameters_sequence_in_a_choice():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:element name="Choice">
        <xsd:complexType>
          <xsd:choice>
            <xsd:element name="a1" type="xsd:string" />
            <xsd:element name="sequence">
              <xsd:complexType>
                <xsd:sequence>
                  <xsd:element name="e1" type="xsd:string" />
                  <xsd:element name="e2" type="xsd:string" />
                  <xsd:element name="e3" type="xsd:string" />
                </xsd:sequence>
              </xsd:complexType>
            </xsd:element>
            <xsd:element name="a2" type="xsd:string" />
          </xsd:choice>
        </xsd:complexType>
      </xsd:element>
    </xsd:schema>
  </wsdl:types>
  <wsdl:message name="fRequestMessage">
    <wsdl:part name="parameters" element="ns:Choice" />
  </wsdl:message>
  <wsdl:portType name="dummyPortType">
    <wsdl:operation name="f">
      <wsdl:input message="ns:fRequestMessage" />
    </wsdl:operation>
  </wsdl:portType>
  <wsdl:binding name="dummy" type="ns:dummyPortType">
    <soap:binding style="document"
    transport="http://schemas.xmlsoap.org/soap/http" />
    <wsdl:operation name="f">
      <soap:operation soapAction="f" style="document" />
      <wsdl:input><soap:body use="literal" /></wsdl:input>
      <wsdl:output><soap:body use="literal" /></wsdl:output>
    </wsdl:operation>
  </wsdl:binding>
  <wsdl:service name="dummy">
    <wsdl:port name="dummy" binding="ns:dummy">
      <soap:address location="https://localhost/dummy" />
    </wsdl:port>
  </wsdl:service>
</wsdl:definitions>
""")

    # Input #1.
    request = _construct_SOAP_request(client, 'f', a1="Wackadoodle")
    assert request.str() == """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:ns0="my-namespace" xmlns:ns1="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
   <SOAP-ENV:Header/>
   <ns1:Body>
      <ns0:Choice>
         <ns0:a1>Wackadoodle</ns0:a1>
      </ns0:Choice>
   </ns1:Body>
</SOAP-ENV:Envelope>"""

    # Input #2.
    param = client.factory.create("Choice.sequence")
    param.e2 = "Wackadoodle"
    request = _construct_SOAP_request(client, 'f', sequence=param)
    assert request.str() == """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:ns0="my-namespace" xmlns:ns1="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
   <SOAP-ENV:Header/>
   <ns1:Body>
      <ns0:Choice>
         <ns0:sequence>
            <ns0:e1/>
            <ns0:e2>Wackadoodle</ns0:e2>
            <ns0:e3/>
         </ns0:sequence>
      </ns0:Choice>
   </ns1:Body>
</SOAP-ENV:Envelope>"""


def test_function_parameters_sequence_in_a_choice_in_a_sequence():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:element name="External">
        <xsd:complexType>
          <xsd:sequence>
            <xsd:element name="choice">
              <xsd:complexType>
                <xsd:choice>
                  <xsd:element name="a1" type="xsd:string" />
                  <xsd:element name="sequence">
                    <xsd:complexType>
                      <xsd:sequence>
                        <xsd:element name="e1" type="xsd:string" />
                        <xsd:element name="e2" type="xsd:string" />
                        <xsd:element name="e3" type="xsd:string" />
                      </xsd:sequence>
                    </xsd:complexType>
                  </xsd:element>
                  <xsd:element name="a2" type="xsd:string" />
                </xsd:choice>
              </xsd:complexType>
            </xsd:element>
          </xsd:sequence>
        </xsd:complexType>
      </xsd:element>
    </xsd:schema>
  </wsdl:types>
  <wsdl:message name="fRequestMessage">
    <wsdl:part name="parameters" element="ns:External" />
  </wsdl:message>
  <wsdl:portType name="dummyPortType">
    <wsdl:operation name="f">
      <wsdl:input message="ns:fRequestMessage" />
    </wsdl:operation>
  </wsdl:portType>
  <wsdl:binding name="dummy" type="ns:dummyPortType">
    <soap:binding style="document"
    transport="http://schemas.xmlsoap.org/soap/http" />
    <wsdl:operation name="f">
      <soap:operation soapAction="f" style="document" />
      <wsdl:input><soap:body use="literal" /></wsdl:input>
      <wsdl:output><soap:body use="literal" /></wsdl:output>
    </wsdl:operation>
  </wsdl:binding>
  <wsdl:service name="dummy">
    <wsdl:port name="dummy" binding="ns:dummy">
      <soap:address location="https://localhost/dummy" />
    </wsdl:port>
  </wsdl:service>
</wsdl:definitions>
""")

    # Construct input parameters.
    param = client.factory.create("External.choice")
    param.sequence = client.factory.create("External.choice.sequence")
    param.sequence.e2 = "Wackadoodle"

    # Construct a SOAP request containing our input parameters.
    request = _construct_SOAP_request(client, 'f', param)
    assert request.str() == """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:ns0="my-namespace" xmlns:ns1="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
   <SOAP-ENV:Header/>
   <ns1:Body>
      <ns0:External>
         <ns0:choice>
            <ns0:sequence>
               <ns0:e1/>
               <ns0:e2>Wackadoodle</ns0:e2>
               <ns0:e3/>
            </ns0:sequence>
         </ns0:choice>
      </ns0:External>
   </ns1:Body>
</SOAP-ENV:Envelope>"""


def test_function_parameters_strings():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:element name="Elemento">
        <xsd:complexType>
          <xsd:sequence>
            <xsd:element name="x1" type="xsd:string" />
            <xsd:element name="x2" type="xsd:string" />
            <xsd:element name="x3" type="xsd:string" />
          </xsd:sequence>
        </xsd:complexType>
      </xsd:element>
    </xsd:schema>
  </wsdl:types>
  <wsdl:message name="fRequestMessage">
    <wsdl:part name="parameters" element="ns:Elemento" />
  </wsdl:message>
  <wsdl:portType name="dummyPortType">
    <wsdl:operation name="f">
      <wsdl:input message="ns:fRequestMessage" />
    </wsdl:operation>
  </wsdl:portType>
  <wsdl:binding name="dummy" type="ns:dummyPortType">
    <soap:binding style="document"
    transport="http://schemas.xmlsoap.org/soap/http" />
    <wsdl:operation name="f">
      <soap:operation soapAction="f" style="document" />
      <wsdl:input><soap:body use="literal" /></wsdl:input>
      <wsdl:output><soap:body use="literal" /></wsdl:output>
    </wsdl:operation>
  </wsdl:binding>
  <wsdl:service name="dummy">
    <wsdl:port name="dummy" binding="ns:dummy">
      <soap:address location="https://localhost/dummy" />
    </wsdl:port>
  </wsdl:service>
</wsdl:definitions>
""")

    service = client.sd[0]
    assert not service.types

    # Method parameters as read from the service definition.
    assert len(service.params) == 3
    assert service.params[0][0].name == "x1"
    assert service.params[0][0].type[0] == "string"
    assert service.params[0][0].type[1] == "http://www.w3.org/2001/XMLSchema"
    assert isinstance(service.params[0][1], suds.xsd.sxbuiltin.XString)
    assert service.params[1][0].name == "x2"
    assert service.params[1][0].type[0] == "string"
    assert service.params[1][0].type[1] == "http://www.w3.org/2001/XMLSchema"
    assert isinstance(service.params[1][1], suds.xsd.sxbuiltin.XString)
    assert service.params[2][0].name == "x3"
    assert service.params[2][0].type[0] == "string"
    assert service.params[2][0].type[1] == "http://www.w3.org/2001/XMLSchema"
    assert isinstance(service.params[2][1], suds.xsd.sxbuiltin.XString)

    # Method parameters as read from a method object.
    assert len(service.ports) == 1
    port, methods = service.ports[0]
    assert len(methods) == 1
    method = methods[0]
    assert len(method) == 2
    method_name = method[0]
    assert method_name == "f"
    method_params = method[1]
    assert len(method_params) == 3
    assert method_params[0][0] == "x1"
    assert method_params[0][1] is service.params[0][0]
    assert method_params[1][0] == "x2"
    assert method_params[1][1] is service.params[1][0]
    assert method_params[2][0] == "x3"
    assert method_params[2][1] is service.params[2][0]


def test_global_enumeration():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:simpleType name="AAA">
        <xsd:restriction base="xsd:string">
          <xsd:enumeration value="One" />
          <xsd:enumeration value="Two" />
          <xsd:enumeration value="Thirty-Two" />
        </xsd:restriction>
      </xsd:simpleType>
    </xsd:schema>
  </wsdl:types>
  <wsdl:portType name="dummyPortType">
  </wsdl:portType>
  <wsdl:binding name="dummy" type="ns:dummyPortType">
    <soap:binding style="document"
    transport="http://schemas.xmlsoap.org/soap/http" />
  </wsdl:binding>
  <wsdl:service name="dummy">
    <wsdl:port name="dummy" binding="ns:dummy">
      <soap:address location="https://localhost/dummy" />
    </wsdl:port>
  </wsdl:service>
</wsdl:definitions>
""")

    assert len(client.sd) == 1
    service = client.sd[0]

    assert len(service.types) == 1
    for typeTuple in service.types:
        # Tuple containing the same object twice.
        assert len(typeTuple) == 2
        assert typeTuple[0] is typeTuple[1]

    aType = service.types[0][0]
    assert isinstance(aType, suds.xsd.sxbasic.Simple)
    assert aType.name == "AAA"
    assert aType.enum()
    assert aType.mixed()
    assert aType.restriction()
    assert not aType.choice()
    assert not aType.sequence()

    assert len(aType.rawchildren) == 1
    assert isinstance(aType.rawchildren[0], suds.xsd.sxbasic.Restriction)
    assert aType.rawchildren[0].ref[0] == "string"
    assert aType.rawchildren[0].ref[1] == "http://www.w3.org/2001/XMLSchema"

    enum = client.factory.create("AAA")
    assert enum.One == "One"
    assert enum.Two == "Two"
    assert getattr(enum, "Thirty-Two") == "Thirty-Two"


def test_global_sequence_in_a_global_sequence():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:complexType name="Oklahoma">
        <xsd:sequence>
          <xsd:element name="c1" type="xsd:string" />
          <xsd:element name="c2" type="xsd:string" />
          <xsd:element name="c3" type="xsd:string" />
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="Wackadoodle">
        <xsd:sequence>
          <xsd:element name="x1" type="xsd:string" />
          <xsd:element name="x2" type="Oklahoma" />
          <xsd:element name="x3" type="xsd:string" />
        </xsd:sequence>
      </xsd:complexType>
    </xsd:schema>
  </wsdl:types>
  <wsdl:portType name="dummyPortType">
  </wsdl:portType>
  <wsdl:binding name="dummy" type="ns:dummyPortType">
    <soap:binding style="document"
    transport="http://schemas.xmlsoap.org/soap/http" />
  </wsdl:binding>
  <wsdl:service name="dummy">
    <wsdl:port name="dummy" binding="ns:dummy">
      <soap:address location="https://localhost/dummy" />
    </wsdl:port>
  </wsdl:service>
</wsdl:definitions>
""")

    service = client.sd[0]

    assert len(service.types) == 2
    for typeTuple in service.types:
        # Tuple containing the same object twice.
        assert len(typeTuple) == 2
        assert typeTuple[0] is typeTuple[1]

    aTypeIn = service.types[0][0]
    assert isinstance(aTypeIn, suds.xsd.sxbasic.Complex)
    assert aTypeIn.name == "Oklahoma"
    assert not aTypeIn.sequence()
    assert aTypeIn.rawchildren[0].sequence()

    aTypeOut = service.types[1][0]
    assert isinstance(aTypeOut, suds.xsd.sxbasic.Complex)
    assert aTypeOut.name == "Wackadoodle"
    assert not aTypeOut.sequence()
    assert aTypeOut.rawchildren[0].sequence()

    assert len(aTypeOut.rawchildren) == 1
    children = aTypeOut.children()
    assert isinstance(children, list)
    assert len(children) == 3
    assert children[0][0].name == "x1"
    assert children[0][0].type[0] == "string"
    assert children[0][0].type[1] == "http://www.w3.org/2001/XMLSchema"
    assert children[1][0].name == "x2"
    assert children[1][0].type[0] == "Oklahoma"
    assert children[1][0].type[1] == "my-namespace"
    assert children[2][0].name == "x3"
    assert children[2][0].type[0] == "string"
    assert children[2][0].type[1] == "http://www.w3.org/2001/XMLSchema"

    sequenceOut = client.factory.create("Wackadoodle")
    _assert_dynamic_type(sequenceOut, "Wackadoodle")
    assert sequenceOut.__metadata__.sxtype is aTypeOut
    assert sequenceOut.x1 is None
    sequenceIn = sequenceOut.x2
    assert sequenceOut.x3 is None
    _assert_dynamic_type(sequenceIn, "Oklahoma")
    assert sequenceIn.__metadata__.sxtype is aTypeIn
    assert sequenceIn.c1 is None
    assert sequenceIn.c2 is None
    assert sequenceIn.c3 is None


def test_global_string_sequence():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:complexType name="Oklahoma">
        <xsd:sequence>
          <xsd:element name="c1" type="xsd:string" />
          <xsd:element name="c2" type="xsd:string" />
          <xsd:element name="c3" type="xsd:string" />
        </xsd:sequence>
      </xsd:complexType>
    </xsd:schema>
  </wsdl:types>
  <wsdl:portType name="dummyPortType">
  </wsdl:portType>
  <wsdl:binding name="dummy" type="ns:dummyPortType">
    <soap:binding style="document"
    transport="http://schemas.xmlsoap.org/soap/http" />
  </wsdl:binding>
  <wsdl:service name="dummy">
    <wsdl:port name="dummy" binding="ns:dummy">
      <soap:address location="https://localhost/dummy" />
    </wsdl:port>
  </wsdl:service>
</wsdl:definitions>
""")

    service = client.sd[0]

    assert len(service.types) == 1
    for typeTuple in service.types:
        # Tuple containing the same object twice.
        assert len(typeTuple) == 2
        assert typeTuple[0] is typeTuple[1]

    aType = service.types[0][0]
    assert isinstance(aType, suds.xsd.sxbasic.Complex)
    assert aType.name == "Oklahoma"
    assert not aType.choice()
    assert not aType.enum()
    assert not aType.mixed()
    assert not aType.restriction()
    assert not aType.sequence()

    assert len(aType.rawchildren) == 1
    sequence_node = aType.rawchildren[0]
    assert isinstance(sequence_node, suds.xsd.sxbasic.Sequence)
    assert sequence_node.sequence()
    assert len(sequence_node) == 3
    sequence_items = sequence_node.children()
    assert isinstance(sequence_items, list)
    assert len(sequence_items) == 3
    assert sequence_items[0][0].name == "c1"
    assert sequence_items[0][0].type[0] == "string"
    assert sequence_items[0][0].type[1] == "http://www.w3.org/2001/XMLSchema"
    assert sequence_items[1][0].name == "c2"
    assert sequence_items[1][0].type[0] == "string"
    assert sequence_items[1][0].type[1] == "http://www.w3.org/2001/XMLSchema"
    assert sequence_items[2][0].name == "c3"
    assert sequence_items[2][0].type[0] == "string"
    assert sequence_items[2][0].type[1] == "http://www.w3.org/2001/XMLSchema"

    sequence = client.factory.create("Oklahoma")
    getattr(sequence, "c1")
    getattr(sequence, "c2")
    getattr(sequence, "c3")
    pytest.raises(AttributeError, getattr, sequence, "nonExistingChild")
    assert sequence.c1 is None
    assert sequence.c2 is None
    assert sequence.c3 is None
    sequence.c1 = "Pero"
    sequence.c3 = "�dero"
    assert sequence.c1 == "Pero"
    assert sequence.c2 is None
    assert sequence.c3 == "�dero"


def test_local_sequence_in_a_global_sequence():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:complexType name="Wackadoodle">
        <xsd:sequence>
          <xsd:element name="x1">
              <xsd:complexType name="Oklahoma">
                <xsd:sequence>
                  <xsd:element name="c1" type="xsd:string" />
                  <xsd:element name="c2" type="xsd:string" />
                  <xsd:element name="c3" type="xsd:string" />
                </xsd:sequence>
              </xsd:complexType>
          </xsd:element>
          <xsd:element name="x2">
              <xsd:complexType>
                <xsd:sequence>
                  <xsd:element name="s" type="xsd:string" />
                </xsd:sequence>
              </xsd:complexType>
          </xsd:element>
        </xsd:sequence>
      </xsd:complexType>
    </xsd:schema>
  </wsdl:types>
  <wsdl:portType name="dummyPortType">
  </wsdl:portType>
  <wsdl:binding name="dummy" type="ns:dummyPortType">
    <soap:binding style="document"
    transport="http://schemas.xmlsoap.org/soap/http" />
  </wsdl:binding>
  <wsdl:service name="dummy">
    <wsdl:port name="dummy" binding="ns:dummy">
      <soap:address location="https://localhost/dummy" />
    </wsdl:port>
  </wsdl:service>
</wsdl:definitions>
""")

    service = client.sd[0]
    assert len(service.types) == 1

    aTypeOut = service.types[0][0]
    assert isinstance(aTypeOut, suds.xsd.sxbasic.Complex)
    assert aTypeOut.name == "Wackadoodle"
    assert not aTypeOut.sequence()
    assert aTypeOut.rawchildren[0].sequence()

    children = aTypeOut.children()
    assert isinstance(children, list)
    assert len(children) == 2
    aTypeIn1 = children[0][0]
    assert isinstance(aTypeIn1, suds.xsd.sxbasic.Element)
    assert not aTypeIn1.sequence()
    assert aTypeIn1.rawchildren[0].rawchildren[0].sequence()
    aTypeIn2 = children[1][0]
    assert isinstance(aTypeIn2, suds.xsd.sxbasic.Element)
    assert not aTypeIn2.sequence()
    assert aTypeIn2.rawchildren[0].rawchildren[0].sequence()
    assert aTypeIn1.rawchildren[0].name == "Oklahoma"
    assert aTypeIn1.rawchildren[0].type is None
    namespace1 = aTypeIn1.rawchildren[0].namespace()
    assert namespace1 == ("ns", "my-namespace")
    assert aTypeIn2.rawchildren[0].name is None
    assert aTypeIn2.rawchildren[0].type is None
    assert aTypeIn1.rawchildren[0].namespace() is namespace1

    sequenceOut = client.factory.create("Wackadoodle")
    _assert_dynamic_type(sequenceOut, "Wackadoodle")
    assert sequenceOut.__metadata__.sxtype is aTypeOut
    sequenceIn1 = sequenceOut.x1
    sequenceIn2 = sequenceOut.x2
    _assert_dynamic_type(sequenceIn1, "x1")
    _assert_dynamic_type(sequenceIn2, "x2")
    assert sequenceIn1.__metadata__.sxtype is aTypeIn1
    assert sequenceIn2.__metadata__.sxtype is aTypeIn2
    assert sequenceIn1.c1 is None
    assert sequenceIn1.c2 is None
    assert sequenceIn1.c3 is None
    assert sequenceIn2.s is None


def test_no_trailing_comma_in_function_prototype_description_string__0():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:element name="InputData">
        <xsd:complexType>
          <xsd:sequence />
        </xsd:complexType>
      </xsd:element>
    </xsd:schema>
  </wsdl:types>
  <wsdl:message name="fRequestMessage">
    <wsdl:part name="parameters" element="ns:InputData" />
  </wsdl:message>
  <wsdl:portType name="dummyPortType">
    <wsdl:operation name="f">
      <wsdl:input message="ns:fRequestMessage" />
    </wsdl:operation>
  </wsdl:portType>
  <wsdl:binding name="dummy" type="ns:dummyPortType">
    <soap:binding style="document"
    transport="http://schemas.xmlsoap.org/soap/http" />
    <wsdl:operation name="f">
      <soap:operation soapAction="f" style="document" />
      <wsdl:input><soap:body use="literal" /></wsdl:input>
      <wsdl:output><soap:body use="literal" /></wsdl:output>
    </wsdl:operation>
  </wsdl:binding>
  <wsdl:service name="dummy">
    <wsdl:port name="dummy" binding="ns:dummy">
      <soap:address location="https://localhost/dummy" />
    </wsdl:port>
  </wsdl:service>
</wsdl:definitions>
""")
    s = str(client)
    assert " f()\n" in s


def test_no_trailing_comma_in_function_prototype_description_string__1():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:element name="InputData">
        <xsd:complexType>
          <xsd:sequence>
            <xsd:element name="x1" type="xsd:string" />
          </xsd:sequence>
        </xsd:complexType>
      </xsd:element>
    </xsd:schema>
  </wsdl:types>
  <wsdl:message name="fRequestMessage">
    <wsdl:part name="parameters" element="ns:InputData" />
  </wsdl:message>
  <wsdl:portType name="dummyPortType">
    <wsdl:operation name="f">
      <wsdl:input message="ns:fRequestMessage" />
    </wsdl:operation>
  </wsdl:portType>
  <wsdl:binding name="dummy" type="ns:dummyPortType">
    <soap:binding style="document"
    transport="http://schemas.xmlsoap.org/soap/http" />
    <wsdl:operation name="f">
      <soap:operation soapAction="f" style="document" />
      <wsdl:input><soap:body use="literal" /></wsdl:input>
      <wsdl:output><soap:body use="literal" /></wsdl:output>
    </wsdl:operation>
  </wsdl:binding>
  <wsdl:service name="dummy">
    <wsdl:port name="dummy" binding="ns:dummy">
      <soap:address location="https://localhost/dummy" />
    </wsdl:port>
  </wsdl:service>
</wsdl:definitions>
""")
    s = str(client)
    assert " f(xs:string x1)\n" in s


def test_no_trailing_comma_in_function_prototype_description_string__3():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:element name="InputData">
        <xsd:complexType>
          <xsd:sequence>
            <xsd:element name="x1" type="xsd:string" />
            <xsd:element name="x2" type="xsd:string" />
            <xsd:element name="x3" type="xsd:string" />
          </xsd:sequence>
        </xsd:complexType>
      </xsd:element>
    </xsd:schema>
  </wsdl:types>
  <wsdl:message name="fRequestMessage">
    <wsdl:part name="parameters" element="ns:InputData" />
  </wsdl:message>
  <wsdl:portType name="dummyPortType">
    <wsdl:operation name="f">
      <wsdl:input message="ns:fRequestMessage" />
    </wsdl:operation>
  </wsdl:portType>
  <wsdl:binding name="dummy" type="ns:dummyPortType">
    <soap:binding style="document"
    transport="http://schemas.xmlsoap.org/soap/http" />
    <wsdl:operation name="f">
      <soap:operation soapAction="f" style="document" />
      <wsdl:input><soap:body use="literal" /></wsdl:input>
      <wsdl:output><soap:body use="literal" /></wsdl:output>
    </wsdl:operation>
  </wsdl:binding>
  <wsdl:service name="dummy">
    <wsdl:port name="dummy" binding="ns:dummy">
      <soap:address location="https://localhost/dummy" />
    </wsdl:port>
  </wsdl:service>
</wsdl:definitions>
""")
    s = str(client)
    assert " f(xs:string x1, xs:string x2, xs:string x3)\n" in s


def test_no_types():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema" />
  </wsdl:types>
  <wsdl:portType name="dummyPortType">
  </wsdl:portType>
  <wsdl:binding name="dummy" type="ns:dummyPortType">
    <soap:binding style="document"
    transport="http://schemas.xmlsoap.org/soap/http" />
  </wsdl:binding>
  <wsdl:service name="dummy">
    <wsdl:port name="dummy" binding="ns:dummy">
      <soap:address location="https://localhost/dummy" />
    </wsdl:port>
  </wsdl:service>
</wsdl:definitions>
""")

    assert len(client.sd) == 1
    service = client.sd[0]

    assert not client.wsdl.schema.types
    assert not service.types

    pytest.raises(suds.TypeNotFound, client.factory.create, "NonExistingType")


def test_parameter_referencing_missing_element():
    try:
        client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    </xsd:schema>
  </wsdl:types>
  <wsdl:message name="fRequestMessage">
    <wsdl:part name="parameters" element="ns:missingElement" />
  </wsdl:message>
  <wsdl:portType name="dummyPortType">
    <wsdl:operation name="f">
      <wsdl:input message="ns:fRequestMessage" />
    </wsdl:operation>
  </wsdl:portType>
  <wsdl:binding name="dummy" type="ns:dummyPortType">
    <soap:binding style="document"
    transport="http://schemas.xmlsoap.org/soap/http" />
    <wsdl:operation name="f">
      <soap:operation soapAction="f" style="document" />
      <wsdl:input><soap:body use="literal" /></wsdl:input>
      <wsdl:output><soap:body use="literal" /></wsdl:output>
    </wsdl:operation>
  </wsdl:binding>
  <wsdl:service name="dummy">
    <wsdl:port name="dummy" binding="ns:dummy">
      <soap:address location="https://localhost/dummy" />
    </wsdl:port>
  </wsdl:service>
</wsdl:definitions>
""")
        pytest.fail("Excepted exception suds.TypeNotFound not thrown.")
    except suds.TypeNotFound, e:
        assert str(e) == "Type not found: '(missingElement, my-namespace, )'"


def test_schema_node_occurrences():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
"""
    + _element_node_xml("AnElement1")
    + _element_node_xml("AnElement2", min=1)
    + _element_node_xml("AnElement3", max=1)

    + _element_node_xml("AnOptionalElement1", min=0)
    + _element_node_xml("AnOptionalElement2", min=0, max=1)

    + _element_node_xml("Array_0_2", min=0, max=2)
    + _element_node_xml("Array_0_999", min=0, max=999)
    + _element_node_xml("Array_0_X", min=0, max="unbounded")

    + _element_node_xml("Array_x_2", max=2)
    + _element_node_xml("Array_x_999", max=999)
    + _element_node_xml("Array_x_X", max="unbounded")

    + _element_node_xml("Array_1_2", min=1, max=2)
    + _element_node_xml("Array_1_999", min=1, max=999)
    + _element_node_xml("Array_1_X", min=1, max="unbounded")

    + _element_node_xml("Array_5_5", min=5, max=5)
    + _element_node_xml("Array_5_999", min=5, max=999)
    + _element_node_xml("Array_5_X", min=5, max="unbounded")
+ """
    </xsd:schema>
  </wsdl:types>
</wsdl:definitions>
""")
    schema = client.wsdl.schema

    def a(schema, name, min=None, max=None):
        element = schema.elements[name, "my-namespace"]

        if min is None:
            assert element.min is None
            min = 1
        else:
            assert str(min) == element.min
        if max is None:
            assert element.max is None
            max = 1
        else:
            assert str(max) == element.max

        expected_optional = min == 0
        assert expected_optional == element.optional()

        expected_required = not expected_optional
        assert expected_required == element.required()

        expected_multi_occurrence = (max == "unbounded") or (max > 1)
        assert expected_multi_occurrence == element.multi_occurrence()

    a(schema, "AnElement1")
    a(schema, "AnElement2", min=1)
    a(schema, "AnElement3", max=1)

    a(schema, "AnOptionalElement1", min=0)
    a(schema, "AnOptionalElement2", min=0, max=1)

    a(schema, "Array_0_2", min=0, max=2)
    a(schema, "Array_0_999", min=0, max=999)
    a(schema, "Array_0_X", min=0, max="unbounded")

    a(schema, "Array_x_2", max=2)
    a(schema, "Array_x_999", max=999)
    a(schema, "Array_x_X", max="unbounded")

    a(schema, "Array_1_2", min=1, max=2)
    a(schema, "Array_1_999", min=1, max=999)
    a(schema, "Array_1_X", min=1, max="unbounded")

    a(schema, "Array_5_5", min=5, max=5)
    a(schema, "Array_5_999", min=5, max=999)
    a(schema, "Array_5_X", min=5, max="unbounded")


def test_schema_node_resolve():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:complexType name="Typo">
        <xsd:sequence>
          <xsd:element name="u1" type="xsd:string" />
          <xsd:element name="u2" type="xsd:string" />
          <xsd:element name="u3" type="xsd:string" />
        </xsd:sequence>
      </xsd:complexType>
      <xsd:element name="Elemento">
        <xsd:complexType>
          <xsd:sequence>
            <xsd:element name="x1" type="xsd:string" />
            <xsd:element name="x2" type="Typo" />
            <xsd:element name="x3">
              <xsd:complexType>
                <xsd:sequence>
                  <xsd:element name="a1" type="xsd:string" />
                  <xsd:element name="a2" type="xsd:string" />
                </xsd:sequence>
              </xsd:complexType>
            </xsd:element>
          </xsd:sequence>
        </xsd:complexType>
      </xsd:element>
      <xsd:element name="ElementoTyped" type="Typo" />
    </xsd:schema>
  </wsdl:types>
</wsdl:definitions>
""")
    schema = client.wsdl.schema

    # Collect references to the test schema type nodes.
    assert len(schema.types) == 1
    typo = schema.types["Typo", "my-namespace"]
    typo_u1 = typo.children()[0][0]
    assert typo_u1.name == "u1"

    # Collect references to the test schema element nodes.
    assert len(schema.elements) == 2
    elemento = schema.elements["Elemento", "my-namespace"]
    elemento_x2 = elemento.children()[1][0]
    assert elemento_x2.name == "x2"
    elemento_x3 = elemento.children()[2][0]
    assert elemento_x3.name == "x3"
    elementoTyped = schema.elements["ElementoTyped", "my-namespace"]

    # Resolving top-level locally defined non-content nodes.
    assert typo.resolve() is typo

    # Resolving a correctly typed top-level locally typed element.
    assert elemento.resolve() is elemento

    # Resolving top-level globally typed elements.
    assert elementoTyped.resolve() is typo

    # Resolving a subnode referencing a globally defined type.
    assert elemento_x2.resolve() is typo

    # Resolving a locally defined subnode.
    assert elemento_x3.resolve() is elemento_x3

    # Resolving builtin type nodes.
    assert typo_u1.resolve().__class__ is suds.xsd.sxbuiltin.XString
    assert typo_u1.resolve(nobuiltin=False).__class__ is  \
        suds.xsd.sxbuiltin.XString
    assert typo_u1.resolve(nobuiltin=True) is typo_u1
    assert elemento_x2.resolve(nobuiltin=True) is typo
    assert elemento_x3.resolve(nobuiltin=True) is elemento_x3


def test_schema_node_resolve__nobuiltin_caching():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:element name="Elemento1" type="xsd:string" />
      <xsd:element name="Elemento2" type="xsd:string" />
      <xsd:element name="Elemento3" type="xsd:string" />
      <xsd:element name="Elemento4" type="xsd:string" />
    </xsd:schema>
  </wsdl:types>
</wsdl:definitions>
""")
    schema = client.wsdl.schema

    # Collect references to the test schema element nodes.
    assert len(schema.elements) == 4
    e1 = schema.elements["Elemento1", "my-namespace"]
    e2 = schema.elements["Elemento2", "my-namespace"]
    e3 = schema.elements["Elemento3", "my-namespace"]
    e4 = schema.elements["Elemento4", "my-namespace"]

    #   Repeating the same resolve() call twice makes sure that the first call
    # does not cache an incorrect value, thus causing the second call to return
    # an incorrect result.

    assert e1.resolve().__class__ is suds.xsd.sxbuiltin.XString
    assert e1.resolve().__class__ is suds.xsd.sxbuiltin.XString

    assert e2.resolve(nobuiltin=True) is e2
    assert e2.resolve(nobuiltin=True) is e2

    assert e3.resolve().__class__ is suds.xsd.sxbuiltin.XString
    assert e3.resolve(nobuiltin=True) is e3
    assert e3.resolve(nobuiltin=True) is e3

    assert e4.resolve(nobuiltin=True) is e4
    assert e4.resolve().__class__ is suds.xsd.sxbuiltin.XString
    assert e4.resolve().__class__ is suds.xsd.sxbuiltin.XString


def test_schema_node_resolve__invalid_type():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:element name="Elemento1" type="Elemento1" />
      <xsd:element name="Elemento2" type="Elemento1" />
      <xsd:element name="Elemento3" type="XXX" />
    </xsd:schema>
  </wsdl:types>
</wsdl:definitions>
""")
    schema = client.wsdl.schema
    assert len(schema.elements) == 3
    elemento1 = schema.elements["Elemento1", "my-namespace"]
    elemento2 = schema.elements["Elemento2", "my-namespace"]
    elemento3 = schema.elements["Elemento3", "my-namespace"]
    pytest.raises(suds.TypeNotFound, elemento1.resolve)
    pytest.raises(suds.TypeNotFound, elemento2.resolve)
    pytest.raises(suds.TypeNotFound, elemento3.resolve)


def test_schema_node_resolve__references():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:complexType name="Typo">
        <xsd:sequence>
          <xsd:element name="u1" type="xsd:string" />
          <xsd:element name="u2" type="xsd:string" />
          <xsd:element name="u3" type="xsd:string" />
        </xsd:sequence>
      </xsd:complexType>
      <xsd:element name="ElementoTyped" type="Typo" />
      <xsd:element name="ElementoTyped11" ref="ElementoTyped" />
      <xsd:element name="ElementoTyped12" ref="ElementoTyped11" />
      <xsd:element name="ElementoTyped13" ref="ElementoTyped12" />
      <xsd:element name="ElementoTyped21" ref="ElementoTyped" />
      <xsd:element name="ElementoTyped22" ref="ElementoTyped21" />
      <xsd:element name="ElementoTyped23" ref="ElementoTyped22" />
      <xsd:element name="ElementoTypedX" ref="ElementoTypedX" />
      <xsd:element name="ElementoTypedX1" ref="ElementoTypedX2" />
      <xsd:element name="ElementoTypedX2" ref="ElementoTypedX1" />
    </xsd:schema>
  </wsdl:types>
</wsdl:definitions>
""")
    schema = client.wsdl.schema

    # Collect references to the test schema element & type nodes.
    assert len(schema.types) == 1
    typo = schema.types["Typo", "my-namespace"]
    assert len(schema.elements) == 10
    elementoTyped = schema.elements["ElementoTyped", "my-namespace"]
    elementoTyped11 = schema.elements["ElementoTyped11", "my-namespace"]
    elementoTyped12 = schema.elements["ElementoTyped12", "my-namespace"]
    elementoTyped13 = schema.elements["ElementoTyped13", "my-namespace"]
    elementoTyped21 = schema.elements["ElementoTyped21", "my-namespace"]
    elementoTyped22 = schema.elements["ElementoTyped22", "my-namespace"]
    elementoTyped23 = schema.elements["ElementoTyped23", "my-namespace"]
    elementoTypedX = schema.elements["ElementoTypedX", "my-namespace"]
    elementoTypedX1 = schema.elements["ElementoTypedX1", "my-namespace"]
    elementoTypedX2 = schema.elements["ElementoTypedX2", "my-namespace"]

    #   For referenced element node chains try resolving their nodes in both
    # directions and try resolving them twice to try and avoid any internal
    # resolve result caching that might cause some resursive resolution branch
    # to not get taken.
    #   Note that these assertions are actually redundant since inter-element
    # references get processed and referenced type information merged back into
    # the referencee when the schema information is loaded so no recursion is
    # needed here in the first place. The tests should still be left in place
    # and pass to serve as a safeguard in case this reference processing gets
    # changed in the future.
    assert elementoTyped11.resolve() is typo
    assert elementoTyped11.resolve() is typo
    assert elementoTyped13.resolve() is typo
    assert elementoTyped13.resolve() is typo

    assert elementoTyped23.resolve() is typo
    assert elementoTyped23.resolve() is typo
    assert elementoTyped21.resolve() is typo
    assert elementoTyped21.resolve() is typo

    # Recursive element references.
    assert elementoTypedX.resolve() is elementoTypedX
    assert elementoTypedX1.resolve() is elementoTypedX1
    assert elementoTypedX2.resolve() is elementoTypedX2


def test_schema_object_child_access_by_index():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:complexType name="Oklahoma">
        <xsd:sequence>
          <xsd:element name="c1" type="xsd:string" />
          <xsd:element name="c2" type="xsd:string" />
          <xsd:element name="c3" type="xsd:string" />
        </xsd:sequence>
      </xsd:complexType>
    </xsd:schema>
  </wsdl:types>
  <wsdl:portType name="dummyPortType">
  </wsdl:portType>
  <wsdl:binding name="dummy" type="ns:dummyPortType">
    <soap:binding style="document"
    transport="http://schemas.xmlsoap.org/soap/http" />
  </wsdl:binding>
  <wsdl:service name="dummy">
    <wsdl:port name="dummy" binding="ns:dummy">
      <soap:address location="https://localhost/dummy" />
    </wsdl:port>
  </wsdl:service>
</wsdl:definitions>
""")

    service = client.sd[0]
    aType = service.types[0][0]
    sequence = aType.rawchildren[0]
    assert isinstance(sequence, suds.xsd.sxbasic.Sequence)
    children = aType.children()
    assert isinstance(children, list)

    assert sequence[-1] is None

    # TODO: Children are returned as a 2-tuple containing the child element and
    # its ancestry (list of its parent elements). For some reason the ancestry
    # list is returned as a new list on every __getitem__() call and so can not
    # be compared using the 'is' operator. Also the children() function and
    # accesing children by index does not seem to return ancestry lists of the
    # same depth. See whether this can be updated so we always get the same
    # ancestry list object.
    # TODO: Add more detailed tests for the ancestry list structure.
    # TODO: Add more detailed tests for the rawchildren list structure.

    assert isinstance(sequence[0], tuple)
    assert len(sequence[0]) == 2
    assert sequence[0][0] is children[0][0]

    assert isinstance(sequence[1], tuple)
    assert len(sequence[1]) == 2
    assert sequence[1][0] is children[1][0]

    assert isinstance(sequence[2], tuple)
    assert len(sequence[2]) == 2
    assert sequence[2][0] is children[2][0]

    assert sequence[3] is None


def test_simple_wsdl():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:element name="f">
        <xsd:complexType>
          <xsd:sequence>
            <xsd:element name="a" type="xsd:string" />
            <xsd:element name="b" type="xsd:string" />
          </xsd:sequence>
        </xsd:complexType>
      </xsd:element>
      <xsd:element name="fResponse">
        <xsd:complexType>
          <xsd:sequence>
            <xsd:element name="c" type="xsd:string" />
          </xsd:sequence>
        </xsd:complexType>
      </xsd:element>
    </xsd:schema>
  </wsdl:types>
  <wsdl:message name="fRequestMessage">
    <wsdl:part name="parameters" element="ns:f" />
  </wsdl:message>
  <wsdl:message name="fResponseMessage">
    <wsdl:part name="parameters" element="ns:fResponse" />
  </wsdl:message>
  <wsdl:portType name="dummyPortType">
    <wsdl:operation name="f">
      <wsdl:input message="ns:fRequestMessage" />
      <wsdl:output message="ns:fResponseMessage" />
    </wsdl:operation>
  </wsdl:portType>
  <wsdl:binding name="dummy" type="ns:dummyPortType">
    <soap:binding style="document"
    transport="http://schemas.xmlsoap.org/soap/http" />
    <wsdl:operation name="f">
      <soap:operation soapAction="f" style="document" />
      <wsdl:input><soap:body use="literal" /></wsdl:input>
      <wsdl:output><soap:body use="literal" /></wsdl:output>
    </wsdl:operation>
  </wsdl:binding>
  <wsdl:service name="dummy">
    <wsdl:port name="dummy" binding="ns:dummy">
      <soap:address location="https://localhost/dummy" />
    </wsdl:port>
  </wsdl:service>
</wsdl:definitions>
""")

    # Target namespace.
    assert client.wsdl.tns[0] == "ns"
    assert client.wsdl.tns[1] == "my-namespace"

    # Elements.
    assert len(client.wsdl.schema.elements) == 2
    elementIn = client.wsdl.schema.elements["f", "my-namespace"]
    elementOut = client.wsdl.schema.elements["fResponse", "my-namespace"]
    assert isinstance(elementIn, suds.xsd.sxbasic.Element)
    assert isinstance(elementOut, suds.xsd.sxbasic.Element)
    assert elementIn.name == "f"
    assert elementOut.name == "fResponse"

    # Service definition.
    assert len(client.sd) == 1
    service_definition = client.sd[0]
    assert service_definition.wsdl is client.wsdl

    # Service.
    assert len(client.wsdl.services) == 1
    service = client.wsdl.services[0]
    assert service_definition.service is service

    # Ports.
    assert len(service.ports) == 1
    port = service.ports[0]
    assert len(service_definition.ports) == 1
    assert len(service_definition.ports[0]) == 2
    assert service_definition.ports[0][0] is port

    # Methods (from wsdl).
    assert len(port.methods) == 1
    method_name, method = _first_from_dict(port.methods)
    assert method_name == "f"
    assert method.name == "f"
    assert method.location == b"https://localhost/dummy"

    # Methods (from service definition, for format specifications see the
    # suds.ServiceDefinition.addports() docstring).
    port, methods = service_definition.ports[0]
    assert len(methods) == 1
    method = methods[0]
    assert len(method) == 2
    method_name = method[0]
    assert method_name == "f"
    method_params = method[1]
    assert len(method_params) == 2
    assert method_params[0][0] == "a"
    assert method_params[1][0] == "b"

    # TODO: Once we learn more about suds - add the following assertions:
    #   * assert method.input parameters = a (string), b (string).
    #   * assert method.output parameters = c (string).


def test_wsdl_schema_content():
    client = _client_from_wsdl(
"""<?xml version='1.0' encoding='UTF-8'?>
<wsdl:definitions targetNamespace="my-namespace"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:ns="my-namespace"
xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:types>
    <xsd:schema targetNamespace="my-namespace"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:complexType name="UngaBunga">
        <xsd:sequence>
          <xsd:element name="u1" type="xsd:string" />
          <xsd:element name="u2" type="xsd:string" />
          <xsd:element name="u3" type="xsd:string" />
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="Fifi">
        <xsd:sequence>
          <xsd:element name="x" type="xsd:string" />
        </xsd:sequence>
      </xsd:complexType>
      <xsd:element name="Elemento">
        <xsd:complexType>
          <xsd:sequence>
            <xsd:element name="x1" type="xsd:string" />
            <xsd:element name="x2" type="UngaBunga" />
            <xsd:element name="x3">
              <xsd:complexType>
                <xsd:sequence>
                  <xsd:element name="a1" type="xsd:string" />
                  <xsd:element name="a2" type="xsd:string" />
                </xsd:sequence>
              </xsd:complexType>
            </xsd:element>
          </xsd:sequence>
        </xsd:complexType>
      </xsd:element>
    </xsd:schema>
  </wsdl:types>
</wsdl:definitions>
""")

    # Elements.
    assert len(client.wsdl.schema.elements) == 1
    elemento = client.wsdl.schema.elements["Elemento", "my-namespace"]
    assert isinstance(elemento, suds.xsd.sxbasic.Element)

    pytest.raises(KeyError, client.wsdl.schema.elements.__getitem__,
        ("DoesNotExist", "OMG"))

    # Types.
    assert len(client.wsdl.schema.types) == 2
    unga_bunga = client.wsdl.schema.types["UngaBunga", "my-namespace"]
    assert isinstance(unga_bunga, suds.xsd.sxbasic.Complex)
    fifi = client.wsdl.schema.types["Fifi", "my-namespace"]
    assert isinstance(unga_bunga, suds.xsd.sxbasic.Complex)

    pytest.raises(KeyError, client.wsdl.schema.types.__getitem__,
        ("DoesNotExist", "OMG"))


def _assert_dynamic_type(anObject, typename):
    assert anObject.__module__ == suds.sudsobject.__name__
    assert anObject.__metadata__.sxtype.name == typename
    #   In order to be compatible with old style classes (py2 only) we need to
    # access the object's class information using its __class__ member and not
    # the type() function. type() function always returns <type 'instance'> for
    # old-style class instances while the __class__ member returns the correct
    # class information for both old and new-style classes.
    assert anObject.__class__.__module__ == suds.sudsobject.__name__
    assert anObject.__class__.__name__ == typename


def _client_from_wsdl(wsdl_content):
    """
    Constructs a non-caching suds Client based on the given WSDL content.

      Stores the content directly inside the suds library internal document
    store under a hard-coded id to avoid having to load the data from a
    temporary file.

      Caveats:
        * All files stored under the same id so each new local file overwrites
          the previous one.
        * We need to explicitly disable caching here or otherwise, because we
          are using the same id for all our local WSDL documents, suds would
          always reuse the first such local document from its cache.

    """
    # Idea for an alternative implementation:
    #   Custom suds.cache.Cache subclass that would know how to access our
    # locally stored documents or at least not cache them if we are storing
    # them inside the suds library DocumentStore. Not difficult, allows us to
    # have per-client instead of global configuration & allows us to support
    # other cache types but certainly not as short as the current
    # implementation.
    testFileId = "whatchamacallit"
    suds.store.DocumentStore.store[testFileId] = wsdl_content
    return suds.client.Client("suds://" + testFileId, cache=None)


def _construct_SOAP_request(client, operation_name, *args, **kwargs):
    """
    Returns a SOAP request for a given web service operation invocation.

      To make the test case code calling this function simpler, assumes we want
    to call the operation on the given client's first service & port.

    """
    method = client.wsdl.services[0].ports[0].methods[operation_name]
    return method.binding.input.get_message(method, args, kwargs)


def _element_node_xml(name, min=None, max=None):
    s = []
    s.append('      <xsd:element name="')
    s.append(name)
    s.append('" type="xsd:string" ')
    if min is not None:
        s.append('minOccurs="{}" '.format(min))
    if max is not None:
        s.append('maxOccurs="{}" '.format(max))
    s.append('/>\n')
    return ''.join(s)


def _first_from_dict(d):
    """Returns the first name/value pair from a dictionary or None if empty."""
    for x in d.items():
        return x[0], x[1]
