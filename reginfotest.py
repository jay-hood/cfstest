import requests
from lxml import html, etree

res = requests.get('http://media.ethics.ga.gov/Search/Campaign/Campaign_Name.aspx?NameID=563&FilerID=C2017000285&Type=candidate')
tree = html.fromstring(res.content)
base = 'ctl00_ContentPlaceHolder1_Name_Reports1_TabContainer1_TabPanel2_lbl'
name = base+'Name'
party = base+'PartyAffiliation'
street = base+'Address'
csz = base+'CSZ'
name_info = tree.xpath(f'//*[@id="{name}"]/text()')
party_info = tree.xpath(f"//*[@id='{party}']/text()")
street_info = tree.xpath(f"//*[@id='{street}']/text()")
csz = tree.xpath(f"//*[@id='{csz}']/text()")
try:
    if name_info:
        print(name_info.pop())
    else:
        print('No name info')
    if party_info:
        print(party_info.pop())
    else:
        print('No party info')
    if street_info:
        print(street_info.pop())
    else:
        print('No street info')
    if csz:
        print(csz.pop())
    else:
        print('No csz info')
except Exception as e:
    print(e)
