# --------------------------------------------------------------------------------------------------
# Copyright (c) Lukas Vik. All rights reserved.
#
# This file is part of the tsfpga project, a project platform for modern FPGA development.
# https://tsfpga.com
# https://gitlab.com/tsfpga/tsfpga
# --------------------------------------------------------------------------------------------------

# Standard libraries
import re
from collections import OrderedDict


class HierarchicalUtilizationParser:

    """
    Used for parsing the ``report_utilization -hierarchical`` report generated by Vivado.
    """

    @staticmethod
    def get_size(report):
        """
        Takes a hierarchical utilization report as a string and returns the top level size
        for the specified run.

        Arguments:
            report (str): A string containing the entire Vivado hierarchical utilization report.
        """
        lines = report.split("\n")
        for idx, line in enumerate(lines):
            # Find the table line that is the top level
            if re.search(r"\(top\)", line):
                # Parse the report, remove uninteresting fields and create dictionary
                # Note that "|" is the column separator. Heading titles for the data is two lines
                # above the row for the top level.
                headers = [column_data.strip() for column_data in lines[idx - 2].split("|")]
                numbers = [column_data.strip() for column_data in line.split("|")]
                # The first columns contain entity name, etc. We only want the numbers
                headers = headers[3:-1]
                numbers = numbers[3:-1]
                # Convert numbers from string to integers
                numbers = [int(number) for number in numbers]
                return OrderedDict(zip(headers, numbers))

        return {}
