from bs4 import BeautifulSoup
import pprint

def is_gridcell_and_visible(tag):
    if( not tag.has_attr('role')):
        return False
    if( tag.has_attr('style') and ('display: none' in tag.attrs['style'] or 'display:none' in tag.attrs['style'])):
        return False
    else:
        return True

with open('E:\\000 Workspace\\html\\test2.html', encoding='utf-8') as f:
    text = f.read()
    html = BeautifulSoup(text, 'html.parser')
    row = html.find(id = 'row0jqxgrid')

