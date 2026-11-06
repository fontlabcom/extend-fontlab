# this_file: tests_docs/test_publish.py
"""Exercise publishing against owned local Git remotes; no live API writes."""
import json
import os
import shlex
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GIT = shutil.which('git')


class PublishTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.repo = self.folder / 'repo'
        self.remote = self.folder / 'remote.git'
        self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1')
        self.env.pop('GIT_INDEX_FILE', None)
        subprocess.run([GIT, 'init', '--bare', str(self.remote)], check=True, capture_output=True)
        subprocess.run([GIT, 'init', '-b', 'main', str(self.repo)], check=True, capture_output=True)
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        (self.repo / 'docs').mkdir()
        (self.repo / 'docs/index.html').write_text('old')
        (self.repo / 'source.txt').write_text('source')
        self.git('add', '.')
        self.git('commit', '-m', 'fixture')
        self.git('remote', 'add', 'origin', str(self.remote))
        self.git('push', 'origin', 'HEAD:main')
        self.sha = self.git('rev-parse', 'HEAD').strip()
        self.env['GITHUB_OUTPUT'] = str(self.folder / 'output')
        self.env['GITHUB_REPOSITORY'] = 'fixture/extend'
        bindir = self.folder / 'bin'
        bindir.mkdir()
        gh = bindir / 'gh'
        gh.write_text('''#!/bin/sh
case "$*" in
  *git/ref/heads/main*) git ls-remote origin refs/heads/main | cut -f1 ;;
  *pages/builds*)
    printf '%s\\n' 'POST' >> "$API_LOG"
    if test -n "${POST_DRIFT_SHA:-}"; then
      git --git-dir="$DRIFT_REMOTE" fetch "$DRIFT_SOURCE" "$POST_DRIFT_SHA:refs/heads/main"
    fi
    exit "${POST_EXIT:-0}" ;;
  *pages*) printf '%s\\n' "$PAGES_SETTINGS" ;;
  *) printf '%s\\n' "${DEFAULT_BRANCH:-main}" ;;
esac
''')
        gh.chmod(0o755)
        self.env['PATH'] = str(bindir) + os.pathsep + self.env['PATH']
        self.env['API_LOG'] = str(self.folder / 'api.log')
        self.env['PAGES_SETTINGS'] = json.dumps({'build_type': 'legacy', 'source': {'branch': 'main', 'path': '/docs'}})

    def git(self, *args):
        return subprocess.check_output([GIT, '-C', str(self.repo), *args], env=self.env, text=True, stderr=subprocess.STDOUT)

    def run_script(self, name, sha=None):
        return subprocess.run(['sh', str(ROOT / 'src_docs' / name), sha or self.sha], cwd=self.repo, env=self.env, text=True, capture_output=True, check=False)

    def test_changed_docs_commit_only_output_and_preserve_source(self):
        (self.repo / 'docs/index.html').write_text('new')
        (self.repo / 'source.txt').write_text('uncommitted owner data')
        result = self.run_script('publish.sh')
        self.assertEqual(result.returncode, 0, result.stderr)
        current = self.git('rev-parse', 'HEAD').strip()
        self.assertNotEqual(current, self.sha)
        self.assertEqual(self.git('diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD').strip(), 'docs/index.html')
        self.assertEqual(self.git('show', 'HEAD:source.txt'), 'source')
        self.assertEqual((self.repo / 'source.txt').read_text(), 'uncommitted owner data')
        self.assertEqual((self.folder / 'output').read_text(), f'sha={current}\n')
        self.assertIn(current, self.git('ls-remote', 'origin', 'refs/heads/main'))

    def test_unchanged_docs_keep_existing_commit(self):
        result = self.run_script('publish.sh')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git('rev-parse', 'HEAD').strip(), self.sha)
        self.assertEqual((self.folder / 'output').read_text(), f'sha={self.sha}\n')

    def test_superseded_source_does_not_commit_or_emit_output(self):
        self.git('commit', '--allow-empty', '-m', 'new source')
        self.git('push', 'origin', 'HEAD:main')
        self.git('checkout', self.sha)
        (self.repo / 'docs/index.html').write_text('old run')
        result = self.run_script('publish.sh')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('superseded', result.stdout)
        self.assertFalse((self.folder / 'output').exists())
        self.assertEqual(self.git('rev-parse', 'HEAD').strip(), self.sha)

    def test_wrong_checkout_and_preexisting_staged_data_fail(self):
        result = self.run_script('publish.sh', '0' * 40)
        self.assertNotEqual(result.returncode, 0)
        (self.repo / 'source.txt').write_text('staged owner data')
        self.git('add', 'source.txt')
        result = self.run_script('publish.sh')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git('diff', '--cached', '--name-only').strip(), 'source.txt')

    def test_push_rejection_is_failure_and_does_not_emit_output(self):
        hook = self.remote / 'hooks/pre-receive'
        hook.write_text('#!/bin/sh\nexit 1\n')
        hook.chmod(0o755)
        (self.repo / 'docs/index.html').write_text('new')
        result = self.run_script('publish.sh')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.folder / 'output').exists())
        self.assertIn(self.sha, self.git('ls-remote', 'origin', 'refs/heads/main'))

    def test_qualified_current_head_requests_pages(self):
        result = self.run_script('request-pages.sh')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.folder / 'api.log').read_text(), 'POST\n')

    def test_wrong_default_or_pages_source_never_posts(self):
        for default, settings in [('master', self.env['PAGES_SETTINGS']), ('main', '{"build_type":"workflow","source":{"branch":"main","path":"/docs"}}'), ('main', '{"build_type":"legacy","source":{"branch":"main","path":"/"}}')]:
            with self.subTest(default=default, settings=settings):
                self.env.update(DEFAULT_BRANCH=default, PAGES_SETTINGS=settings)
                result = self.run_script('request-pages.sh')
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((self.folder / 'api.log').exists())

    def test_pages_permission_failure_propagates(self):
        self.env['POST_EXIT'] = '1'
        result = self.run_script('request-pages.sh')
        self.assertNotEqual(result.returncode, 0)

    def test_superseded_pages_request_never_posts(self):
        self.git('commit', '--allow-empty', '-m', 'new source')
        self.git('push', 'origin', 'HEAD:main')
        self.git('checkout', self.sha)
        result = self.run_script('request-pages.sh')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('superseded', result.stdout)
        self.assertFalse((self.folder / 'api.log').exists())

    def test_competing_commit_between_guard_and_push_is_preserved(self):
        tree = self.git('rev-parse', 'HEAD^{tree}').strip()
        concurrent = self.git('commit-tree', tree, '-p', self.sha, '-m', 'concurrent owner').strip()
        hook = self.repo / '.git/hooks/pre-push'
        command = [GIT, '--git-dir=' + str(self.remote), 'fetch', str(self.repo), concurrent + ':refs/heads/main']
        hook.write_text('#!/bin/sh\n' + shlex.join(command) + '\n')
        hook.chmod(0o755)
        (self.repo / 'docs/index.html').write_text('racing output')
        result = self.run_script('publish.sh')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.folder / 'output').exists())
        self.assertIn(concurrent, self.git('ls-remote', 'origin', 'refs/heads/main'))

    def test_main_drift_during_pages_request_is_reported_as_failure(self):
        tree = self.git('rev-parse', 'HEAD^{tree}').strip()
        concurrent = self.git('commit-tree', tree, '-p', self.sha, '-m', 'concurrent owner').strip()
        self.env.update(POST_DRIFT_SHA=concurrent, DRIFT_REMOTE=str(self.remote), DRIFT_SOURCE=str(self.repo))
        result = self.run_script('request-pages.sh')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.folder / 'api.log').read_text(), 'POST\n')
        self.assertIn(concurrent, self.git('ls-remote', 'origin', 'refs/heads/main'))

    def test_unreachable_origin_fails_without_commit_output_or_staging(self):
        self.git('remote', 'set-url', 'origin', str(self.folder / 'absent.git'))
        (self.repo / 'docs/index.html').write_text('new output')
        result = self.run_script('publish.sh')
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertFalse((self.folder / 'output').exists())
        self.assertEqual(self.git('rev-parse', 'HEAD').strip(), self.sha)
        self.assertEqual(self.git('diff', '--cached', '--name-only'), '')

    def test_remote_missing_main_fails_without_commit_output_or_staging(self):
        subprocess.run([GIT, '--git-dir=' + str(self.remote), 'update-ref', '-d', 'refs/heads/main'], check=True)
        (self.repo / 'docs/index.html').write_text('new output')
        result = self.run_script('publish.sh')
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertFalse((self.folder / 'output').exists())
        self.assertEqual(self.git('rev-parse', 'HEAD').strip(), self.sha)
        self.assertEqual(self.git('diff', '--cached', '--name-only'), '')
