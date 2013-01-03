from __future__ import absolute_import

from xml.etree.ElementTree import Element, SubElement

from . import tool_menu


def register_tool(link):
    SubElement(tool_menu, 'tool_link', link=link)
