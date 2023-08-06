"""
Contains all utility functions
"""
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.subscription import SubscriptionClient
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class utils:
    def __init__(self, credentials: ClientSecretCredential):
        """
        :param credentials:  ClientSecretCredential object
        """
        self.credentials = credentials

    def list_subscriptions(self) -> list:
        """
        :param self:
        :return: list of Azure subscriptions
        """
        logger.info(" ---Inside utils :: list_subscriptions()--- ")

        subs_client = SubscriptionClient(credential=self.credentials)

        subs_list = subs_client.subscriptions.list()
        response = []
        for subs in subs_list:
            sid = subs.id
            response.append(sid.split('/')[-1])

        return response

    def list_vms(self, subscriptions: list) -> dict:
        """
        :param subscriptions: list of subscriptions
        :return: dictionary containing the list VMs
        """
        logger.info(" ---Inside utils :: list_vms()--- ")

        response = {}

        for subscription in subscriptions:
            compute_client = ComputeManagementClient(credential=self.credentials, subscription_id=subscription)
            vm_list = compute_client.virtual_machines.list_all()

            for vm in vm_list:
                response.setdefault(subscription, []).append(vm)

        return response

    # returns the list of disks across all the subscriptions
    def list_disks(self, subscriptions: list) -> dict:
        """
        :param subscriptions: list of subscriptions
        :return:
        """
        logger.info(" ---Inside utils :: list_disks()--- ")
        response = {}

        for subscription in subscriptions:
            compute_client = ComputeManagementClient(credential=self.credentials, subscription_id=subscription)
            disk_lst = compute_client.disks.list()

            for disk in disk_lst:
                response.setdefault(subscription, []).append(disk)

        return response

    # returns the list of snapshots
    def list_snapshots(self, subscriptions: list) -> dict:
        """
        :param subscriptions: list of azure subscriptions
        :return: list of snapshots
        """
        logger.info(" ---Inside utils :: list_snapshots()--- ")
        response = {}

        for subscription in subscriptions:
            compute_client = ComputeManagementClient(credential=self.credentials, subscription_id=subscription)
            snapshot_list = compute_client.snapshots.list()

            for snapshot in snapshot_list:
                response.setdefault(subscription, []).append(snapshot)

        return response

    '''***********************Incomplete'''
    # returns the list of load balancers across all subscriptions
    def list_load_balancers(self, subscriptions: list) -> dict:
        """
        :param subscriptions: list of subscription in an azure account
        :return: dictionary containing list of load balancers
        """
        logger.info(" ---Inside utils :: list_load_balancers()--- ")

        response = {}

        for subscription in subscriptions:
            client = NetworkManagementClient(credential=self.credentials, subscription_id=subscription)
            lb_list = client.load_balancers.list_all()
            for lb in lb_list:
                print(lb)

        return response

    # returns the list of NSG
    def list_nsg(self, subscriptions: list) -> dict:
        """
        :param subscriptions: list of subscriptions
        :return: dictionary containing list of nsg
        """
        logger.info(" ---Inside utils :: list_nsg()--- ")

        response = {}

        for subscription in subscriptions:
            client = NetworkManagementClient(credential=self.credentials, subscription_id=subscription)
            nsg_list = client.network_security_groups.list_all()

            for nsg in nsg_list:
                response.setdefault(subscription, []).append(nsg)

        return response
