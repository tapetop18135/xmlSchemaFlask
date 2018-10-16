from spyne import Iterable, Integer, Unicode, rpc, Application, ServiceBase, Array, TTableModel, Integer32, String, ComplexModel, Float, xml
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.protocol.soap import Soap11
from spyne.protocol.xml import XmlDocument

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker

import sqlite3
from flask import g
import xmlschema

from lxml import etree
import dicttoxml
# Generate a ComplexModelBase subclass with
# metadata information
# Initialize SQLAlchemy Environment
engine = create_engine('sqlite:///./db.db')

class GraphPlotValue(ComplexModel):
    __namespace__ = "graphSST"
    key = Integer()
    lat = Float()
    sst = Float()
    date_use = String()

def mapArray(Array_t):
    temp = []
    for i in Array_t:
        temp.append(GraphPlotValue(key=i[0], lat=i[1], sst=i[2], date_use=i[3],))

    return temp

class HelloWorldService(ServiceBase):

    @rpc(_returns=Iterable(GraphPlotValue))
    def testDB(ctx):
        result = engine.execute('select * from dataSST')
        # for r in result:
        #     print(r)
        v = mapArray(result)

        return v

    @rpc(_returns=String)
    def listfoodService(ctx):

        my_schema = xmlschema.XMLSchema('./data/xsd/breakfast_menu.xsd')
        if(my_schema.is_valid('./data/xml/breakfast_menu.xml')):
            with open('./data/xml/breakfast_menu.xml') as f:
                resultXML = f.read()
            result = resultXML
        else:
            result = """<Error>Error NOT Valid</Error>"""

        return result


    @rpc(_returns=String)
    def getGrapXMLdata(ctx):

        results = engine.execute('select * from dataSST')
        dictTemp = []
        for r in results:
            tempData={}
            tempData['date_use'] = r[3]
            tempData['x_lat'] = r[1]
            tempData['y_value'] = r[2]
        
            dictTemp.append(tempData)
        
        xml = dicttoxml.dicttoxml(dictTemp)

        my_schema = xmlschema.XMLSchema('./data/xsd/graphLat.xsd')
        root = etree.XML(xml)
        if(my_schema.is_valid(root)):
            result = xml
        else:
            result = """<Error>Error NOT Valid</Error>"""

        return result


def create_app(flask_app):
    """Creates SOAP services application and distribute Flask config into
    user con defined context for each method call.
    """
    application = Application([HelloWorldService], 'spyne.examples.flask',
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11()
        # out_protocol=Soap11(),
    )

    return application