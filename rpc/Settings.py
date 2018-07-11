class SettingsHolder:
    """
    This class holds all the settings. Needs to be setup with one of the
    `setup` methods before using it.
    """
    RPC_LIST = None

    # Setup methods
    def setup(self, addr_list):
        """ Load settings from a JSON config file """
        self.RPC_LIST = addr_list

    def setup_mainnet(self):
        """ Load settings from the mainnet JSON config file """
        self.setup(
            [
                "seed1.ont.io:20336",
                "seed2.ont.io:20336",
                "seed3.ont.io:20336",
                "seed4.ont.io:20336",
                "seed5.ont.io:20336"
            ]
        )

    def setup_testnet(self):
        self.setup(
            [
                "polaris1.ont.io:20336",
                "polaris2.ont.io:20336",
                "polaris3.ont.io:20336",
                "polaris4.ont.io:20336"
            ]
        )

    def setup_privnet(self):
        self.setup(
            [
                "http://127.0.0.1:20336"
            ]
        )


# Settings instance used by external modules
settings = SettingsHolder()

# Load testnet settings as default
settings.setup_privnet()
