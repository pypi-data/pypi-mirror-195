"""DNS Authenticator for Azure DNS."""
import logging
from os import getenv
from typing import Dict

from azure.mgmt.dns import DnsManagementClient
from azure.mgmt.dns.models import RecordSet, TxtRecord
from azure.core.exceptions import HttpResponseError
from azure.identity import ClientSecretCredential, ManagedIdentityCredential, CertificateCredential

from certbot import errors
from certbot.plugins import dns_common

logger = logging.getLogger(__name__)
logging.getLogger('azure').setLevel(logging.WARNING)


class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Azure DNS

    This Authenticator uses the Azure DNS API to fulfill a dns-01 challenge.
    """

    description = ('Obtain certificates using a DNS TXT record (if you are using '
                   'Azure for DNS).')
    ttl = 120

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credential = None
        self.domain_zoneid = {}  # type: Dict[str, str]

        # Azure Environmental Support
        self._azure_environment = getenv("AZURE_ENVIRONMENT", "AzurePublicCloud").lower()
        self._azure_endpoints = {
            "azurepubliccloud": {
                "ResourceManagerEndpoint": "https://management.azure.com/",
                "ActiveDirectoryEndpoint": "https://login.microsoftonline.com/"
            },
            "azureusgovernmentcloud": {
                "ResourceManagerEndpoint": "https://management.usgovcloudapi.net/",
                "ActiveDirectoryEndpoint": "https://login.microsoftonline.us/"
            },
            "azurechinacloud": {
                "ResourceManagerEndpoint": "https://management.chinacloudapi.cn/",
                "ActiveDirectoryEndpoint": "https://login.chinacloudapi.cn/"
            },
            "azuregermancloud": {
                "ResourceManagerEndpoint": "https://management.microsoftazure.de/",
                "ActiveDirectoryEndpoint": "https://login.microsoftonline.de/"
            }
        }

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(add)
        add('config', help='Azure config INI file.')
        add('credentials', help='Azure config INI file. Fallback for legacy integrations')

    def more_info(self):  # pylint: disable=missing-function-docstring
        return 'This plugin configures a DNS TXT record to respond to a dns-01 challenge using ' + \
               'the Azure DNS API.'

    def _validate_credentials(self, credentials):
        sp_client_id = credentials.conf('sp_client_id')
        sp_client_secret = credentials.conf('sp_client_secret')
        sp_certificate_path = credentials.conf('sp_certificate_path')
        tenant_id = credentials.conf('tenant_id')
        has_sp = all((sp_client_id, any((sp_client_secret, sp_certificate_path)), tenant_id))

        msi_client_id = credentials.conf('msi_client_id')
        msi_system_assigned = credentials.conf('msi_system_assigned')

        if not any((has_sp, msi_system_assigned, msi_client_id)):
            raise errors.PluginError('{}: No authentication methods have been '
                                     'configured for Azure DNS. Either configure '
                                     'a service principal or system/user assigned '
                                     'managed identity'.format(credentials.confobj.filename))

        has_zone_mapping = any((key for key in credentials.confobj.keys() if 'azure_zone' in key))

        if not has_zone_mapping:
            raise errors.PluginError('{}: At least one zone mapping needs to be provided,'
                                     ' e.g dns_azure_zone1 = DOMAIN:DNS_ZONE_RESOURCE_GROUP_ID'
                                     ''.format(credentials.confobj.filename))

        # Azure Environment
        environment = credentials.conf('environment')

        if environment:
            self._azure_environment = environment.lower()

        self._arm_endpoint = self._azure_endpoints[self._azure_environment]["ResourceManagerEndpoint"]
        self._aad_endpoint = self._azure_endpoints[self._azure_environment]["ActiveDirectoryEndpoint"]
        
        # Check we have key value
        dns_zone_mapping_items_has_colon = [':' in value
                                            for key, value in credentials.confobj.items()
                                            if 'azure_zone' in key]
        if not all(dns_zone_mapping_items_has_colon):
            raise errors.PluginError('{}: DNS Zone mapping is not in the format of '
                                     'DOMAIN:DNS_ZONE_RESOURCE_GROUP_ID'
                                     ''.format(credentials.confobj.filename))

    def _setup_credentials(self):
        # Alias's dns-azure-credentials -> dns-azure-config
        if self.config.namespace.dns_azure_credentials:
            self.config.namespace.dns_azure_config = self.config.namespace.dns_azure_credentials

        valid_creds = self._configure_credentials(
            'config',
            'Azure config INI file',
            None,
            self._validate_credentials
        )

        # Convert dns_azure_zoneX = key:value into key:value
        dns_zone_mapping_items = [value for key, value in valid_creds.confobj.items()
                                  if 'azure_zone' in key]
        self.domain_zoneid = dict([item.split(':', 1) for item in dns_zone_mapping_items])

        # Figure out which credential type we're going to use
        sp_client_id = valid_creds.conf('sp_client_id')
        sp_client_secret = valid_creds.conf('sp_client_secret')
        sp_certificate_path = valid_creds.conf('sp_certificate_path')
        tenant_id = valid_creds.conf('tenant_id')
        msi_client_id = valid_creds.conf('msi_client_id')

        self.credential = self._get_azure_credentials(
            sp_client_id, sp_client_secret, sp_certificate_path, tenant_id, msi_client_id, self._aad_endpoint
        )

    @staticmethod
    def _get_azure_credentials(client_id=None, client_secret=None, certificate_path=None, tenant_id=None, msi_client_id=None, aad_endpoint=None):
        has_sp = all((client_id, client_secret, tenant_id))
        has_sp_cert = all((client_id, certificate_path, tenant_id))
        if has_sp:
            return ClientSecretCredential(
                client_id=client_id,
                client_secret=client_secret,
                tenant_id=tenant_id,
                authority=aad_endpoint
            )
        elif has_sp_cert:
            return CertificateCredential(
                client_id=client_id,
                certificate_path=certificate_path,
                tenant_id=tenant_id,
                authority=aad_endpoint
            )
        elif msi_client_id:
            return ManagedIdentityCredential(client_id=msi_client_id)
        else:
            return ManagedIdentityCredential()

    def _get_ids_for_domain(self, domain: str):
        try:
            for azure_dns_domain, resource_group in self.domain_zoneid.items():
                # Look to see if domain ends with key, to cover subdomains
                if domain.endswith(azure_dns_domain):
                    subscription_id = resource_group.split('/')[2]
                    rg_name = resource_group.split('/')[4]
                    return azure_dns_domain, subscription_id, rg_name
            else:
                raise errors.PluginError('Domain {} does not have a valid domain to '
                                         'resource group id mapping'.format(domain))
        except IndexError:
            raise errors.PluginError('Domain {} has an invalid resource group id'.format(domain))

    @staticmethod
    def _get_relative_domain(fqdn: str, domain: str) -> str:
        if fqdn == domain:
            return '@'
        return fqdn.replace(domain, '').strip('.')

    def _perform(self, domain, validation_name, validation):
        azure_domain, subscription_id, resource_group_name = self._get_ids_for_domain(domain)
        client = self._get_azure_client(subscription_id)
        relative_validation_name = self._get_relative_domain(validation_name, azure_domain)

        # Check to see if there are any existing TXT validation record values
        txt_value = {validation}
        try:
            existing_rr = client.record_sets.get(
                resource_group_name=resource_group_name,
                zone_name=azure_domain,
                relative_record_set_name=relative_validation_name,
                record_type='TXT')
            for record in existing_rr.txt_records:
                for value in record.value:
                    txt_value.add(value)
        except HttpResponseError as err:
            if err.status_code != 404:  # Ignore RR not found
                raise errors.PluginError('Failed to check TXT record for domain '
                                         '{}, error: {}'.format(domain, err))

        try:
            client.record_sets.create_or_update(
                resource_group_name=resource_group_name,
                zone_name=azure_domain,
                relative_record_set_name=relative_validation_name,
                record_type='TXT',
                parameters=RecordSet(ttl=self.ttl, txt_records=[TxtRecord(value=[v]) for v in txt_value])
            )
        except HttpResponseError as err:
            raise errors.PluginError('Failed to add TXT record to domain '
                                     '{}, error: {}'.format(domain, err))

    def _cleanup(self, domain, validation_name, validation):
        if self.credential is None:
            self._setup_credentials()

        azure_domain, subscription_id, resource_group_name = self._get_ids_for_domain(domain)
        relative_validation_name = self._get_relative_domain(validation_name, azure_domain)
        client = self._get_azure_client(subscription_id)

        txt_value = set()
        try:
            existing_rr = client.record_sets.get(resource_group_name=resource_group_name,
                                                 zone_name=azure_domain,
                                                 relative_record_set_name=relative_validation_name,
                                                 record_type='TXT')
            for record in existing_rr.txt_records:
                for value in record.value:
                    txt_value.add(value)
        except HttpResponseError as err:
            if err.status_code != 404:  # Ignore RR not found
                raise errors.PluginError('Failed to check TXT record for domain '
                                         '{}, error: {}'.format(domain, err))

        txt_value -= {validation}

        try:
            if txt_value:
                client.record_sets.create_or_update(
                    resource_group_name=resource_group_name,
                    zone_name=azure_domain,
                    relative_record_set_name=relative_validation_name,
                    record_type='TXT',
                    parameters=RecordSet(ttl=self.ttl,
                                         txt_records=[TxtRecord(value=[v]) for v in txt_value])
                )
            else:
                client.record_sets.delete(
                    resource_group_name=resource_group_name,
                    zone_name=azure_domain,
                    relative_record_set_name=relative_validation_name,
                    record_type='TXT'
                )
        except HttpResponseError as err:
            if err.status_code != 404:  # Ignore RR not found
                raise errors.PluginError('Failed to remove TXT record for domain '
                                         '{}, error: {}'.format(domain, err))

    def _get_azure_client(self, subscription_id):
        """
        Gets azure DNS client

        :param subscription_id: Azure subscription ID
        :type subscription_id: str
        :return: Azure DNS client
        :rtype: DnsManagementClient
        """
        return DnsManagementClient(self.credential, subscription_id, None, self._arm_endpoint, credential_scopes=[self._arm_endpoint + "/.default"])
