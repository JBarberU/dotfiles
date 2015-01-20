from log import Log
from xc_testcase import TestCase
from result_formatter import ResultFormatterBase
from colors import Colors

class CommandlineResultFormatter(ResultFormatterBase):

    def format_result(self, test_cases):
      for tc in test_cases:
        if tc.result:
          Log.print_msg("Pass", tc.file_name, Colors.GREEN)
        else:
          Log.print_msg("Fail", tc.file_name, Colors.RED)

