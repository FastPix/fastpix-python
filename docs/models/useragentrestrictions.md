# UserAgentRestrictions

Restrictions based on the user agent


## Fields

| Field                                                      | Type                                                       | Required                                                   | Description                                                |
| ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| `default_policy`                                           | [Optional[models.PolicyAction]](../models/policyaction.md) | :heavy_minus_sign:                                         | Policy action type                                         |
| `allow`                                                    | List[*str*]                                                | :heavy_minus_sign:                                         | A list of user agents that are explicitly allowed access   |
| `deny`                                                     | List[*str*]                                                | :heavy_minus_sign:                                         | A list of user agents that are explicitly denied access    |