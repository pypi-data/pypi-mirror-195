'''
This module performs unit tests on the Pioneer REST API

Usage:
  api_tests.py [--authlegacy=<bool>] [--user=<str>] [--pass=<str>] [--appkey=<str>] [--wksp=<str>]
  api_tests.py (-h | --help)

Examples:
  api_tests.py --user=username --pass=secret
  api_tests.py --user=username --appkey=op_guid --wksp=sqa

Options:
  -h, --help
  -a, --authlegacy=<bool>  true for legacy username password method [default: False]
  -u, --user=<str>         API user [default:]
  -p, --pass=<str>         API password [default:]
  -k, --appkey=<str>       non expiring auth key [default:]
  -w, --wksp=<str>         wksp to use [default: Studio]
'''

import api
import os
import time
import unittest
from contextlib import redirect_stderr, redirect_stdout
from dateutil.parser import parse
from datetime import date, datetime, timedelta
from docopt import docopt
from io import StringIO
from json import dumps, loads
from random import randint
from sys import platform
from typing import Tuple, Optional
from uuid import uuid4


class TestApi(unittest.TestCase):
    '''A series of Pioneer REST API unit tests

    OVERRIDE
    docopt configuration passed into the module will override the default static members

    STATIC MEMBERS
    USERNAME    required to be issued api key
    USERPASS    required to be issued api key
    WORKSPACE   defines what storage account to use for IO operations
    APPKEY      non expiring authentication key
    AUTH_LEGACY true for legacy username password authentication method
    '''

    USERNAME: Optional[str] = None
    USERPASS: Optional[str] = None
    WORKSPACE: str = 'Studio'
    APPKEY: Optional[str] = None
    AUTH_LEGACY: bool = False

    # method execution order - unittest.TestLoader.sortTestMethodsUsing
    # default string sort of class method names startswith test_{method-name}, ie dir(self)

    @classmethod
    def setUpClass(cls) -> None:
        '''called before test methods are ran
        ensure cache directories and test data inputs are available in target wksp
        '''

        cls.API = api.Api(
            auth_legacy=TestApi.AUTH_LEGACY,
            appkey=TestApi.APPKEY,
            un=TestApi.USERNAME,
            pw=TestApi.USERPASS,
        )
        cls.API.debug_requests = False

        # directory references
        cls.dir_local_current: str = os.path.dirname(__file__)
        cls.dir_testdata_local: str = os.path.join(cls.dir_local_current, 'quick_tests')
        assert os.path.exists(cls.dir_testdata_local)
        assert len(os.listdir(cls.dir_testdata_local)) >= 1
        cls.dir_testdata_remote: str = 'quick_tests'
        cls.files_testdata_local: list[str] = []
        cls.files_testdata_remote: list[str] = []
        cls.py_run_me: str = ''
        cls.py_run_me_quick: str = ''

        # get all directories from wksp
        resp = cls.API.wksp_files(cls.WORKSPACE, '/quick_tests/')
        files_remote: list[str] = [f['filePath'] for f in resp['files']]

        # comb over local test data and map to destination file structure
        for f in os.listdir(cls.dir_testdata_local):
            local: str = os.path.join(cls.dir_testdata_local, f)
            if os.path.isfile(local) is False:
                continue
            elif os.path.getsize(local) == 0:
                continue
            dest: str = os.path.join(cls.dir_testdata_remote, f)
            cls.files_testdata_local.append(local)
            cls.files_testdata_remote.append(dest)
            if dest.endswith('sleep.py'):
                cls.py_run_me = dest
            elif dest.endswith('quick.py'):
                cls.py_run_me_quick = dest

            # upload local test data to destination
            for idx, local in enumerate(cls.files_testdata_local):
                dest = cls.files_testdata_remote[idx]
            res: list[str] = [f for f in files_remote if dest in f]
            if len(res) == 0:
                print(f'uploading {dest}')
                resp = cls.API.wksp_file_upload(
                    cls.WORKSPACE, file_path_dest=dest, file_path_local=local
                )

    def date_isoformat(self, date_str: str) -> bool:
        '''is date string isoformat'''

        d: date
        try:
            d = date.fromisoformat(date_str)
            return isinstance(d, date)
        except ValueError:
            return False

    def test_000_init_api_version_bad(self) -> None:
        '''recover from a bad api version provided'''

        bad_version: int = 99

        with redirect_stderr(StringIO()) as err:
            a = api.Api(auth_legacy=TestApi.AUTH_LEGACY, version=bad_version)
            output: str = err.getvalue().strip()

        self.assertGreater(output.find(f'API version {bad_version} not supported'), -1)
        self.assertRegex(a.api_version, r'app/v0/')

    def test_000_init_password_missing(self) -> None:
        '''get password uses a secret stream and input will not echo'''

        if platform != 'linux':
            self.skipTest('only linux has timed inputs')

        with redirect_stdout(StringIO()) as out:
            try:
                a = api.Api(auth_legacy=True, un=TestApi.USERNAME)
            except (EOFError, TimeoutError):
                pass
            output: str = out.getvalue().strip()

        self.assertEqual(output.find('REQUIRED API User Password'), -1)

    def test_000_prereqs(self) -> None:
        '''ensure job data is available to test against'''

        self.API.wksp_job_start(self.WORKSPACE, self.py_run_me_quick, tags='unittest_preseed')
        stime: float = time.time()
        print('Pre-seeding by running a new job')
        res: bool = self.API.util_job_monitor(
            self.WORKSPACE, self.API._job_start_recent_key, stop_when='done', secs_max=300
        )
        delta: float = time.time() - stime
        print(f'Job completed {res}, time spent {delta}')
        self.assertLessEqual(delta, 180.0)

    def test_auth_apikey(self) -> None:
        '''api key is required for all api calls with legacy authentication'''

        self.assertIsNotNone(
            self.API.auth_apikey
        ) if self.API.auth_method_legacy else self.assertIsNone(self.API.auth_apikey)

    def test_auth_apikey_expiration(self) -> None:
        '''ensure api key is refreshed and not expired'''

        if self.API.auth_method_legacy:
            self.assertGreater(self.API.auth_apikey_expiry, datetime.now().timestamp())
        else:
            self.assertEqual(self.API.auth_apikey_expiry, 0)

    def test_auth_header(self) -> None:
        '''request header must have valid apikey or appkey'''

        if self.AUTH_LEGACY:
            self.assertEqual(self.API.auth_req_header['x-api-key'], self.API.auth_apikey)
        else:
            self.assertEqual(self.API.auth_req_header['x-app-key'], self.API.auth_appkey)

    def test_account_info(self) -> None:
        '''account properties'''

        resp = self.API.account_info()
        self.assertEqual(resp['result'], 'success')
        if self.API.auth_username:
            self.assertEqual(resp['username'], self.API.auth_username)
        else:
            self.assertIsInstance(resp['username'], str)
        self.assertGreaterEqual(resp['apiConcurrentSolvesMax'], 1)
        self.assertGreaterEqual(resp['workspaceCount'], 1)

    def test_account_summary(self) -> None:
        '''aggregated account information'''

        d: dict = self.API._account_summary()
        self.assertIsInstance(d['API DOMAIN'], str)
        self.assertIsInstance(d['API USERNAME'], str)
        self.assertIsInstance(d['API AUTH METHOD LEGACY'], bool)
        self.assertIsInstance(d['JOB MAX CONCURRENCY'], int)
        self.assertIsInstance(d['JOB HISTORY TOTAL'], int)
        self.assertIsInstance(d['JOB ACTIVE'], int)
        self.assertIsInstance(d['DATABASE'], int)
        self.assertIsInstance(d['WORKSPACE'], int)
        self.assertIsInstance(d['DISK SSD'], int)
        if self.API.auth_method_legacy:
            self.assertIsInstance(d['API KEY MINS LEFT'], float)

    def test_account_jobs(self) -> None:
        ''' 'any user job from any workspace'''

        job_count: int = 50
        resp = self.API._account_jobs(max_jobs=job_count)
        self.assertIsInstance(resp['jobs'], list)
        self.assertIsInstance(resp['result'], str)
        self.assertIsInstance(resp['subsetCount'], int)
        self.assertIsInstance(resp['totalCount'], int)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['subsetCount'], job_count)
        for job in resp['jobs']:
            self.assertIsInstance(job['canHaveResult'], bool)
            self.assertIsInstance(job['jobInfo'], dict)
            self.assertIsInstance(job['jobInfo']['command'], str)
            if job['jobInfo']['command'] != 'run_custom':
                self.assertIsInstance(job['jobInfo']['directoryPath'], str)
                self.assertIsInstance(job['jobInfo']['filename'], str)
            self.assertIsInstance(job['jobInfo']['resourceConfig'], dict)
            self.assertIsInstance(job['jobInfo']['resourceConfig']['cpu'], str)
            self.assertIsInstance(job['jobInfo']['resourceConfig']['name'], str)
            self.assertIsInstance(job['jobInfo']['resourceConfig']['ram'], str)
            self.assertIsInstance(
                float(job['jobInfo']['resourceConfig']['run_rate']), float
            )  # BUG OE-6710 float or int
            self.assertIsInstance(job['jobInfo']['tags'], str)
            self.assertIsInstance(int(job['jobInfo']['timeout']), int)  # BUG OE-6710 str or int
            self.assertIsInstance(job['jobInfo']['workspace'], str)
            self.assertIsInstance(job['jobKey'], str)
            self.assertIsInstance(float(job['runRate']), float)  # BUG OE-6710 float or int
            self.assertIsInstance(job['status'], str)
            self.assertIsInstance(job['submittedDatetime'], str)
            self.assertIsInstance(job['submittedTimeStamp'], int)

            if job['status'] in ('done', 'cancelled', 'error'):
                self.assertTrue(job['canHaveResult'])
                self.assertIsInstance(job['billedTime'], str)
                self.assertIsInstance(float(job['billedTimeMs']), float)  # BUG OE-6710 float or int
                self.assertIsInstance(job['endDatetime'], str)
                self.assertIsInstance(job['endTimeStamp'], int)
                self.assertIsInstance(job['runTime'], str)
                self.assertIsInstance(job['runTimeMs'], int)
                self.assertIsInstance(job['startDatetime'], str)
                self.assertIsInstance(job['startTimeStamp'], int)
            else:
                # self.assertFalse(job['canHaveResult']) # BUG OE-6710 stopped cant have a result
                pass

    def test_account_jobs_active(self) -> None:
        '''compare active account jobs count to all active wksp jobs'''

        start_new_job: bool = bool(randint(0, 1))
        if start_new_job:
            self.API.wksp_job_start(self.WORKSPACE, self.py_run_me, tags='unittest_jobs_active')

        active_account: int = 0
        resp = self.API._account_jobs(
            max_jobs=200
        )  # BUG submitted counts as active therefore must account for excessive submitted jobs
        for job in resp['jobs']:
            if job['status'] in self.API.JOBSTATES_ACTIVE:
                active_account += 1

        active_wksp: int = self.API._jobs_active
        self.assertEqual(active_account, active_wksp)
        if start_new_job:
            self.assertGreater(active_account, 0)
            self.assertGreater(active_wksp, 0)

    def test_account_storage_devices(self) -> None:
        '''get a list of available storage devices in an account'''

        resp = self.API.account_storage_devices()
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)
        self.assertGreaterEqual(resp['count'], 1)
        self.assertIsInstance(resp['storages'], list)
        with self.subTest():
            for d in resp['storages']:
                if d['type'] == 'azure_afs':
                    self.assertEqual(len(d), 11)
                    self.assertIsInstance(d['bytesUsed'], int)
                    self.assertIsInstance(d['capacity'], int)
                    self.assertIsInstance(d['created'], int)
                    self.assertTrue(d['description'] is None or isinstance(d['description'], str))
                    self.assertIsInstance(d['id'], str)
                    self.assertIsInstance(d['internal'], bool)
                    self.assertTrue(
                        d['lockoutReason'] is None or isinstance(d['lockoutReason'], str)
                    )
                    self.assertIsInstance(d['name'], str)
                    self.assertIsInstance(d['tier'], str)
                    self.assertIsInstance(d['type'], str)
                    self.assertIsInstance(d['updated'], int)
                if d['type'] == 'azure_workspace':
                    self.assertEqual(len(d), 12)
                    self.assertIsInstance(d['bytesUsed'], int)
                    self.assertIsInstance(d['capacity'], int)
                    self.assertIsInstance(d['created'], int)
                    self.assertTrue(d['description'] is None or isinstance(d['description'], str))
                    self.assertIsInstance(d['id'], str)
                    self.assertIsInstance(d['internal'], bool)
                    self.assertTrue(
                        d['lockoutReason'] is None or isinstance(d['lockoutReason'], str)
                    )
                    self.assertIsInstance(d['name'], str)
                    self.assertIsInstance(d['tier'], str)
                    self.assertIsInstance(d['type'], str)
                    self.assertIsInstance(d['updated'], int)
                    self.assertIsInstance(d['workspaceKey'], str)
                elif d['type'] == 'onedrive':
                    self.assertEqual(len(d), 18)
                    self.assertIsInstance(d['accountName'], str)
                    self.assertIsInstance(d['authenticated'], int)
                    self.assertTrue(d['bytesUsed'] is None or isinstance(d['bytesUsed'], int))
                    self.assertIsInstance(d['capacity'], int)
                    self.assertIsInstance(d['created'], int)
                    self.assertTrue(d['description'] is None or isinstance(d['description'], str))
                    self.assertIsInstance(d['endpointSuffix'], str)
                    self.assertIsInstance(d['homeAccountId'], str)
                    self.assertIsInstance(d['id'], str)
                    self.assertIsInstance(d['internal'], bool)
                    self.assertTrue(
                        d['lockoutReason'] is None or isinstance(d['lockoutReason'], str)
                    )
                    self.assertIsInstance(d['name'], str)
                    self.assertIsInstance(d['protocol'], str)
                    self.assertIsInstance(d['tier'], str)
                    self.assertIsInstance(d['type'], str)
                    self.assertIsInstance(d['updated'], int)
                    self.assertIsInstance(d['username'], str)
                elif d['type'] == 'postgres_db':
                    self.assertEqual(len(d), 17)
                    self.assertTrue(d['bytesUsed'] is None or isinstance(d['bytesUsed'], int))
                    self.assertTrue(
                        d['bytesUsedLastUpdated'] is None
                        or isinstance(d['bytesUsedLastUpdated'], int)
                    )
                    self.assertIsInstance(d['created'], int)
                    self.assertIsInstance(d['dbname'], str)
                    self.assertTrue(d['description'] is None or isinstance(d['description'], str))
                    self.assertIsInstance(d['host'], str)
                    self.assertIsInstance(d['id'], str)
                    self.assertTrue(
                        d['lockoutReason'] is None or isinstance(d['lockoutReason'], str)
                    )
                    self.assertIsInstance(d['name'], str)
                    self.assertIsInstance(d['port'], int)
                    self.assertIsInstance(d['type'], str)
                    self.assertIsInstance(d['updated'], int)
                    self.assertIsInstance(d['user'], str)
                    self.assertIsInstance(d['defaultSchema'], str)
                    if d['defaultSchema'].startswith('anura_2_'):
                        self.assertIsInstance(d['schemaStatus'], str)
                        self.assertTrue(
                            d['schemaStatus'] in ('error', 'invalid', 'valid')
                            or len(d['schemaStatus']) == 0
                        )
                        self.assertTrue(
                            d['schemaStatusLastUpdated'] is None
                            or isinstance(d['schemaStatusLastUpdated'], float)
                        )
                        self.assertIsInstance(d['schemaVersion'], str)
                        self.assertRegex(d['schemaVersion'], r'2\.[4-9]\.\d+')
                    else:
                        self.assertEqual(d['defaultSchema'], '"$user"')
                        self.assertEqual(d['schemaStatus'], 'valid')
                        self.assertIsNone(d['schemaStatusLastUpdated'])
                        self.assertTrue(len(d['schemaVersion']) == 0)

    def test_account_usage(self) -> None:
        '''atlas and andromeda information'''

        resp = self.API._account_usage()
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['andromeda'], dict)
        self.assertIsInstance(resp['atlas'], dict)
        self.assertEqual(len(resp), 3)

        self.assertIsInstance(resp['andromeda']['jobsLastThirty'], int)
        self.assertIsInstance(resp['andromeda']['jobsMostRecent'], int)
        self.assertIsInstance(resp['andromeda']['jobsTimeLastThirty'], float)
        self.assertIsInstance(resp['andromeda']['jobsTimeTotal'], float)
        self.assertIsInstance(resp['andromeda']['jobsTotal'], int)
        self.assertIsInstance(resp['andromeda']['periodHours'], float)
        self.assertEqual(len(resp['andromeda']), 6)
        self.assertEqual(len(str(resp['andromeda']['jobsMostRecent'])), 13)
        dt: datetime = datetime.fromtimestamp(resp['andromeda']['jobsMostRecent'] / 1000)
        now: datetime = datetime.utcnow()
        self.assertEqual(dt.year, now.year)
        self.assertEqual(dt.month, now.month)

        self.assertIsInstance(resp['atlas'], dict)
        self.assertIsInstance(resp['atlas']['lastLogin'], int)
        self.assertIsInstance(resp['atlas']['periodHours'], float)
        self.assertIsInstance(resp['atlas']['task'], dict)
        self.assertIsInstance(resp['atlas']['workspaceCount'], int)
        self.assertEqual(len(resp['atlas']), 4)
        self.assertEqual(len(str(resp['atlas']['lastLogin'])), 13)
        dt: datetime = datetime.fromtimestamp(resp['atlas']['lastLogin'] / 1000)
        self.assertIsInstance(dt, datetime)

        self.assertIsInstance(resp['atlas']['task'], dict)
        if resp['atlas']['task']['durationCurrentWeek'] == 0:
            self.assertIsInstance(resp['atlas']['task']['durationCurrentWeek'], int)
        else:
            self.assertIsInstance(resp['atlas']['task']['durationCurrentWeek'], float)
        self.assertIsInstance(resp['atlas']['task']['durationLastThirty'], float)
        self.assertIsInstance(resp['atlas']['task']['durationTotal'], float)
        self.assertIsInstance(resp['atlas']['task']['lastDuration'], float)
        self.assertIsInstance(resp['atlas']['task']['lastRunStart'], int)
        self.assertIsInstance(resp['atlas']['task']['runCurrentWeek'], int)
        self.assertIsInstance(resp['atlas']['task']['runlastThirty'], int)
        self.assertIsInstance(resp['atlas']['task']['runTotal'], int)
        self.assertEqual(len(resp['atlas']['task']), 8)
        self.assertEqual(len(str(resp['atlas']['task']['lastRunStart'])), 13)
        dt: datetime = datetime.fromtimestamp(resp['atlas']['task']['lastRunStart'] / 1000)
        self.assertIsInstance(dt, datetime)

    def test_account_workspaces(self) -> None:
        '''check all workspaces properties'''

        resp = self.API.account_workspaces()
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)

        wksp_exists: bool = False
        for wksp in resp['workspaces']:
            self.assertRegex(wksp['name'], '^[\\w-]+$')
            self.assertEqual(len(wksp['key']), 25)
            self.assertIn(wksp['stack'], ['Optilogic', 'Gurobi'])
            self.assertIn(wksp['status'], ['STARTING', 'RUNNING', 'STOPPING', 'STOPPED'])
            self.assertRegex(wksp['status'], '\\w{3,}')

            # https://en.wikipedia.org/wiki/ISO_8601
            dt_wksp_creation: datetime = parse(wksp['createdon'])
            self.assertGreaterEqual(dt_wksp_creation.year, 2020)

            if wksp['name'] == self.WORKSPACE:
                wksp_exists = True

        self.assertTrue(wksp_exists)

    def test_account_workspace_count(self) -> None:
        '''account info and workspaces both return wksp count'''

        resp = self.API.account_info()
        ws_count: int = self.API.account_workspace_count
        self.assertEqual(resp['workspaceCount'], ws_count)

    @unittest.skip('cant delete a wksp atm')
    def test_account_workspace_create(self) -> None:
        '''creating a new workspace'''

        resp = self.API.account_workspace_create('delme')
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['name'], 'delme')
        self.assertEqual(resp['stack'], 'Gurobi')

    def test_account_workspace_create_crash(self) -> None:
        '''expected to not create the same workspace twice'''

        resp = self.API.account_workspace_create('Studio')
        self.assertEqual(resp['crash'], True)
        self.assertEqual(resp['exception'].response.status_code, 400)

    def test_account_workspace_delete(self):
        '''deleting a newly created workspace'''

        with self.assertRaises(NotImplementedError):
            resp = self.API.account_workspace_delete('delme')

    def test_api_server_online(self) -> None:
        '''check if api service is up and running'''

        self.assertTrue(self.API.api_server_online)

    def test_api_version(self) -> None:
        '''only version zero is supported'''

        self.assertTrue(self.API.api_version.endswith('v0/'))

    def test_database_create_delete(self) -> None:
        '''create a postgres database then delete'''

        # get the latest BOTS template, anura_2_{{n}}_blast_off_to_space
        bots: list[str] = [t for t in self.API.DATABASE_TEMPLATES if t.find('blast') > -1]
        bots = sorted(bots, reverse=True)
        dbname: str = f'pg_{time.perf_counter_ns()}'

        resp = self.API.database_create(dbname, desc=f'unittest {dbname}', template=bots[0])
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['storageId'], str)
        self.assertEqual(len(resp['storageId']), 36)

        resp = self.API.storage_delete(dbname)
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['result'], 'success')

    def test_database_create_delete_wrong_id(self) -> None:
        '''create a postgres database with a template name instead of id'''

        tname: str = 'Out of China'
        self.assertFalse(tname in self.API.DATABASE_TEMPLATES)
        dbname: str = f'pg_{time.perf_counter_ns()}'

        # create using an invalid template id
        resp = self.API.database_create(dbname, desc=f'unittest {dbname} {tname}', template=tname)
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['storageId'], str)
        self.assertEqual(len(resp['storageId']), 36)

        # verify template name fallback
        db = self.API.storage(dbname)
        self.assertEqual(db['result'], 'success')
        self.assertEqual(db['name'], dbname)
        self.assertEqual(db['type'], 'postgres_db')
        self.assertEqual(db['id'], resp['storageId'])
        self.assertGreater(db['description'].find(tname), -1)

        resp = self.API.storage_delete(dbname)
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['result'], 'success')

    def test_database_create_failure(self) -> None:
        '''attempt creating a postgres database with bad template id'''

        with self.assertRaises(AssertionError):
            self.API.database_create(name='cant', template='does_not_exist')

    def test_database_schemas(self) -> None:
        '''currently only anura schemas'''

        ANURA_STATUS: Tuple[str, ...] = ('current', 'deprecated', 'preview', 'retired')
        resp = self.API.database_schemas()
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['schemas'], dict)
        self.assertEqual(len(resp), 2)
        self.assertEqual(len(resp['schemas']), 1)
        self.assertTrue(resp['schemas'].get('anura', False))
        for schema_type in resp['schemas'].keys():
            for v in resp['schemas'][schema_type]:
                self.assertEqual(len(v), 10)
                self.assertIsInstance(v['generalAvailabilityDate'], str)
                self.assertIsInstance(v['description'], str)
                self.assertIsInstance(v['notes'], str)
                self.assertIsInstance(v['schemaName'], str)
                self.assertRegex(v['schemaName'], r'anura_2_[4-9]')
                self.assertIsInstance(v['schemaVersion'], str)
                self.assertRegex(v['schemaVersion'], r'2\.[4-9]\.\d+')
                self.assertIsInstance(v['status'], str)
                self.assertIn(v['status'], ANURA_STATUS)
                self.assertTrue(self.date_isoformat(v['generalAvailabilityDate']))
                if v.get('defaultMigrationDate'):
                    self.assertIsInstance(v['defaultMigrationDate'], str)
                    self.assertTrue(self.date_isoformat(v['defaultMigrationDate']))
                if v.get('endOfLifeDate'):
                    self.assertIsInstance(v['endOfLifeDate'], str)
                    self.assertTrue(self.date_isoformat(v['endOfLifeDate']))
                if v.get('limitedAvailabilityDate'):
                    self.assertIsInstance(v['limitedAvailabilityDate'], str)
                    self.assertTrue(self.date_isoformat(v['limitedAvailabilityDate']))
                if v.get('techPreviewDate'):
                    self.assertIsInstance(v['techPreviewDate'], str)
                    self.assertTrue(self.date_isoformat(v['techPreviewDate']))

    def test_database_tables(self) -> None:
        '''list of schemas and tables'''

        if self.API.storagetype_database_exists is False:
            self.skipTest('account does not have a postgres database')

        db = self.API.account_storage_device(type='postgres_db')
        resp = self.API.database_tables(db['name'])
        self.assertIsInstance(resp['result'], str)
        for schema in resp['schemas']:
            self.assertIsInstance(schema['name'], str)
            self.assertIsInstance(schema['tables'], int)
            self.assertIsInstance(schema['is_default_schema'], bool)
        self.assertIsInstance(resp['tables'], list)

        if len(resp['tables']) >= 1:
            self.assertIsInstance(resp['tables'][0]['name'], str)
            self.assertIsInstance(resp['tables'][0]['rows'], int)
            self.assertIsInstance(resp['tables'][0]['schema'], str)

    def test_database_tables_empty(self) -> None:
        '''clear the data in specified tables'''

        db: str = 'unittest_empty_bom_table'
        tbl: str = 'billsofmaterials'
        anura_versions: list[str] = sorted(
            {t[0:9] for t in self.API.DATABASE_TEMPLATES if t.find('anura') > -1}, reverse=True
        )
        schema: str = anura_versions[0]

        # assert db exists
        exists: bool = self.API.storagename_database_exists(db)
        if exists:
            resp = self.API.storage(db)
            schema = resp['defaultSchema']
        else:
            self.API.database_create(name=db, template=f'{schema}_blast_off_to_space')

        # assert db has data
        QUERY_ROWS: str = f'SELECT COUNT(*) FROM {schema}.{tbl}'
        resp = self.API.sql_query(db, QUERY_ROWS)
        rows: int = int(resp['queryResults'][0]['count'])
        if rows == 0:
            query_insert = f'INSERT INTO {schema}.{tbl}\n'
            query_insert += (
                '(bomname, productname, producttype, quantity, quantityuom, status, notes)\n'
            )
            query_insert += f"VALUES\n('Unittest', 'RM1', 'Component', '1', 'EA', 'Exclude', 'unittest{time.time()}')"
            self.API.sql_query(db, query_insert)
            rows = 1

        # remove table data dry run
        resp = self.API.database_tables_empty(db, tables=[tbl], dry_run=True)
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp), 4)
        self.assertTrue(resp['dryRun'])
        self.assertIsInstance(resp['emptied'], list)
        self.assertEqual(len(resp['emptied']), 1)
        self.assertEqual(resp['emptied'][0], f'{schema}.{tbl}')
        self.assertIsInstance(resp['failed'], list)
        self.assertEqual(len(resp['failed']), 0)
        resp = self.API.sql_query(db, QUERY_ROWS)
        rows_dry_run: int = int(resp['queryResults'][0]['count'])
        self.assertEqual(rows, rows_dry_run)

        # remove table data
        resp = self.API.database_tables_empty(db, tables=[tbl])
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp), 4)
        self.assertFalse(resp['dryRun'])
        self.assertIsInstance(resp['emptied'], list)
        self.assertEqual(len(resp['emptied']), 1)
        self.assertEqual(resp['emptied'][0], f'{schema}.{tbl}')
        self.assertIsInstance(resp['failed'], list)
        self.assertEqual(len(resp['failed']), 0)
        resp = self.API.sql_query(db, QUERY_ROWS)
        rows_cleared: int = int(resp['queryResults'][0]['count'])
        self.assertEqual(rows_cleared, 0)

    def test_database_templates(self) -> None:
        '''empty db or anura schemas'''

        resp = self.API.database_templates()
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)
        self.assertEqual(resp['count'], 12)
        self.assertIsInstance(resp['templates'], list)
        self.assertEqual(len(resp['templates']), 12)

        # self.assertTrue(t['id'] in self.API.DATABASE_TEMPLATES)
        TEMPLATE_KEYS: Tuple[str, ...] = ('id', 'name', 'schema', 'serverName')
        for t in resp['templates']:
            self.assertIsInstance(t, dict)
            for k in TEMPLATE_KEYS:
                self.assertIsInstance(t[k], str)

        TEMPLATES: list[dict] = [
            {
                'id': 'empty',
                'name': 'Empty Database',
                'role': '',
                'schema': '',
                'serverName': 'default',
            },
            {
                'id': 'anura_2_4_blast_off_to_space',
                'name': 'Anura - Blast off to Space (2.4)',
                'role': 'pioneer-team',
                'schema': 'anura_2_4',
                'serverName': 'default',
            },
            {
                'id': 'anura_2_4_clean',
                'name': 'Anura - New Model (2.4)',
                'role': 'pioneer-team',
                'schema': 'anura_2_4',
                'serverName': 'default',
            },
            {
                'id': 'anura_2_5_blast_off_to_space',
                'name': 'Anura - Blast off to Space',
                'role': '',
                'schema': 'anura_2_5',
                'serverName': 'default',
            },
            {
                'id': 'anura_2_5_clean',
                'name': 'Anura - New Model',
                'role': '',
                'schema': 'anura_2_5',
                'serverName': 'default',
            },
            {
                'id': '12d0e352-8f06-45aa-b3ba-58d6d93d3186',
                'name': 'Blast Off To Space (BOTS)',
                'role': 'hidden',
                'schema': 'anura_2_5',
                'serverName': 'default',
            },
            {
                'id': '812d6fae-9fe7-4541-bee5-3cdb78e03eeb',
                'name': 'China Exit Strategy in Asia',
                'role': 'hidden',
                'schema': 'anura_2_5',
                'serverName': 'default',
            },
            {
                'id': '67a881b3-b6ab-4e95-9452-6dae8e831a6b',
                'name': 'Detailed Facility Selection',
                'role': 'hidden',
                'schema': 'anura_2_5',
                'serverName': 'default',
            },
            {
                'id': '71214744-f90a-4dcc-8008-bb9dab9493be',
                'name': 'Greenfield Facility Selection',
                'role': 'hidden',
                'schema': 'anura_2_5',
                'serverName': 'default',
            },
            {
                'id': 'd74fd9cc-e829-4ad3-9f33-f4ef0f3ddae1',
                'name': 'Multi-Year Capacity Planning',
                'role': 'hidden',
                'schema': 'anura_2_5',
                'serverName': 'default',
            },
            {
                'id': 'b69f11eb-ed38-4b72-a43d-d59f7ab2cfa6',
                'name': 'Out of China',
                'role': 'hidden',
                'schema': 'anura_2_5',
                'serverName': 'default',
            },
            {
                'id': '37392edb-d582-4ce8-9f75-024651aa8592',
                'name': 'Tactical Capacity Optimization',
                'role': 'hidden',
                'schema': 'anura_2_5',
                'serverName': 'default',
            },
        ]

        self.assertEqual(resp['templates'], TEMPLATES)

    def test_ip_address_allow(self) -> None:
        '''whitelist ip address'''

        if self.API.storagetype_database_exists is False:
            self.skipTest('account does not have a postgres database')

        db = self.API.account_storage_device(type='postgres_db')
        resp = self.API.ip_address_allow(database_name=db['name'], ip='127.0.0.0')

        self.assertIsInstance(resp['ip'], str)
        self.assertIsInstance(resp['message'], str)
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['ip'], '127.0.0.0')
        self.assertEqual(resp['result'], 'accepted')
        self.assertIn('five-minute delay', resp['message'])

    def test_ip_address_allow_invalid(self) -> None:
        '''unable to whitelist, ip address is invalid'''

        if self.API.storagetype_database_exists is False:
            self.skipTest('account does not have a postgres database')

        db = self.API.account_storage_device(type='postgres_db')
        r = self.API.ip_address_allow(database_name=db['name'], ip='alpha.0.0.0')
        resp: dict = r['resp'].json()
        self.assertIsInstance(resp['message'], str)
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['message'], 'ipAddress is missing or invalid')

    def test_ip_address_allowed(self) -> None:
        '''ip address is whitelisted'''

        if self.API.storagetype_database_exists is False:
            self.skipTest('account does not have a postgres database')

        db = self.API.account_storage_device(type='postgres_db')
        resp = self.API.ip_address_allowed(database_name=db['name'], ip='127.0.0.0')
        self.assertIsInstance(resp['allowed'], bool)
        self.assertIsInstance(resp['ip'], str)
        self.assertIsInstance(resp['message'], str)
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['allowed'], True)
        self.assertEqual(resp['ip'], '127.0.0.0')
        self.assertEqual(resp['result'], 'success')
        self.assertIn('is in the firewall', resp['message'])

    def test_ip_address_allowed_invalid(self) -> None:
        '''ip address is invalid'''

        if self.API.storagetype_database_exists is False:
            self.skipTest('account does not have a postgres database')

        db = self.API.account_storage_device(type='postgres_db')
        r = self.API.ip_address_allowed(database_name=db['name'], ip='alpha.0.0.0')
        resp: dict = r['resp'].json()

        self.assertIsInstance(resp['message'], str)
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['message'], 'ipAddress is missing or invalid')

    def test_onedrive_push(self) -> None:
        '''push optilogic files to onedrive'''

        with self.assertRaises(NotImplementedError):
            self.API.onedrive_push('fakeFilePath')

        return  # OE-7039 API: OneDrive Push Broke

        # does account even have onedrive storage?
        onedrive: bool = self.API.storagetype_onedrive_exists
        if onedrive is False:
            self.skipTest('OneDrive device not available')

        # storage device info cached, grab the first onedrive device name
        devices = self.API.account_storage_devices()
        onedrives = [d for d in devices['storages'] if d['type'] == 'onedrive']

        # upload a file to onedrive device
        file_contents: str = f'{datetime.now()} unittest test_onedrive_push {time.time()}'
        file_path: str = f"/{onedrives[0]['name']}/unittest.txt"
        self.API.wksp_file_upload('Studio', file_path, overwrite=True, filestr=file_contents)

        # initiate push to onedrive
        resp = self.API.onedrive_push(file_path)
        self.assertEqual(resp['result'], 'success')
        self.assertGreaterEqual(resp['count'], 1)
        self.assertIsInstance(resp['storageId'], str)
        self.assertIsInstance(resp['storageName'], str)
        self.assertTrue(resp['storageId'], onedrives[0]['id'])
        self.assertTrue(resp['storageName'], onedrives[0]['name'])

    def test_secret_add(self) -> None:
        '''create a new secret'''

        nano_secs: str = str(time.perf_counter_ns())
        n: str = 'unittest_secret_last_added'
        prereq = self.API.secret(n)
        if prereq.get('crash'):
            self.API.secret_add(n, value=nano_secs, category='unittest')
        else:
            self.API.secret_update(n, value=nano_secs)

        cat: str = 'geocode'
        desc: str = f'unittest {nano_secs}'
        for provider in self.API.GEO_PROVIDERS:
            meta_dict: dict = {'isDefault': False, 'provider': provider}
            meta_str: str = dumps(meta_dict)
            name: str = f'ut_{provider}_{nano_secs}'
            value: str = str(uuid4())

            resp = self.API.secret_add(name, value, cat, desc, meta=meta_str)
            self.assertIsInstance(resp['created'], str)
            self.assertIsInstance(resp['description'], str)
            self.assertIsInstance(resp['id'], str)
            self.assertIsInstance(resp['meta'], str)
            self.assertIsInstance(resp['name'], str)
            self.assertIsInstance(resp['result'], str)
            self.assertIsInstance(resp['type'], str)
            self.assertIsInstance(resp['value'], str)
            self.assertEqual(resp['description'], desc)
            self.assertEqual(resp['meta'], meta_str)
            self.assertEqual(resp['name'], name)
            self.assertEqual(resp['result'], 'success')
            self.assertEqual(resp['type'], cat)
            self.assertEqual(resp['value'], value)
            self.assertTrue(resp['created'].endswith('Z'))
            dt: datetime = parse(resp['created'])
            self.assertTrue(dt.tzname(), 'UTC')
            now: datetime = datetime.utcnow()
            self.assertEqual(dt.year, now.year)
            self.assertEqual(dt.month, now.month)
            self.assertEqual(dt.day, now.day)

    def test_secret_alter(self) -> None:
        '''modify a secret'''

        secrets = self.API._secret_select_all(desc='unittest')  # no values returned, too sensitive
        sec: dict = {}
        name: str = ''
        for secret in secrets:
            if secret['name'].find('bing') > -1:
                sec = secret
                name = secret['name']
                break

        secret = self.API.secret(name)
        newname: str = 'ut_altered'

        resp = self.API.secret_update(name, new_name=newname)
        self.assertEqual(resp['created'], sec['created'])
        self.assertEqual(resp['id'], sec['id'])
        self.assertEqual(resp['description'], sec['description'])
        self.assertEqual(resp['meta'], sec['meta'])
        self.assertEqual(resp['name'], newname)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['type'], sec['type'])

        old = self.API.secret(name)
        self.assertTrue(old['crash'])
        d: dict = loads(old['response_body'])
        self.assertIsInstance(d, dict)
        self.assertEqual(d['result'], 'error')
        self.assertGreater(d['message'].find('no secret found'), -1)
        self.assertEqual(secret['value'], resp['value'])

        new = self.API.secret('ut_altered')
        self.assertEqual(resp['id'], new['id'])
        self.assertEqual(resp['name'], newname)

    def test_secrets(self) -> None:
        '''check all secrets'''

        resp = self.API.secrets()
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)
        self.assertGreaterEqual(resp['count'], 1)
        self.assertIsInstance(resp['secrets'], list)
        self.assertGreaterEqual(len(resp['secrets']), 1)

        for s in resp['secrets']:
            self.assertIsInstance(s['created'], str)
            self.assertEqual(len(s['created']), 24)
            self.assertIsInstance(s['id'], str)
            self.assertEqual(len(s['id']), 36)
            self.assertIsInstance(s['name'], str)
            self.assertGreater(len(s['name']), 0)

            if s.get('description'):
                self.assertIsInstance(s['description'], str)
            if s.get('meta'):
                self.assertIsInstance(s['meta'], str)
            if s.get('type'):
                self.assertIsInstance(s['type'], str)

            dt: datetime = parse(s['created'])
            self.assertTrue(dt.tzname(), 'UTC')

    def test_secrets_exist(self) -> None:
        '''check newly created unittest secrets'''

        prereq = self.API.secret('unittest_secret_last_added')
        if prereq.get('crash'):
            self.skipTest('must first run method test_secret_add')
        nano_secs: str = prereq['value']

        self.assertFalse(
            self.API._secret_exist(name='does_not_exist', category='geocode', desc='unittest')
        )
        self.assertFalse(
            self.API._secret_exist(
                name=f'ut_pcmiler_{nano_secs}', category='geocode', desc='does_not_exist'
            )
        )
        self.assertTrue(
            self.API._secret_exist(
                name=f'ut_pcmiler_{nano_secs}', category='geocode', desc='unittest'
            )
        )

        self.assertFalse(self.API._secret_exist(name='does_not_exist', category='geocode'))
        self.assertFalse(
            self.API._secret_exist(name=f'ut_pcmiler_{nano_secs}', category='does_not_exist')
        )
        self.assertTrue(self.API._secret_exist(name=f'ut_pcmiler_{nano_secs}', category='geocode'))

        self.assertFalse(self.API._secret_exist(name='does_not_exist', desc='unittest'))
        self.assertFalse(
            self.API._secret_exist(name=f'ut_pcmiler_{nano_secs}', desc='does_not_exist')
        )
        self.assertTrue(self.API._secret_exist(name=f'ut_pcmiler_{nano_secs}', desc='unittest'))

        self.assertFalse(self.API._secret_exist(category='geocode', desc='does_not_exist'))
        self.assertTrue(self.API._secret_exist(category='geocode', desc='unittest'))

        self.assertFalse(self.API._secret_exist(name='does_not_exist'))
        self.assertTrue(self.API._secret_exist(name=f'ut_pcmiler_{nano_secs}'))

        self.assertFalse(self.API._secret_exist(category='does_not_exist'))
        self.assertTrue(self.API._secret_exist(category='geocode'))

        self.assertFalse(self.API._secret_exist(desc='does_not_exist'))
        self.assertTrue(self.API._secret_exist(desc='unittest'))

    def test_secrets_remove(self) -> None:
        '''remove all unittest secrets'''

        secrets = self.API._secret_select_all(desc='unittest')

        for s in secrets:
            resp = self.API.secret_delete(s['name'])
            self.assertEqual(resp['result'], 'success')
            self.assertEqual(resp['id'], s['id'])
            self.assertEqual(resp['name'], s['name'])

    def test_sql_connect_info(self) -> None:
        '''get the connection information for a sql storage item'''

        if self.API.storagetype_database_exists is False:
            self.skipTest('account does not have a postgres database')

        pg = self.API.account_storage_device('postgres_db')
        resp = self.API.sql_connection_info(pg['name'])
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp['raw']), 6)
        self.assertIsInstance(resp['raw']['host'], str)
        self.assertTrue(resp['raw']['host'].endswith('postgres.database.azure.com'))
        self.assertIsInstance(resp['raw']['dbname'], str)
        self.assertIsInstance(resp['raw']['password'], str)
        self.assertIsInstance(resp['raw']['port'], int)
        self.assertIsInstance(resp['raw']['sslmode'], str)
        self.assertIsInstance(resp['raw']['user'], str)
        self.assertIsInstance(resp['connectionStrings'], dict)
        self.assertEqual(len(resp['connectionStrings']), 5)
        self.assertTrue(resp['connectionStrings']['jdbc'].startswith('jdbc:postgresql://'))
        self.assertTrue(resp['connectionStrings']['libpq'].startswith('host='))
        self.assertTrue(resp['connectionStrings']['net'].startswith('Server='))
        self.assertTrue(resp['connectionStrings']['psql'].startswith('psql \'host='))
        self.assertTrue(resp['connectionStrings']['url'].startswith('postgresql://'))

    def test_storage(self) -> None:
        '''perform storage device info on every device from storage device list'''

        devices = self.API.account_storage_devices()
        self.assertEqual(devices['result'], 'success')
        with self.subTest():
            for d in devices['storages']:
                d = self.API.storage(d['name'])
                self.assertEqual(d['result'], 'success')
                if d['type'] == 'azure_afs':
                    self.assertEqual(len(d), 12)
                    self.assertIsInstance(d['bytesUsed'], int)
                    self.assertIsInstance(d['capacity'], int)
                    self.assertIsInstance(d['created'], int)
                    self.assertTrue(d['description'] is None or isinstance(d['description'], str))
                    self.assertIsInstance(d['id'], str)
                    self.assertIsInstance(d['internal'], bool)
                    self.assertTrue(
                        d['lockoutReason'] is None or isinstance(d['lockoutReason'], str)
                    )
                    self.assertIsInstance(d['name'], str)
                    self.assertIsInstance(d['tier'], str)
                    self.assertIsInstance(d['type'], str)
                    self.assertIsInstance(d['updated'], int)
                if d['type'] == 'azure_workspace':
                    self.assertEqual(len(d), 13)
                    self.assertIsInstance(d['bytesUsed'], int)
                    self.assertIsInstance(d['capacity'], int)
                    self.assertIsInstance(d['created'], int)
                    self.assertTrue(d['description'] is None or isinstance(d['description'], str))
                    self.assertIsInstance(d['id'], str)
                    self.assertIsInstance(d['internal'], bool)
                    self.assertTrue(
                        d['lockoutReason'] is None or isinstance(d['lockoutReason'], str)
                    )
                    self.assertIsInstance(d['name'], str)
                    self.assertIsInstance(d['tier'], str)
                    self.assertIsInstance(d['type'], str)
                    self.assertIsInstance(d['updated'], int)
                    self.assertIsInstance(d['workspaceKey'], str)
                elif d['type'] == 'onedrive':
                    self.assertEqual(len(d), 20)
                    self.assertIsInstance(d['accountName'], str)
                    self.assertIsInstance(d['authenticated'], int)
                    self.assertTrue(d['bytesUsed'] is None or isinstance(d['bytesUsed'], int))
                    self.assertIsInstance(d['capacity'], int)
                    self.assertIsInstance(d['created'], int)
                    self.assertIsInstance(d['connected'], bool)
                    self.assertTrue(d['description'] is None or isinstance(d['description'], str))
                    self.assertIsInstance(d['endpointSuffix'], str)
                    self.assertIsInstance(d['homeAccountId'], str)
                    self.assertIsInstance(d['id'], str)
                    self.assertIsInstance(d['internal'], bool)
                    self.assertTrue(
                        d['lockoutReason'] is None or isinstance(d['lockoutReason'], str)
                    )
                    self.assertIsInstance(d['name'], str)
                    self.assertIsInstance(d['protocol'], str)
                    self.assertIsInstance(d['tier'], str)
                    self.assertIsInstance(d['type'], str)
                    self.assertIsInstance(d['updated'], int)
                    self.assertIsInstance(d['userId'], str)
                    self.assertIsInstance(d['username'], str)
                elif d['type'] == 'postgres_db':
                    self.assertEqual(len(d), 18)
                    self.assertTrue(d['bytesUsed'] is None or isinstance(d['bytesUsed'], int))
                    self.assertTrue(
                        d['bytesUsedLastUpdated'] is None
                        or isinstance(d['bytesUsedLastUpdated'], int)
                    )
                    self.assertIsInstance(d['created'], int)
                    self.assertIsInstance(d['dbname'], str)
                    self.assertTrue(d['description'] is None or isinstance(d['description'], str))
                    self.assertIsInstance(d['host'], str)
                    self.assertIsInstance(d['id'], str)
                    self.assertTrue(
                        d['lockoutReason'] is None or isinstance(d['lockoutReason'], str)
                    )
                    self.assertIsInstance(d['name'], str)
                    self.assertIsInstance(d['port'], int)
                    self.assertIsInstance(d['type'], str)
                    self.assertIsInstance(d['updated'], int)
                    self.assertIsInstance(d['user'], str)
                    self.assertIsInstance(d['defaultSchema'], str)
                    if d['defaultSchema'].startswith('anura_2_'):
                        self.assertIsInstance(d['schemaStatus'], str)
                        self.assertTrue(
                            d['schemaStatus'] in ('error', 'invalid', 'valid')
                            or len(d['schemaStatus']) == 0
                        )
                        self.assertTrue(
                            d['schemaStatusLastUpdated'] is None
                            or isinstance(d['schemaStatusLastUpdated'], float)
                        )
                        self.assertIsInstance(d['schemaVersion'], str)
                        self.assertRegex(d['schemaVersion'], r'2\.[4-9]\.\d+')
                    else:
                        self.assertEqual(d['defaultSchema'], '"$user"')
                        self.assertEqual(d['schemaStatus'], 'valid')
                        self.assertIsNone(d['schemaStatusLastUpdated'])
                        self.assertTrue(len(d['schemaVersion']) == 0)

    @unittest.skip('api has not implemented')
    def test_storage_disk_create(self):
        '''create a new file storage device'''

        raise NotImplementedError

    @unittest.skip('api is incomplete')
    def test_storage_delete(self):
        '''delete storage device'''

        raise NotImplementedError

    def test_sql_query(self) -> None:
        '''test sql statement execution'''

        if self.API.storagetype_database_exists is False:
            self.skipTest('account does not have postgres database')

        pg = self.API.account_storage_device(type='postgres_db')
        resp = self.API.sql_query(
            database_name=pg['name'], query='SELECT datname FROM pg_database;'
        )
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['rowCount'], int)
        self.assertGreaterEqual(resp['rowCount'], 1)
        self.assertIsInstance(resp['queryResults'], list)
        self.assertGreaterEqual(len(resp['queryResults']), 1)

    def test_wksp_file_copy(self) -> None:
        '''make a copy of a file within a workspace'''

        src: str = self.py_run_me
        dest: str = f'{self.dir_testdata_remote}/cp_test.txt'
        resp = self.API.wksp_file_copy(
            self.WORKSPACE, file_path_src=src, file_path_dest=dest, overwrite=True
        )
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['copyStatus'], 'success')
        self.assertEqual(resp['message'], 'Copy complete')
        src_result: str = (
            f"{resp['sourceFileInfo']['directoryPath']}/{resp['sourceFileInfo']['filename']}"
        )
        dest_result: str = (
            f"{resp['targetFileInfo']['directoryPath']}/{resp['targetFileInfo']['filename']}"
        )
        self.assertEqual(src, src_result)
        self.assertEqual(dest, dest_result)

    def test_wksp_file_delete(self) -> None:
        '''delete a copied file with a workspace'''

        f: str = f'{self.dir_testdata_remote}/cp_test.txt'
        resp = self.API.wksp_file_delete(self.WORKSPACE, file_path=f)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['message'], 'File deleted')
        file_result = f"{resp['fileInfo']['directoryPath']}/{resp['fileInfo']['filename']}"
        self.assertEqual(f, file_result)

    def test_wksp_file_download(self) -> None:
        '''download a file from a given workspace'''

        download = self.API.wksp_file_download(self.WORKSPACE, file_path=self.py_run_me)
        self.assertGreaterEqual(len(download), 1)
        self.assertIsInstance(download, str)

    def test_wksp_file_download_crash(self) -> None:
        '''download a file from a given workspace'''

        resp: str = self.API.wksp_file_download(self.WORKSPACE, file_path='does_not_exist')
        self.assertIsInstance(resp, str)
        r: dict = loads(resp)
        self.assertEqual(r['result'], 'error')
        self.assertIsInstance(r['error'], str)
        self.assertEqual(len(r['correlationId']), 36)

    def test_wksp_file_download_meta(self) -> None:
        '''file metadata'''

        resp = self.API.wksp_file_download_status(self.WORKSPACE, file_path=self.py_run_me)
        self.assertEqual(resp['result'], 'success')
        keys: Tuple[str, ...] = (
            'result',
            'workspace',
            'filename',
            'directoryPath',
            'filePath',
            'lastModified',
            'contentLength',
            'date',
            'fileCreatedOn',
            'fileLastWriteOn',
            'fileChangeOn',
        )
        for key in resp.keys():
            self.assertIn(key, keys)
        self.assertEqual(resp['filePath'], self.py_run_me)
        self.assertEqual(resp['workspace'], self.WORKSPACE)
        self.assertIsInstance(resp['contentLength'], int)
        dt: datetime = parse(resp['lastModified'])
        self.assertEqual(dt.tzname(), 'UTC')

    def test_wksp_file_upload(self) -> None:
        '''upload a file to a workspace'''

        dest: str = f'{self.dir_testdata_remote}/str2file.txt'
        resp = self.API.wksp_file_upload(
            self.WORKSPACE, file_path_dest=dest, overwrite=True, filestr='test'
        )
        self.assertEqual(resp['result'], 'success')
        self.assertIn(resp['message'], ['File created', 'File replaced'])

    def test_wksp_files(self) -> None:
        '''file structure from a given workspace and must have at least one file'''

        resp = self.API.wksp_files(self.WORKSPACE)
        self.assertEqual(resp['result'], 'success')
        self.assertGreaterEqual(resp['count'], 1)
        self.assertIsInstance(resp['files'], list)
        self.assertGreaterEqual(len(resp['files']), 1)
        self.assertTrue(resp['files'][0].get('filename'))
        self.assertTrue(resp['files'][0].get('directoryPath'))
        self.assertTrue(resp['files'][0].get('filePath'))
        self.assertTrue(resp['files'][0].get('contentLength'))

    def test_wksp_folder_delete(self) -> None:
        '''delete a folder from a workspace'''

        folder: str = 'delmenow'
        fp: str = os.path.join(folder, 'delme.txt')
        self.API.wksp_file_upload(self.WORKSPACE, fp, filestr='first file line')
        resp = self.API.wksp_folder_delete(self.WORKSPACE, dir_path=folder, force=True)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['message'], 'Directory and all contents deleted')
        self.assertEqual(resp['directoryPath'], folder)

    def test_wksp_info(self) -> None:
        '''properties of a given workspace'''

        resp = self.API.wksp_info(self.WORKSPACE)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['name'], self.WORKSPACE)
        self.assertEqual(len(resp['key']), 25)
        self.assertRegex(resp['key'], '^workspace')
        self.assertIn(resp['stack'], ['Optilogic', 'Simulation', 'Gurobi'])
        self.assertTrue(resp['status'].isupper())

    def test_wksp_job_back2back(self) -> None:
        '''one job to run many python modules in a row'''

        item_one: dict = {
            'pyModulePath': '/projects/quick_tests/sleep.py',
            'commandArgs': 'not_used',
            'timeout': 90,
        }
        item_two: dict = {
            'pyModulePath': '/projects/quick_tests/airline_hub_location_cbc.py',
            'timeout': 30,
        }
        batch = {'batchItems': [item_one, item_two]}

        tag: str = 'unittest_batch_back2back'
        resp = self.API.wksp_job_back2back(
            self.WORKSPACE, batch=batch, verboseOutput=True, tags=tag
        )
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp), 5)
        self.assertEqual(resp['message'], 'Job submitted')
        self.assertIsInstance(resp['jobKey'], str)
        self.assertEqual(len(resp['jobKey']), 36)
        self.assertIsInstance(resp['batch'], dict)
        self.assertEqual(len(resp['batch']), 1)

        # batchItems
        self.assertIsInstance(batch['batchItems'], list)
        self.assertEqual(len(batch['batchItems']), 2)
        # item_one
        self.assertIsInstance(resp['batch']['batchItems'][0], list)
        self.assertEqual(len(resp['batch']['batchItems'][0]), 3)
        self.assertEqual(resp['batch']['batchItems'][0][0], item_one['pyModulePath'])
        self.assertEqual(resp['batch']['batchItems'][0][1], item_one['commandArgs'])
        self.assertEqual(resp['batch']['batchItems'][0][2], item_one['timeout'])
        # item_two
        self.assertIsInstance(resp['batch']['batchItems'][1], list)
        self.assertEqual(len(resp['batch']['batchItems'][1]), 3)
        self.assertEqual(resp['batch']['batchItems'][1][0], item_two['pyModulePath'])
        self.assertIsNone(resp['batch']['batchItems'][1][1])
        self.assertEqual(resp['batch']['batchItems'][1][2], item_two['timeout'])

        # jobInfo
        self.assertIsInstance(resp['jobInfo'], dict)
        self.assertEqual(len(resp['jobInfo']), 4)
        self.assertEqual(resp['jobInfo']['workspace'], self.WORKSPACE)
        self.assertEqual(resp['jobInfo']['tags'], tag)
        self.assertEqual(resp['jobInfo']['timeout'], -1)
        self.assertIsInstance(resp['jobInfo']['resourceConfig'], dict)
        self.assertEqual(len(resp['jobInfo']['resourceConfig']), 4)
        self.assertEqual(resp['jobInfo']['resourceConfig']['cpu'], '1vCore')
        self.assertEqual(resp['jobInfo']['resourceConfig']['name'], '3XS')
        self.assertEqual(resp['jobInfo']['resourceConfig']['ram'], '2Gb')
        self.assertEqual(resp['jobInfo']['resourceConfig']['run_rate'], 2)

        # verify new batch job
        job = self.API.wksp_job_status(self.WORKSPACE, resp['jobKey'])
        self.assertEqual(job['jobInfo']['workspace'], self.WORKSPACE)
        self.assertEqual(job['jobInfo']['directoryPath'], '/usr/bin')
        self.assertEqual(job['jobInfo']['filename'], 'batch_run.py')
        self.assertEqual(job['jobInfo']['command'], 'run')
        self.assertIsInstance(job['jobInfo']['commandArgs'], str)
        args: dict = loads(job['jobInfo']['commandArgs'][1:-1])
        self.assertIsInstance(args, dict)
        self.assertIsInstance(args['batchItems'], list)
        self.assertEqual(args['batchItems'][0][0], item_one['pyModulePath'])
        self.assertEqual(args['batchItems'][0][1], item_one['commandArgs'])
        self.assertEqual(args['batchItems'][0][2], item_one['timeout'])
        self.assertEqual(args['batchItems'][1][0], item_two['pyModulePath'])
        self.assertEqual(args['batchItems'][1][1], item_two.get('commandArgs'))
        self.assertEqual(args['batchItems'][1][2], item_two['timeout'])
        self.assertEqual(job['jobInfo']['resourceConfig']['cpu'], '1vCore')
        self.assertEqual(job['jobInfo']['resourceConfig']['name'], '3XS')
        self.assertEqual(job['jobInfo']['resourceConfig']['ram'], '2Gb')
        self.assertEqual(job['jobInfo']['resourceConfig']['run_rate'], 2)

    def test_wksp_job_back2back_findnrun(self) -> None:
        '''search file paths yields one job to run many python modules in a row'''

        item_one: dict = {
            'pySearchTerm': '/projects/quick_tests/sleep.py',
            'commandArgs': 'not_used',
            'timeout': 90,
        }
        item_two: dict = {
            'pySearchTerm': '/projects/quick_tests/airline_hub_location_cbc.py',
            'timeout': 30,
        }
        batch = {'batchItems': [item_one, item_two]}

        tag: str = 'unittest_batch_back2back_find'
        resp = self.API.wksp_job_back2back_findnrun(
            self.WORKSPACE, batch=batch, verboseOutput=True, tags=tag
        )
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp), 5)
        self.assertEqual(resp['message'], 'Job submitted')
        self.assertIsInstance(resp['jobKey'], str)
        self.assertEqual(len(resp['jobKey']), 36)
        self.assertIsInstance(resp['batch'], dict)
        self.assertEqual(len(resp['batch']), 2)
        self.assertTrue(resp['batch']['search'])

        # batchItems
        self.assertIsInstance(batch['batchItems'], list)
        self.assertEqual(len(batch['batchItems']), 2)
        # item_one
        self.assertIsInstance(resp['batch']['batchItems'][0], list)
        self.assertEqual(len(resp['batch']['batchItems'][0]), 3)
        self.assertEqual(resp['batch']['batchItems'][0][0], item_one['pySearchTerm'])
        self.assertEqual(resp['batch']['batchItems'][0][1], item_one['commandArgs'])
        self.assertEqual(resp['batch']['batchItems'][0][2], item_one['timeout'])
        # item_two
        self.assertIsInstance(resp['batch']['batchItems'][1], list)
        self.assertEqual(len(resp['batch']['batchItems'][1]), 3)
        self.assertEqual(resp['batch']['batchItems'][1][0], item_two['pySearchTerm'])
        self.assertIsNone(resp['batch']['batchItems'][1][1])
        self.assertEqual(resp['batch']['batchItems'][1][2], item_two['timeout'])

        # jobInfo
        self.assertIsInstance(resp['jobInfo'], dict)
        self.assertEqual(len(resp['jobInfo']), 4)
        self.assertEqual(resp['jobInfo']['workspace'], self.WORKSPACE)
        self.assertEqual(resp['jobInfo']['tags'], tag)
        self.assertEqual(resp['jobInfo']['timeout'], -1)
        self.assertIsInstance(resp['jobInfo']['resourceConfig'], dict)
        self.assertEqual(len(resp['jobInfo']['resourceConfig']), 4)
        self.assertEqual(resp['jobInfo']['resourceConfig']['cpu'], '1vCore')
        self.assertEqual(resp['jobInfo']['resourceConfig']['name'], '3XS')
        self.assertEqual(resp['jobInfo']['resourceConfig']['ram'], '2Gb')
        self.assertEqual(resp['jobInfo']['resourceConfig']['run_rate'], 2)

        # verify new batch job
        job = self.API.wksp_job_status(self.WORKSPACE, resp['jobKey'])
        self.assertEqual(job['jobInfo']['workspace'], self.WORKSPACE)
        self.assertEqual(job['jobInfo']['directoryPath'], '/usr/bin')
        self.assertEqual(job['jobInfo']['filename'], 'batch_search_n_run.py')
        self.assertEqual(job['jobInfo']['command'], 'run')
        self.assertIsInstance(job['jobInfo']['commandArgs'], str)
        args: dict = loads(job['jobInfo']['commandArgs'][1:-1])
        self.assertIsInstance(args, dict)
        self.assertIsInstance(args['batchItems'], list)
        self.assertEqual(args['batchItems'][0][0], item_one['pySearchTerm'])
        self.assertEqual(args['batchItems'][0][1], item_one['commandArgs'])
        self.assertEqual(args['batchItems'][0][2], item_one['timeout'])
        self.assertEqual(args['batchItems'][1][0], item_two['pySearchTerm'])
        self.assertEqual(args['batchItems'][1][1], item_two.get('commandArgs'))
        self.assertEqual(args['batchItems'][1][2], item_two['timeout'])
        self.assertEqual(job['jobInfo']['resourceConfig']['cpu'], '1vCore')
        self.assertEqual(job['jobInfo']['resourceConfig']['name'], '3XS')
        self.assertEqual(job['jobInfo']['resourceConfig']['ram'], '2Gb')
        self.assertEqual(job['jobInfo']['resourceConfig']['run_rate'], 2)

    def test_wksp_job_file_error(self) -> None:
        '''get job error file'''

        resp: str = self.API.wksp_job_file_error(self.WORKSPACE, self.API._job_start_recent_key)
        self.assertIsInstance(resp, str)
        if resp.startswith('{\"result\":\"error\"'):
            err: dict = loads(resp)
            self.assertEqual(err['result'], 'error')
            self.assertIsInstance(err['error'], str)
            self.assertIsInstance(err['correlationId'], str)
            self.assertEqual(len(err['correlationId']), 36)
        else:
            self.assertGreater(len(resp), 0)

    def test_wksp_job_file_result(self) -> None:
        '''get job result file'''

        resp: str = self.API.wksp_job_file_result(self.WORKSPACE, self.API._job_start_recent_key)
        self.assertIsInstance(resp, str)
        if resp.startswith('{\"result\":\"error\"'):
            err: dict = loads(resp)
            self.assertEqual(err['result'], 'error')
            self.assertIsInstance(err['error'], str)
            self.assertIsInstance(err['correlationId'], str)
            self.assertEqual(len(err['correlationId']), 36)
        else:
            self.assertGreater(len(resp), 0)

    def test_wksp_job_ledger(self) -> None:
        '''get job ledger that has realtime messages'''

        resp = self.API.wksp_job_ledger(self.WORKSPACE, self.API._job_start_recent_key)
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)
        self.assertGreaterEqual(resp['count'], 1)
        self.assertIsInstance(resp['records'], list)
        self.assertGreaterEqual(len(resp['records']), 1)
        self.assertIsInstance(resp['records'][0]['timestamp'], int)
        self.assertIsInstance(resp['records'][0]['datetime'], str)
        # job was created during init, assert same day
        self.assertTrue(resp['records'][0]['datetime'].endswith('Z'))
        dt: datetime = parse(resp['records'][0]['datetime'])
        self.assertTrue(dt.tzname(), 'UTC')
        now: datetime = datetime.utcnow()
        self.assertEqual(dt.year, now.year)
        self.assertEqual(dt.month, now.month)
        self.assertEqual(dt.day, now.day)

    def test_wksp_job_metrics(self) -> None:
        '''get one second cpu and memory sampling of a job'''

        resp = self.API.wksp_job_metrics(self.WORKSPACE, self.API._job_start_recent_key)
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)
        self.assertGreaterEqual(resp['count'], 1)
        self.assertIsInstance(resp['max'], dict)
        self.assertEqual(len(resp['max']), 7)
        self.assertIsInstance(resp['max']['memoryPercent'], float)
        self.assertIsInstance(resp['max']['memoryResident'], float)
        self.assertIsInstance(resp['max']['memoryAvailable'], int)
        self.assertIsInstance(resp['max']['cpuPercent'], float)
        self.assertIsInstance(resp['max']['cpuUsed'], float)
        self.assertIsInstance(resp['max']['cpuAvailable'], int)
        self.assertIsInstance(resp['max']['processCount'], int)
        self.assertIsInstance(resp['records'], list)
        self.assertGreaterEqual(len(resp['records']), 1)
        self.assertIsInstance(resp['records'][0]['timestamp'], int)
        self.assertIsInstance(resp['records'][0]['datetime'], str)
        self.assertTrue(resp['records'][0]['datetime'].endswith('Z'))
        dt: datetime = parse(resp['records'][0]['datetime'])
        self.assertTrue(dt.tzname(), 'UTC')
        now: datetime = datetime.utcnow()
        self.assertEqual(dt.year, now.year)
        self.assertEqual(dt.month, now.month)
        self.assertEqual(dt.day, now.day)
        self.assertIsInstance(resp['records'][0], dict)
        self.assertIsInstance(resp['records'][0]['cpuAvailable'], int)
        self.assertIsInstance(resp['records'][0]['cpuPercent'], float)
        self.assertIsInstance(resp['records'][0]['cpuUsed'], float)
        self.assertIsInstance(resp['records'][0]['memoryAvailable'], int)
        self.assertIsInstance(resp['records'][0]['memoryPercent'], float)
        self.assertIsInstance(resp['records'][0]['memoryResident'], float)
        self.assertIsInstance(resp['records'][0]['processCount'], int)

    def test_wksp_job_metrics_max(self) -> None:
        '''get peak cpu and memory stats of a job'''

        resp = self.API.wksp_job_metrics_max(self.WORKSPACE, self.API._job_start_recent_key)
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['max'], dict)
        self.assertEqual(len(resp['max']), 7)
        self.assertIsInstance(resp['max']['memoryPercent'], float)
        self.assertIsInstance(resp['max']['memoryResident'], float)
        self.assertIsInstance(resp['max']['memoryAvailable'], int)
        self.assertIsInstance(resp['max']['cpuPercent'], float)
        self.assertIsInstance(resp['max']['cpuUsed'], float)
        self.assertIsInstance(resp['max']['cpuAvailable'], int)
        self.assertIsInstance(resp['max']['processCount'], int)

    def test_wksp_job_metrics_mia(self) -> None:
        '''
        OE-5276 Job Metrics are Missing Sometimes
        OE-5369 Job Metrics Missing v3
        '''

        # spin up a few jobs to create load and evaluate all
        jobs_max: int = 9
        tag_time: float = time.time()
        tag: str = f'metrics_{tag_time}'
        secs: int = 15
        for job in range(jobs_max):
            self.API.wksp_job_start(self.WORKSPACE, self.py_run_me, tags=tag, timeout=secs)

        # check the jobs that are about to run
        d: dict = {}
        check: bool = True
        loops: int = 0
        while check:
            jobs = self.API.wksp_jobs(self.WORKSPACE, tags=tag)

            # jobs all finished?
            terminal: int = 0
            for t in self.API.JOBSTATES_TERMINAL:
                terminal += jobs['statusCounts'].get(t)

            if terminal == jobs_max:
                check = False
                break

            # check running jobs for metrics
            active = self.API.wksp_jobs(self.WORKSPACE, status='running', tags=tag)

            if active['statusCounts']['running'] >= 1:
                for job in active['jobs']:
                    resp = self.API.wksp_job_metrics(self.WORKSPACE, job['jobKey'])
                    self.assertEqual(resp['result'], 'success')
                    self.assertIsInstance(resp['count'], int)
                    # self.assertGreaterEqual(resp['count'], 1)

                    # missing metrics!
                    if resp['count'] == 0:
                        st: str = str(job['startDatetime'])
                        st = st.replace('T', ' ')
                        st = st.replace('Z', '')
                        job_start: datetime = datetime.fromisoformat(st)
                        now: datetime = datetime.utcnow()
                        delta: timedelta = now - job_start
                        d[job['jobKey']] = str(
                            delta
                        )  # store job key and elapsed time without metrics

                        print(
                            f"{str(delta)} secs elapsed and metrics missing for job {job['jobKey']}"
                        )
                        with self.subTest():
                            self.assertLess(delta.total_seconds(), 5)

            time.sleep(1)

        # were there any jobs that failed metric check?
        if len(d) >= 1:
            print(f"\n\nJob Submitted: {jobs_max}, Job Duration: {secs}, Job Tag: {tag}")
            print('\n JobKey, LastSeenWithMissingMetricCount_RunDuration')
            for k in d.items():
                print(k[1], k[0])

    def test_wksp_job_start(self) -> None:
        '''creating a job'''

        resp = self.API.wksp_job_start(
            self.WORKSPACE, file_path=self.py_run_me, tags='unittest_start'
        )
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp['jobKey']), 36)
        job_info_keys: Tuple[str, ...] = (
            'workspace',
            'directoryPath',
            'filename',
            'command',
            'resourceConfig',
            'tags',
            'timeout',
        )
        for key in resp['jobInfo'].keys():
            self.assertIn(key, job_info_keys)

    def test_wksp_job_status(self) -> None:
        '''get job status for explicit state'''

        resp = self.API.wksp_job_status(self.WORKSPACE, self.API._job_start_recent_key)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp['jobKey']), 36)
        self.assertIsInstance(resp['submittedDatetime'], str)
        self.assertTrue(resp['submittedDatetime'].endswith('Z'))
        dt: datetime = parse(resp['submittedDatetime'])
        self.assertTrue(dt.tzname(), 'UTC')
        now: datetime = datetime.utcnow()
        self.assertEqual(dt.year, now.year)
        self.assertEqual(dt.month, now.month)
        self.assertEqual(dt.day, now.day)
        self.assertIn(resp['status'], self.API.JOBSTATES)
        job_info_keys: Tuple[str, ...] = (
            'workspace',
            'directoryPath',
            'filename',
            'command',
            'errorFile',
            'resultFile',
            'resourceConfig',
            'tags',
            'timeout',
        )
        for key in resp['jobInfo'].keys():
            self.assertIn(key, job_info_keys)
        self.assertEqual(resp['jobInfo']['command'], 'run')
        self.assertIsInstance(resp['jobInfo']['errorFile'], bool)
        self.assertIsInstance(resp['jobInfo']['resultFile'], bool)
        resource_keys: Tuple[str, ...] = ('name', 'cpu', 'ram', 'run_rate')
        for key in resp['jobInfo']['resourceConfig']:
            self.assertIn(key, resource_keys)

    def test_wksp_job_stop(self) -> None:
        '''stop a most recently created job'''

        # guarantee a job is currently running
        resp = self.API.wksp_job_status(self.WORKSPACE, self.API._job_start_recent_key)
        if resp['status'] in self.API.JOBSTATES_TERMINAL:
            resp = self.API.wksp_job_start(self.WORKSPACE, self.py_run_me)
            success: bool = self.API.util_job_monitor(self.WORKSPACE, resp['jobKey'])
            if success is False:
                self.skipTest('failed to start job within two minutes')

        # stop running job
        resp = self.API.wksp_job_stop(self.WORKSPACE, self.API._job_start_recent_key)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['jobKey'], self.API._job_start_recent_key)
        keys: Tuple[str, ...] = ('result', 'message', 'jobKey', 'status', 'jobInfo')
        for key in resp.keys():
            self.assertIn(key, keys)

    def test_wksp_jobify(self) -> None:
        '''batch queue many jobs'''

        batch = {
            'batchItems': [
                {'pyModulePath': '/projects/quick_tests/sleep.py', 'timeout': 90},
                {
                    'pyModulePath': '/projects/quick_tests/airline_hub_location_cbc.py',
                    'timeout': 30,
                },
            ]
        }

        tag: str = 'unittest_batch_jobify'
        resp = self.API.wksp_jobify(self.WORKSPACE, batch=batch, tags=tag)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['message'], 'Jobs submitted')
        self.assertIsInstance(resp['count'], int)
        self.assertEqual(resp['count'], len(resp['jobKeys']))
        for key in resp['jobKeys']:
            self.assertIsInstance(key, str)
            self.assertEqual(len(key), 36)

    def test_wksp_jobify_findnrun(self) -> None:
        '''search file paths yields many jobs to run each python module found'''

        batch = {
            'batchItems': [
                {'pySearchTerm': '^/quick_tests/sleep.py', 'timeout': 90},
                {'pySearchTerm': '^/quick_tests/airline_hub_location_cbc.py', 'timeout': 30},
            ]
        }

        tag: str = 'unittest_batch_jobify_find'
        resp = self.API.wksp_jobify_findnrun(self.WORKSPACE, batch=batch, tags=tag)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['message'], 'Jobs submitted')
        self.assertIsInstance(resp['count'], int)
        self.assertEqual(len(batch['batchItems']), resp['count'])
        self.assertEqual(resp['count'], len(resp['jobKeys']))
        for key in resp['jobKeys']:
            self.assertIsInstance(key, str)
            self.assertEqual(len(key), 36)

    def test_wksp_jobs(self) -> None:
        '''list the jobs for a specific workspace'''

        resp = self.API.wksp_jobs(self.WORKSPACE)
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)
        self.assertIsInstance(resp['statusCounts'], dict)

        status_keys: Tuple[str, ...] = self.API.JOBSTATES
        for status in resp['statusCounts']:
            self.assertIn(status, status_keys)
            self.assertGreaterEqual(resp['statusCounts'][status], 0)

        self.assertIsInstance(resp['tagCounts'], dict)
        self.assertIsInstance(resp['filters'], dict)

        filter_keys: Tuple[str, ...] = (
            'command',
            'history',
            'runSecsMax',
            'runSecsMin',
            'status',
            'tags',
        )
        for filter in resp['filters']:
            self.assertIn(filter, filter_keys)

        self.assertGreaterEqual(len(resp['jobs']), 1)
        job_keys: Tuple[str, ...] = (
            'jobKey',
            'submittedDatetime',
            'startDatetime',
            'endDatetime',
            'runTime',
            'runRate',
            'billedTime',
            'status',
            'jobInfo',
            'waitTime',
        )
        for job in resp['jobs']:
            for key, value in job.items():
                self.assertIn(key, job_keys)
                if key.lower().find('datetime') > -1 and value:
                    with self.subTest():
                        dt: datetime = parse(value)
                        self.assertEqual(dt.tzname(), 'UTC')
                if key == 'jobInfo':
                    if job[key]['command'] == 'run':
                        self.assertIsInstance(job[key]['directoryPath'], str)
                        self.assertIsInstance(job[key]['filename'], str)
                    self.assertIsInstance(job[key]['resourceConfig'], dict)
                    self.assertIsInstance(job[key]['workspace'], str)

    def test_wksp_jobs_stats(self) -> None:
        '''get the stats for jobs for a specific workspace'''

        resp = self.API.wksp_jobs(self.WORKSPACE)
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)
        self.assertIsInstance(resp['statusCounts'], dict)

        status_keys: Tuple[str, ...] = self.API.JOBSTATES
        for status in resp['statusCounts']:
            self.assertIn(status, status_keys)
            self.assertGreaterEqual(resp['statusCounts'][status], 0)

        self.assertIsInstance(resp['tagCounts'], dict)
        self.assertIsInstance(resp['filters'], dict)

        filter_keys: Tuple[str, ...] = (
            'command',
            'history',
            'runSecsMax',
            'runSecsMin',
            'status',
            'tags',
        )
        for filter in resp['filters']:
            self.assertIn(filter, filter_keys)

    def test_wksp_share_file(self) -> None:
        '''share a file from a workspace to all other workspaces of a user/self'''

        if self.API.auth_username is None:
            self.skipTest('test_wksp_share_folder requires a username')
        
        resp = self.API.wksp_share_file(
            self.WORKSPACE, file_path=self.py_run_me, targetUsers=self.API.auth_username
        )
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp.keys()), 8)
        self.assertIsInstance(resp['errored'], list)
        self.assertEqual(len(resp['errored']), 0)
        self.assertIsInstance(resp['erroredCount'], int)
        self.assertIsInstance(resp['jobs'], list)
        self.assertEqual(len(resp['jobs']), self.API.account_workspace_count - 1)
        for j in resp['jobs']:
            self.assertIsInstance(j['jobKey'], str)
            self.assertIsInstance(j['result'], str)
            self.assertEqual(j['result'], 'success')
        self.assertEqual(resp['jobsCount'], self.API.account_workspace_count - 1)
        self.assertIsInstance(resp['message'], str)
        self.assertEqual(resp['message'], 'Share Accepted')
        self.assertIsInstance(resp['sourceFileInfo'], dict)
        self.assertEqual(len(resp['sourceFileInfo'].keys()), 2)
        self.assertIsInstance(resp['sourceFileInfo']['directoryPath'], str)
        self.assertEqual(resp['sourceFileInfo']['directoryPath'], os.path.split(self.py_run_me)[0])
        self.assertIsInstance(resp['sourceFileInfo']['filename'], str)
        self.assertEqual(resp['sourceFileInfo']['filename'], os.path.split(self.py_run_me)[1])
        self.assertEqual(resp['targetUsers'], self.API.auth_username)

    def test_wksp_share_file_sample(self) -> None:
        '''OE-5840 API Share File/Folder Results in 500 Internal Server Error'''

        if self.API.auth_username is None:
            self.skipTest('test_wksp_share_folder requires a username')
        
        if self.API.account_workspace_count < 2:
            self.skipTest('account does not have required multi-workspaces needed for sharing')

        test_result: bool = False

        # get all not Studio workspaces
        resp: dict = self.API.account_workspaces()
        wksp_names: list[str] = [w['name'] for w in resp['workspaces'] if w['name'] != 'Studio']
        wksp_not_studio: str = wksp_names[0]

        # upload files to share
        filenames: list[str] = []
        filepaths: list[str] = []
        tag: int = time.perf_counter_ns()
        for x in range(10):
            filename: str = f'{tag}_{x}.txt'
            file_path: str = f'/My Files/{tag}/{filename}'
            file_contents: str = f'{datetime.now()} {tag}_{x} unittest test_wksp_share_file_sample'
            resp = self.API.wksp_file_upload('Studio', file_path, filestr=file_contents)
            if resp.get('crash'):
                print(f'{x} {filename} upload attempt failed')
                continue
            filenames.append(filename)
            filepaths.append(file_path)

        # verify uploaded files arrived
        up_arrived: bool = False
        up_count_verified: int = 0
        up_start: float = time.perf_counter()
        while up_arrived is False and time.perf_counter() - up_start < 30:
            resp = self.API.wksp_files('Studio', str(tag))
            if resp.get('crash'):
                continue

            up_count_verified = resp.get('count', 0)
            print(
                f'{tag} {up_count_verified}/{len(filepaths)} confirmed files uploaded {time.perf_counter() - up_start} secs'
            )
            if resp.get('count') == len(filepaths):
                up_arrived = True
                break
            time.sleep(2)

        if up_arrived is False:
            print(f'verify upload failed {len(filepaths)} - {up_count_verified} files missing')
            print('30 seconds not enough time to verify?')

        # share files to other workspaces
        files_failed_sharing: int = 0
        for fp in filepaths:
            resp = self.API.wksp_share_file('Studio', fp, targetUsers=self.API.auth_username)
            if resp.get('crash'):
                print(f'share crash skipping {fp}')
                files_failed_sharing += 1

        # verify shared files arrived to determine test case can pass
        share_arrived: bool = False
        start_share: float = time.perf_counter()
        # TODO verify file share arrived to all non studio workspaces
        diffs = set()
        while share_arrived is False and time.perf_counter() - start_share < 180:
            resp = self.API.wksp_files(wksp_not_studio, str(tag))
            filenames_verified: set[str] = {f['filename'] for f in resp['files']}
            diffs: set[str] = set(filenames).symmetric_difference(filenames_verified)
            if resp.get('count') == up_count_verified and len(diffs) == 0:
                share_arrived = True
                break
            elif resp.get('count', 0) > up_count_verified:
                # BUG there might be file share retry logic
                # 1156398951931738_1.txt failed to share due to 500/504 issue but it showed up 5mins later
                # 1156398951931738_1_2022-10-15T021756Z.txt server tried more than once and created a duplicate!
                break
            time.sleep(2)

        if share_arrived:
            test_result = True
        else:
            print(f'verify share file diff: {len(diffs)}\n{sorted(diffs)}')

        # cleanup: remove files used to share out
        self.API.wksp_folder_delete('Studio', f'My Files/{tag}', force=True)

        # cleanup: remove files shared to other workspaces
        share_folders: list[str] = ['Sent to Me', 'sent_to_me']
        for ws in wksp_names:
            for share_folder in share_folders:
                resp = self.API.wksp_files(ws, share_folder)
                if resp.get('count') == 0:
                    continue
                for fn in filenames:
                    self.API.wksp_file_delete(ws, f'{share_folder}/{self.API.auth_username}/{fn}')

        self.assertTrue(test_result)

    def test_wksp_share_folder(self) -> None:
        '''share a subtree from a workspace to all other workspaces of a user/self'''

        if self.API.auth_username is None:
            self.skipTest('test_wksp_share_folder requires a username')

        resp = self.API.wksp_share_folder(
            self.WORKSPACE, dir_path=self.dir_testdata_remote, targetUsers=self.API.auth_username
        )
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp.keys()), 8)
        self.assertIsInstance(resp['errored'], list)
        self.assertEqual(len(resp['errored']), 0)
        self.assertIsInstance(resp['erroredCount'], int)
        self.assertIsInstance(resp['jobs'], list)
        self.assertEqual(len(resp['jobs']), self.API.account_workspace_count - 1)
        for j in resp['jobs']:
            self.assertIsInstance(j['jobKey'], str)
            self.assertIsInstance(j['result'], str)
            self.assertEqual(j['result'], 'success')
        self.assertEqual(resp['jobsCount'], self.API.account_workspace_count - 1)
        self.assertIsInstance(resp['message'], str)
        self.assertEqual(resp['message'], 'Share Accepted')
        self.assertIsInstance(resp['sourceFileInfo'], dict)
        self.assertEqual(len(resp['sourceFileInfo'].keys()), 1)
        self.assertIsInstance(resp['sourceFileInfo']['directoryPath'], str)
        self.assertEqual(resp['sourceFileInfo']['directoryPath'], self.dir_testdata_remote)
        self.assertEqual(resp['targetUsers'], self.API.auth_username)


if __name__ == '__main__':
    # !! TODO update module docstring to set your user defaults !!
    # apikey replace YOUR_USERNAME, YOUR_PASSWORD
    # appkey replace YOUR_USERNAME, YOUR_APPLICATION_KEY, and set auth_legacy to False

    args: dict = docopt(__doc__)
    TestApi.APPKEY = args.get('--appkey')
    TestApi.AUTH_LEGACY = args.get('--authlegacy', '').lower() == 'true'
    TestApi.USERNAME = args.get('--user')
    TestApi.USERPASS = args.get('--pass')
    TestApi.WORKSPACE = args.get('--wksp', 'Studio')
    unittest.main(__name__, argv=['main'])
