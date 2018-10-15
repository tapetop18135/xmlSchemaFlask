from zeep import Client
from lxml import etree 
import xmlschema


client = Client('http://localhost:8000/soapAPI1/?wsdl')
resultlistfood = client.service.listfoodService()
resultXMLtest = client.service.getGrapXMLdata()
# print(resultXMLtest)

root = etree.fromstring(resultlistfood)
for food in root.findall('food'):
    print("name :",food.find('name').text)
    print("price :",food.find('price').text)
    print("descr :",food.find('description').text.replace('\n',' '))
    print("cal :",food.find('calories').text)
    print()

# # print(resultXMLtest)

# utf8_parser = etree.XMLParser(encoding='utf-8')
# root = etree.fromstring(resultXMLtest.encode('utf-8'), parser=utf8_parser)
# # print(root)
# for food in root.findall('item'):
#     print("date :",food.find('date_use').text)
#     print("x :",food.find('x_lat').text)
#     print("y :",food.find('y_value').text)
#     print()

