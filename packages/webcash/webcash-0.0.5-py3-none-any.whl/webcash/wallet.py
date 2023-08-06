"""
Webcash wallet
"""

# TODO: decorator for check_legal_agreements
# TODO: generate_new_secret
# TODO: remove user interaction from setup(), move that to CLI client
# TODO: insert, insertmany, pay, merge, check, recover, get info

import os
import json
import requests
import secrets

from .webcashbase import (
    SecretWebcash,
    PublicWebcash,
    LEGALESE,
    amount_to_str as _amount_to_str,
    check_legal_agreements as _check_legal_agreements,
    deserialize_amount as _deserialize_amount,
    WEBCASH_ENDPOINT_HEALTH_CHECK,
    WEBCASH_ENDPOINT_REPLACE,
)

CHAIN_CODES = {
    "RECEIVE": 0,
    "PAY": 1,
    "CHANGE": 2,
    "MINING": 3,
}

def _generate_initial_legalese():
    legalese = {disclosure_name: None for disclosure_name in LEGALESE.keys()}
    return legalese

def _generate_initial_walletdepths():
    """
    Setup the walletdepths object all zeroed out for each of the chaincodes.
    """
    return {key.upper(): 0 for key in CHAIN_CODES.keys()}

def _generate_new_master_secret():
    """
    Generate a new random master secret for a deterministic wallet.
    """
    return secrets.token_hex(32)

def _yes_or_no(question):
    while "the user failed to choose y or n":
        reply = str(input(question + " (y/n): ")).lower().strip()
        if reply[:1] == "y":
            return True
        if reply[:1] == "n":
            return False

class WebcashWallet:

    def __init__(self,
                 webcash=None,
                 unconfirmed=None,
                 master_secret=None,
                 walletdepths=None,
                 legalese=None,
                 log=None,
                 version=None,
                 filepath=None,
    ):
        if webcash is None:
            webcash = []

        if unconfirmed is None:
            unconfirmed = []

        if walletdepths is None:
            walletdepths = _generate_initial_walletdepths()

        if master_secret is None:
            print("Generating a new master secret for the wallet (none previously detected)")
            master_secret = _generate_new_master_secret()
            print("Be sure to backup your wallet for safekeeping of its master secret.")

        if log is None:
            log = []

        if legalese is None:
            legalese = _generate_initial_legalese()

        if version is None:
            version = "1.0"
        elif version != "1.0":
            raise Exception("Unknown wallet version.")

        self.webcash = webcash
        self.unconfirmed = unconfirmed
        self.walletdepths = walletdepths
        self.log = log
        self.legalese = legalese
        self.master_secret = master_secret
        self.filepath = filepath
        self.version = version

    def check_legal_agreements(self):
        acknowledgements = self.legalese.items()
        expected = LEGALESE.keys()
        has_expected = all([expectation in self.legalese.keys() for expectation in expected])
        agreement = all(ack[1] == True for ack in acknowledgements)
        return has_expected and agreement

    def setup(self, legalese=None):
        if legalese is not None:
            self.legalese = legalese
        acks = self.check_legal_agreements()
        if acks:
            print("User has already agreed and acknowledged the disclosures.")
        elif not acks:
            self.legalese = {}
            for (disclosure_name, disclosure) in LEGALESE.items():
                print(f"Disclosure \"{disclosure_name}\": {disclosure}")
                print("\n\n")
                answer = _yes_or_no(f"Do you agree?")

                if answer == False:
                    print(f"Unfortunately, you must acknowledge and agree to all agreements to use webcash.")
                    continue
                elif answer == True:
                    self.legalese[disclosure_name] = True
                    continue

        self.save()
        print("\n\n\nAll done! You've acknowledged all the disclosures. You may now use webcash.")

    def to_dict(self):
        return {
            "webcash": self.webcash,
            "unconfirmed": self.unconfirmed,
            "walletdepths": self.walletdepths,
            "log": self.log,
            "legalese": self.legalese,
            "master_secret": self.master_secret,
            "version": self.version,
        }

    @classmethod
    def load(cls, filepath):
        data = json.loads(open(filepath, "r").read())
        data["filepath"] = filepath
        wallet = Wallet(**data)
        return wallet

    def save(self, filepath=None):
        if filepath is None:
            filepath = self.filepath

        temporary_filename = f"{filepath}.{os.getpid()}"
        with open(temporary_filename, "w") as fd:
            fd.write(json.dumps(self.to_dict()))
        os.replace(temporary_filename, filepath)

