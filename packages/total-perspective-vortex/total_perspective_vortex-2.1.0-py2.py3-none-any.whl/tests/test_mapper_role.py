import os
import unittest
from tpv.rules import gateway
from tpv.commands.test import mock_galaxy
from galaxy.jobs.mapper import JobMappingException


class TestMapperRole(unittest.TestCase):

    @staticmethod
    def _map_to_destination(tool, user):
        galaxy_app = mock_galaxy.App(job_conf=os.path.join(os.path.dirname(__file__), 'fixtures/job_conf.yml'))
        job = mock_galaxy.Job()
        tpv_config = os.path.join(os.path.dirname(__file__), 'fixtures/mapping-role.yml')
        gateway.ACTIVE_DESTINATION_MAPPER = None
        return gateway.map_tool_to_destination(galaxy_app, job, tool, user, tpv_config_files=[tpv_config])

    def test_map_default_role(self):
        tool = mock_galaxy.Tool('bwa')
        user = mock_galaxy.User('ford', 'prefect@vortex.org')

        destination = self._map_to_destination(tool, user)
        self.assertEqual(destination.id, "k8s_environment")

    def test_map_overridden_role(self):
        tool = mock_galaxy.Tool('bwa')
        user = mock_galaxy.User('gargravarr', 'fairycake@vortex.org', roles=["training"])

        with self.assertRaisesRegex(JobMappingException, "No destinations are available to fulfill request"):
            self._map_to_destination(tool, user)

    def test_map_role_by_regex(self):
        tool = mock_galaxy.Tool('bwa')
        user = mock_galaxy.User('gargravarr', 'fairycake@vortex.org', roles=["newtraining2021group"])

        destination = self._map_to_destination(tool, user)
        self.assertEqual(destination.id, "k8s_environment")

    def test_map_role_env_combine_order(self):
        tool = mock_galaxy.Tool('bwa')
        user = mock_galaxy.User('gargravarr', 'fairycake@vortex.org', roles=["newtraining2021group"])

        destination = self._map_to_destination(tool, user)
        self.assertEqual(destination.id, "k8s_environment")
        self.assertEqual([env['value'] for env in destination.env if env['name'] == 'TOOL_AND_USER_DEFINED'], ['user'])
        self.assertEqual([env['value'] for env in destination.env if env['name'] == 'TOOL_AND_ROLE_DEFINED'], ['role'])
        self.assertEqual([env['value'] for env in destination.env if env['name'] == 'TOOL_USER_AND_ROLE_DEFINED'],
                         ['user'])
        self.assertEqual([env['value'] for env in destination.env if env['name'] == 'USER_AND_ROLE_DEFINED'],
                         ['user'])
