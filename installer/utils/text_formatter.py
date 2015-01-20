from xc_testcase import TestCase
from result_formatter import ResultFormatterBase
from meta_line import MetaLine

class TextResultFormatter(ResultFormatterBase):

  file_extension = "txt"

  def format_result(self, test_cases):
    lines = ["Testsuite:\n",
             "----------\n"]

    num_fail = 0
    num_pass = 0
    sum_duration = 0

    for tc in test_cases:
      duration = 0
      err_log = ""
      for ml in tc.output:
        if ml.prefix == "Duration":
          duration = float(ml.body)
        elif ml.prefix == "Fail" or ml.prefix == "Error":
          err_log += "{0}: {1}".format(ml.prefix, ml.body)

      if tc.result:
        num_pass += 1
        result = "Pass"
      else:
        num_fail += 1
        result = "Fail"
      sum_duration += duration

      lines += ["{0}: {1} ({2}s)\n".format(result, tc.file_name, duration)]

    lines += ["Summary: failed: {0}, passed: {1}, total: {2}, time: {3}".format(num_fail, num_pass, (num_fail + num_pass), sum_duration)]

    return lines

