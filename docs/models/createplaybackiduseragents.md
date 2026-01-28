# CreatePlaybackIDUserAgents

Restrictions based on the user agent (which is typically a string sent by browsers or bots identifying themselves).


## Fields

| Field                                                                   | Type                                                                    | Required                                                                | Description                                                             |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `default_policy`                                                        | [Optional[models.PolicyAction]](../models/policyaction.md)              | :heavy_minus_sign:                                                      | Policy action type                                                      |
| `allow`                                                                 | List[*str*]                                                             | :heavy_minus_sign:                                                      | A list of specific user agents that are allowed to access the resource. |
| `deny`                                                                  | List[*str*]                                                             | :heavy_minus_sign:                                                      | A list of specific user agents that are blocked.                        |