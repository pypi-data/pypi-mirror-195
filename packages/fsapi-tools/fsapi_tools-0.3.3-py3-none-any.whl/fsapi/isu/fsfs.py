# MIT License

# Copyright (c) 2023 MatrixEditor

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
__doc__ = '''
When using the ISU module and their ISUInspector instances, the ``get_fs_tree``
method returns an object of the ``FSFSTree`` class. It is used to create XML
structured files

>>> root = FSFSTree()
>>> child = FSFSFile('file', {'size': 200})
>>> root.append(child)
>>> root.to_xml()
<fsh1 name="Frontier-Smart-FS"><file size=200 /></fsh1>
'''

__all__ = [
    'FSFSFile', 'FSFSTree'
]

from typing import Iterator


class FSFSFile:
    '''The base class for File-System tree objects.

    Classes that implement the functionalities of this class can be represented as
    a tree. Some built-in functions have been declared to make this class even more
    usable. They are:

    * ``__iter__``: Objects of this class can be used in a `for`-loop.
    * ``__len__``: Used to retrieve the amount of children of this "node"
    * ``__get_item__``: collection behaviour -> get children from their index position

    This class can be used as follows:

    >>> root = FSFSFile('foo', {'size': 10}, text='bar')
    >>> root.to_xml()
    <foo size=10>bar</foo>

    :param tag:        the XML-tag (e.g. <tag></tag>)
    :param attributes: a simple ``dict`` object storing all additional attributes used
                        to describe this object.
    :param text:       the text that will be added between the XML-tags

    '''

    def __init__(self, tag: str, attributes: dict, text: str = None) -> None:
        self.tag = tag
        self.attrs = attributes
        self.text = text
        self.elements = []

    def __iter__(self) -> Iterator:
        return iter(self.elements)

    def __len__(self) -> int:
        return len(self.elements)

    def __get_item__(self, index) -> 'FSFSFile':
        return self.elements[index]

    def get_elements(self) -> list:
        '''Returns all child-nodes.'''
        return self.elements

    def set_attribute(self, name, value):
        '''Sets a new value for the given attribute name.'''
        self.attrs[name] = value

    def get_attribute(self, name):
        '''Returns the stores attribute's value.'''
        return self.attrs[name]

    def get_by_tag(self, tag: str) -> list:
        """Searches recursively by the given tag name.

        :param tag: the tag to look for
        :type tag: str
        :return: a list of elements with the given tag name
        :rtype: list
        """
        values = []
        if self.tag == tag:
            values.append(self)

        for element in self:
            if isinstance(element, FSFSFile):
                values += element.getElementsByTagName(tag)

        return values

    def get_element(self, tag: str) -> 'FSFSFile':
        '''Returns an element with the same tag'''
        for elmnt in self:
            if elmnt.tag == tag:
                return elmnt
        return None

    def to_xml(self, indent='') -> str:
        '''Converts this object into a string (XML-format).'''
        txt = self.text if self.text else ""
        xml_str = f"{indent}<{self.tag}{self._attr_to_str()}"

        if not self.text and len(self.elements) == 0:
            return xml_str + " />"

        xml_str += '>'
        if len(self.elements) != 0:
            for element in self.elements:
                xml_str += '\n' + element.to_xml(indent=indent + '\t')
        if self.text:
            return xml_str + f"{txt}</{self.tag}>"
        else:
            return xml_str + f"\n{indent}</{self.tag}>"

    def _attr_to_str(self) -> str:
        if len(self.attrs) == 0:
            return ""

        x_str = []
        for key in self.attrs:
            value = self.attrs[key]
            if not isinstance(value, int):
                x_str.append(f'{key}="{value}"')
            else:
                x_str.append(f'{key}={value}')
        return ' ' + ', '.join(x_str)

    def append(self, element: 'FSFSFile'):
        """Adds a given FSFSFile object to this one."""
        if element is not None:
            self.elements.append(element)

    def rem_attribute(self, name):
        """Removes the mapped value for the given name, if stored. (and returns it afterwards)"""
        if name in self.attrs:
            return self.attrs.pop(name)
        return None


class FSFSTree(FSFSFile):
    '''A simple delegator for FSFSFile objects.

    FSFSTree objects define their own XML-tag and attributes (if none was
    given). The default output on a FSFSTree would be the following one:

    >>> FSFSTree().to_xml()
    <fsh1 name="Frontier-Smart-FS" />

    :param attributes: a simple ``dict`` object storing all additional attributes
                        used to describe this object.
    '''

    def __init__(self, attributes: dict = None) -> None:
        super().__init__('fsh1',
            attributes if attributes else {'name': 'Frontier-Smart-FS'}
        )
