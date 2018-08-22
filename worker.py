from HLD.instance import shared_HLD_instance
from .account import Account
from .exceptions import WorkerDoesNotExistsException
from .utils import formatTimeString
from .blockchainobject import BlockchainObject


class Worker(BlockchainObject):
    """ Read data about a worker in the chain

        :param str id: id of the worker
        :param HLD HLD_instance: HLD() instance to use when
            accesing a RPC

    """
    type_id = 14

    def refresh(self):
        worker = self.HLD.rpc.get_object(self.identifier)
        if not worker:
            raise WorkerDoesNotExistsException
        worker["work_end_date"] = formatTimeString(worker["work_end_date"])
        worker["work_begin_date"] = formatTimeString(worker["work_begin_date"])
        super(Worker, self).__init__(worker, HLD_instance=self.HLD)
        self.cached = True

    @property
    def account(self):
        return Account(
            self["worker_account"], HLD_instance=self.HLD)


class Workers(list):
    """ Obtain a list of workers for an account

        :param str account_name/id: Name/id of the account (optional)
        :param HLD HLD_instance: HLD() instance to use when
            accesing a RPC
    """
    def __init__(self, account_name=None, HLD_instance=None):
        self.HLD = HLD_instance or shared_HLD_instance()
        if account_name:
            account = Account(account_name, HLD_instance=self.HLD)
            self.workers = self.HLD.rpc.get_workers_by_account(
                account["id"])
        else:
            self.workers = self.HLD.rpc.get_all_workers()

        super(Workers, self).__init__(
            [
                Worker(x, lazy=True, HLD_instance=self.HLD)
                for x in self.workers
            ]
        )
