from .instance import shared_HLD_instance
from .account import Account
from .exceptions import ProposalDoesNotExistException
from .blockchainobject import BlockchainObject
import logging
log = logging.getLogger(__name__)


class Proposal(BlockchainObject):
    """ Read data about a Proposal Balance in the chain

        :param str id: Id of the proposal
        :param HLD HLD_instance: HLD() instance to use when accesing a RPC

    """
    type_id = 10

    def refresh(self):
        proposal = self.HLD.rpc.get_objects([self.identifier])
        if not any(proposal):
            raise ProposalDoesNotExistException
        super(Proposal, self).__init__(proposal[0], HLD_instance=self.HLD)

    @property
    def proposed_operations(self):
        yield from self["proposed_transaction"]["operations"]


class Proposals(list):
    """ Obtain a list of pending proposals for an account

        :param str account: Account name
        :param HLD HLD_instance: HLD() instance to use when accesing a RPC
    """
    def __init__(self, account, HLD_instance=None):
        self.HLD = HLD_instance or shared_HLD_instance()

        account = Account(account, HLD_instance=self.HLD)
        proposals = self.HLD.rpc.get_proposed_transactions(account["id"])

        super(Proposals, self).__init__(
            [
                Proposal(x, HLD_instance=self.HLD)
                for x in proposals
            ]
        )
