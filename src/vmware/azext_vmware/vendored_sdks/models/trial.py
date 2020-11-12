# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class Trial(Model):
    """Subscription trial availability.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar status: Trial status. Possible values include: 'TrialAvailable',
     'TrialUsed', 'TrialDisabled'
    :vartype status: str or ~vendored_sdks.models.TrialStatus
    :ivar available_hosts: Number of trial hosts available
    :vartype available_hosts: int
    """

    _validation = {
        'status': {'readonly': True},
        'available_hosts': {'readonly': True},
    }

    _attribute_map = {
        'status': {'key': 'status', 'type': 'str'},
        'available_hosts': {'key': 'availableHosts', 'type': 'int'},
    }

    def __init__(self, **kwargs):
        super(Trial, self).__init__(**kwargs)
        self.status = None
        self.available_hosts = None