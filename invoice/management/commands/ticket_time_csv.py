# -*- encoding: utf-8 -*-
import csv
import os
import datetime


from django.core.management.base import BaseCommand

from invoice.models import TimeRecord


class Command(BaseCommand):

    help = "Export ticket time to a CSV file"

    """ def _jobs_board_tickets(self):
        return (
            732,
            746,
            747,
            748,
            749,
            750,
            751,
            752,
            753,
            754,
            755,
            756,
            757,
            758,
            759,
            906,
            976,
        )

    def _payment_plan_tickets(self):
        return (
            644,
        )
    """

    def _navigator_tickets(self):
        return (
            1393,
            1377,
            1525,
            1662,
            1832,
            1834,
            1780,
            1651,
            1719,
            1498,
            1585,
            1595,
            1722,
            1549,
            1550,
            1592,
            1734,
            1737,
            1770,
            1798,
            1544,
            1552,
            1652,
            1666,
            1669,
            1833,
            1467,
            1469,
            1610,
            1611,
            1624,
            1634,
            1650,
            1835,
            1771,
            1782,
            1789,
            1785,
            1772,
            1781,
            1665,
            1727,
            1609,
            1726,
            1508,
            1723,
            1720,
            1692,
            1710,
            1713,
            1711,
            1696,
            1708,
            1712,
            1709,
            1707,
            1700,
            1695,
            1694,
            1693,
            1667,
            1608,
            1670,
            1672,
            1671,
            1668,
            1661,
            1660,
            1659,
            1599,
            1647,
            1645,
            1646,
            1644,
            1497,
            1629,
            1607,
            1518,
            1632,
            1620,
            1621,
            1594,
            1623,
            1591,
            1635,
            1615,
            1619,
            1606,
            1602,
            1590,
            1487,
            1570,
            1572,
            1571,
            1573,
            1567,
            1553,
            1551,
            1533,
            1524,
            1504,
            1545,
            1538,
            1520,
            1507,
            1494,
            1534,
            1539,
            1532,
            1531,
            1486,
            1522,
            1537,
            1527,
            1528,
            1495,
            1496,
            1473,
            1483,
            1485,
            1484,
            1481,
            1471,
            1478,
            1476,
            1477,
            1474,
            1464,
            1466,
            1465,
            1463,
            1470,
        )

    def handle(self, *args, **options):
        """Export ticket time to a CSV file.

        Columns:

        - ticket number
        - user name
        - billable - True or False
        - date started
        - minutes

        """
        #Enter job name:
        job_name = 'navigator'

        #Leave line below in as default
        tickets = [1100]

        #Uncomment your seloected model
        # tickets = self._jobs_board_tickets()
        # tickets = self._payment_plan_tickets()

        tickets = self._navigator_tickets()

        tickets = list(tickets)
        tickets.sort()

        file_name = '{}_{:%Y%m%d_%H%M%S}_ticket_time.csv'.format(job_name, datetime.datetime.now())
        print(file_name)
        if os.path.exists(file_name):
            raise Exception(
                "Export file, '{}', already exists.  "
                "Cannot export time.".format(file_name)
            )
        with open(file_name, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, dialect='excel-tab')
            for tr in TimeRecord.objects.filter(ticket__pk__in=tickets):
                print(tr.ticket.pk)
                csv_writer.writerow([
                    tr.ticket.pk,
                    tr.user.username,
                    tr.billable,
                    tr.has_invoice_line,
                    tr.date_started,
                    tr.minutes,
                ])
        print("Exported time to {}".format(file_name))
