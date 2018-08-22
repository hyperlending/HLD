from .account import Account
from .exceptions import VestingBalanceDoesNotExistsException
from .blockchainobject import BlockchainObject


class Vesting(BlockchainObject):
    """ Read data about a Vesting Balance in the chain

        :param str id: Id of the vesting balance
        :param HLD HLD_instance: HLD() instance to use when accesing a RPC

    """
    type_id = 13

    def refresh(self):
        obj = self.HLD.rpc.get_objects([self.identifier])[0]
        if not obj:
            raise VestingBalanceDoesNotExistsException
        super(Vesting, self).__init__(obj, HLD_instance=self.HLD)

    @property
    def account(self):
        return Account(self["owner"], HLD_instance=self.HLD)

    @property
    def claimable(self):
        from .amount import Amount
        if self["policy"][0] == 1:
            p = self["policy"][1]
            ratio = (
                (float(p["coin_seconds_earned"]) /
                    float(self["balance"]["amount"])) /
                float(p["vesting_seconds"])
            ) if float(p["vesting_seconds"]) > 0.0 else 1
            return Amount(
                self["balance"],
                HLD_instance=self.HLD
            ) * ratio
        else:
            raise NotImplementedError("This policy isn't implemented yet")

    def claim(self, amount=None):
        return self.HLD.vesting_balance_withdraw(
            self["id"],
            amount=amount,
            account=self["owner"]
        )
