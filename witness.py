from HLD.instance import shared_HLD_instance
from .account import Account
from .exceptions import WitnessDoesNotExistsException
from .blockchainobject import BlockchainObject


class Witness(BlockchainObject):
    """ Read data about a witness in the chain

        :param str account_name: Name of the witness
        :param HLD HLD_instance: HLD() instance to use when
               accesing a RPC

    """
    type_ids = [6, 2]

    def refresh(self):
        if self.test_valid_objectid(self.identifier):
            _, i, _ = self.identifier.split(".")
            if int(i) == 6:
                witness = self.HLD.rpc.get_object(self.identifier)
            else:
                witness = self.HLD.rpc.get_witness_by_account(
                    self.identifier)
        else:
            account = Account(
                self.identifier, HLD_instance=self.HLD)
            witness = self.HLD.rpc.get_witness_by_account(account["id"])
        if not witness:
            raise WitnessDoesNotExistsException
        super(Witness, self).__init__(witness, HLD_instance=self.HLD)

    @property
    def account(self):
        return Account(self["witness_account"], HLD_instance=self.HLD)


class Witnesses(list):
    """ Obtain a list of **active** witnesses and the current schedule

        :param HLD HLD_instance: HLD() instance to use when
            accesing a RPC
    """
    def __init__(self, HLD_instance=None):
        self.HLD = HLD_instance or shared_HLD_instance()
        self.schedule = self.HLD.rpc.get_object(
            "2.12.0").get("current_shuffled_witnesses", [])

        super(Witnesses, self).__init__(
            [
                Witness(x, lazy=True, HLD_instance=self.HLD)
                for x in self.schedule
            ]
        )
