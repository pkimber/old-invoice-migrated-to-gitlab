# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from decimal import Decimal

from reportlab import platypus
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


class MyReport(object):

    def __init__(self):
        # Use the sample style sheet.
        style_sheet = getSampleStyleSheet()
        self.body = style_sheet["BodyText"]
        self.head_1 = style_sheet["Heading1"]
        self.head_2 = style_sheet["Heading2"]
        self.GRID_LINE_WIDTH = 0.25

    def _bold(self, text):
        return self._para('<b>{}</b>'.format(text))

    def _head(self, text):
        return platypus.Paragraph(text, self.head_2)

    def _image(self, file_name):
        return platypus.Image(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'static',
            file_name
        ))

    def _para(self, text):
        return platypus.Paragraph(text, self.body)

    def _round(self, value):
        return value.quantize(Decimal('.01'))


class NumberedCanvas(canvas.Canvas):
    """
    Copied from ActiveState, Improved ReportLab recipe for page x of y
    http://code.activestate.com/recipes/576832/
    """

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 7)
        self.drawRightString(
            200 * mm,
            20 * mm,
            "Page %d of %d" % (self._pageNumber, page_count)
        )
