# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose">
#   Copyright (c) 2018 Aspose.Slides for Cloud
# </copyright>
# <summary>
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# </summary>
# -----------------------------------------------------------------------------------

import pprint
import re  # noqa: F401

import six

from asposeslidescloud.models.image_transform_effect import ImageTransformEffect

class ColorChangeEffect(ImageTransformEffect):


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'type': 'str',
        'from_color': 'str',
        'to_color': 'str'
    }

    attribute_map = {
        'type': 'type',
        'from_color': 'fromColor',
        'to_color': 'toColor'
    }

    type_determiners = {
        'type': 'ColorChange',
    }

    def __init__(self, type='ColorChange', from_color=None, to_color=None):  # noqa: E501
        """ColorChangeEffect - a model defined in Swagger"""  # noqa: E501
        super(ColorChangeEffect, self).__init__(type)

        self._from_color = None
        self._to_color = None
        self.type = 'ColorChange'

        if from_color is not None:
            self.from_color = from_color
        if to_color is not None:
            self.to_color = to_color

    @property
    def from_color(self):
        """Gets the from_color of this ColorChangeEffect.  # noqa: E501

        Color which will be replaced.  # noqa: E501

        :return: The from_color of this ColorChangeEffect.  # noqa: E501
        :rtype: str
        """
        return self._from_color

    @from_color.setter
    def from_color(self, from_color):
        """Sets the from_color of this ColorChangeEffect.

        Color which will be replaced.  # noqa: E501

        :param from_color: The from_color of this ColorChangeEffect.  # noqa: E501
        :type: str
        """
        self._from_color = from_color

    @property
    def to_color(self):
        """Gets the to_color of this ColorChangeEffect.  # noqa: E501

        Color which will replace.  # noqa: E501

        :return: The to_color of this ColorChangeEffect.  # noqa: E501
        :rtype: str
        """
        return self._to_color

    @to_color.setter
    def to_color(self, to_color):
        """Sets the to_color of this ColorChangeEffect.

        Color which will replace.  # noqa: E501

        :param to_color: The to_color of this ColorChangeEffect.  # noqa: E501
        :type: str
        """
        self._to_color = to_color

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ColorChangeEffect):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
