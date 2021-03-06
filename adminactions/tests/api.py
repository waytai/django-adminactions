# -*- encoding: utf-8 -*-
import unicodecsv as csv
import unittest
import xlrd
from django.contrib.auth.models import Permission
from django.test import TestCase
from adminactions.api import export_as_csv, export_as_xls
import StringIO
from collections import namedtuple


class TestExportQuerySetAsCsv(TestCase):
    def test_queryset_values(self):
        fields = ['codename', 'content_type__app_label']
        header = ['Name', 'Application']
        qs = Permission.objects.filter(codename='add_user').values('codename', 'content_type__app_label')
        mem = StringIO.StringIO()
        export_as_csv(queryset=qs, fields=fields, header=header, out=mem)
        mem.seek(0)
        csv_dump = mem.read()
        self.assertEquals(csv_dump.decode('utf8'), u'"Name";"Application"\r\n"add_user";"auth"\r\n')

    def test_callable_method(self):
        fields = ['codename', 'natural_key']
        qs = Permission.objects.filter(codename='add_user')
        mem = StringIO.StringIO()
        export_as_csv(queryset=qs, fields=fields, out=mem)
        mem.seek(0)
        csv_dump = mem.read()
        self.assertEquals(csv_dump.decode('utf8'), u'"add_user";"(u\'add_user\', u\'auth\', u\'user\')"\r\n')


class TestExportAsCsv(unittest.TestCase):
    def test_export_as_csv(self):
        fields = ['field1', 'field2']
        header = ['Field 1', 'Field 2']
        Row = namedtuple('Row', fields)
        rows = [Row(1, 4),
                Row(2, 5),
                Row(3, u'ӼӳӬԖԊ')]
        mem = StringIO.StringIO()
        export_as_csv(queryset=rows, fields=fields, header=header, out=mem)
        mem.seek(0)
        csv_dump = mem.read()
        self.assertEquals(csv_dump.decode('utf8'), u'"Field 1";"Field 2"\r\n"1";"4"\r\n"2";"5"\r\n"3";"ӼӳӬԖԊ"\r\n')


class TestExportAsExcel(unittest.TestCase):
    def test_export_as_xls(self):
        fields = ['field1', 'field2']
        header = ['Field 1', 'Field 2']
        Row = namedtuple('Row', fields)
        rows = [Row(111, 222),
                Row(333, 444),
                Row(555, u'ӼӳӬԖԊ')]
        mem = StringIO.StringIO()
        export_as_xls(queryset=rows, fields=fields, header=header, out=mem)
        mem.seek(0)
        xls_workbook = xlrd.open_workbook(file_contents=mem.read())
        xls_sheet = xls_workbook.sheet_by_index(0)
        self.assertEqual(xls_sheet.row_values(0)[:], ['#', 'Field 1', 'Field 2'])
        self.assertEqual(xls_sheet.row_values(1)[:], [1.0, 111.0, 222.0])
        self.assertEqual(xls_sheet.row_values(2)[:], [2.0, 333.0, 444.0])
        self.assertEqual(xls_sheet.row_values(3)[:], [3.0, 555.0, u'ӼӳӬԖԊ'])


class TestExportQuerySetAsExcel(TestCase):
    def test_queryset_values(self):
        fields = ['codename', 'content_type__app_label']
        header = ['Name', 'Application']
        qs = Permission.objects.filter(codename='add_user').values('codename', 'content_type__app_label')
        mem = StringIO.StringIO()
        export_as_xls(queryset=qs, fields=fields, header=header, out=mem)
        mem.seek(0)
        w = xlrd.open_workbook(file_contents=mem.read())
        sheet = w.sheet_by_index(0)
        self.assertEquals(sheet.cell_value(1,1), u'add_user')
        self.assertEquals(sheet.cell_value(1,2), u'auth')

    def test_callable_method(self):
        fields = ['codename', 'natural_key']
        qs = Permission.objects.filter(codename='add_user')
        mem = StringIO.StringIO()
        export_as_xls(queryset=qs, fields=fields, out=mem)
        mem.seek(0)
        w = xlrd.open_workbook(file_contents=mem.read())
        sheet = w.sheet_by_index(0)
        self.assertEquals(sheet.cell_value(1,1), u'add_user')
        self.assertEquals(sheet.cell_value(1,2), u'add_userauthuser')
