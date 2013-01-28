from __future__ import absolute_import

from xml.etree.ElementTree import Element, SubElement

from . import setup_menu


def register_setup(link):
    SubElement(setup_menu, 'setup_link', link=link)
