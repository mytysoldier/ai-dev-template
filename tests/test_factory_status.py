import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/factory-status.py'


class FactoryStatusTest(unittest.TestCase):
    def run_with_gh(self, fake_gh):
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / 'gh'
            executable.write_text(fake_gh, encoding='utf-8')
            executable.chmod(0o755)
            env = os.environ.copy()
            env['PATH'] = directory + os.pathsep + env.get('PATH', '')
            return subprocess.run([sys.executable, str(SCRIPT), '1'], env=env, text=True, capture_output=True)

    def test_uses_github_state_instead_of_checkboxes(self):
        # Arrange
        fake_gh = '''#!/usr/bin/env python3
import json,sys
if sys.argv[1:3] == ['issue', 'view']:
 n=int(sys.argv[3]); print(json.dumps({'number':n,'title':'example','state':'CLOSED' if n == 2 else 'OPEN','url':'https://example.test/'+str(n),'body':'## 子Issueと進捗\\n- [ ] #2\\n- [x] #3\\n## 次\\n'}))
else:
 print(json.dumps([{'number':4,'title':'change','headRefName':'feature','url':'https://example.test/pr/4'}]))
'''
        # Act
        result = self.run_with_gh(fake_gh)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('子 #2 [CLOSED]', result.stdout)
        self.assertIn('子 #3 [OPEN]', result.stdout)
        self.assertIn('#4 feature', result.stdout)

    def test_github_error_fails_instead_of_reporting_completion(self):
        # Arrange
        fake_gh = '#!/bin/sh\necho network-failed >&2\nexit 1\n'
        # Act
        result = self.run_with_gh(fake_gh)
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('network-failed', result.stderr)


if __name__ == '__main__':
    unittest.main()
