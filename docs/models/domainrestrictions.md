# DomainRestrictions

Restrictions based on the originating domain of a request


## Fields

| Field                                                                 | Type                                                                  | Required                                                              | Description                                                           |
| --------------------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `default_policy`                                                      | [Optional[models.PolicyAction]](../models/policyaction.md)            | :heavy_minus_sign:                                                    | Policy action type                                                    |
| `allow`                                                               | List[*str*]                                                           | :heavy_minus_sign:                                                    | A list of domain names or patterns that are explicitly allowed access |
| `deny`                                                                | List[*str*]                                                           | :heavy_minus_sign:                                                    | A list of domain names or patterns that are explicitly denied access  |