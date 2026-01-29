# CreatePlaybackIDDomains

Restrictions based on the originating domain of a request (for example, whether requests from certain websites should be allowed or blocked).


## Fields

| Field                                                                      | Type                                                                       | Required                                                                   | Description                                                                |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `default_policy`                                                           | [Optional[models.PolicyAction]](../models/policyaction.md)                 | :heavy_minus_sign:                                                         | Policy action type                                                         |
| `allow`                                                                    | List[*str*]                                                                | :heavy_minus_sign:                                                         | A list of domains that are explicitly allowed access.                      |
| `deny`                                                                     | List[*str*]                                                                | :heavy_minus_sign:                                                         | A list of domains that are explicitly blocked from accessing the resource. |