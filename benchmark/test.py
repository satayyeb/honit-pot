import unittest
import time

from benchmark.llm import LocalLLMApi


class BenchmarkTestResult(unittest.TextTestResult):
    def __init__(self, *args, model_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = model_name
        self.start_time = None
        self.end_time = None
        self.failures_with_model = []
        self.metrics = {}

    def startTestRun(self):
        self.start_time = time.time()
        super().startTestRun()

    def stopTestRun(self):
        self.end_time = time.time()
        elapsed = time.time() - self.start_time
        total = self.testsRun
        failed = len(self.failures) + len(self.errors)
        passed = total - failed
        percent = (passed / total * 100) if total else 0

        self.metrics = {
            'total': total,
            'passed': passed,
            'failed': failed,
            'pass_rate': percent,
            'elapsed_time': elapsed,
        }

        super().stopTestRun()
        self._log_failures()

    def addFailure(self, test, err):
        super().addFailure(test, err)
        # Save failed test info
        self.failures_with_model.append((test, self._exc_info_to_string(err, test)))

    def _log_failures(self):
        if not self.failures_with_model:
            return
        with open(f"failed_tests/failed_tests_{self.model_name.replace('/', '-')}.log", "w") as f:
            for test, traceback in self.failures_with_model:
                f.write(f"[{self.model_name}] {test.id()}\n")
                f.write(traceback + "\n\n")


class BenchmarkTestRunner(unittest.TextTestRunner):

    def __init__(self, *args, model_name=None, **kwargs):
        super().__init__(*args, resultclass=self._make_resultclass(model_name), **kwargs)

    def _make_resultclass(self, model_name):
        def _resultclass(*args, **kwargs):
            return BenchmarkTestResult(*args, model_name=model_name, **kwargs)

        return _resultclass


class HoneypotTestCase(unittest.TestCase):

    def __init__(self, model_name: str, methodName="runTest"):
        self.model_name = model_name
        super().__init__(methodName)

    def setUp(self):
        self.llm = LocalLLMApi(self.model_name)
