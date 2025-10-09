# CreateMediaPlaybackIDAccessRestrictions


## Fields

| Field                                                                        | Type                                                                         | Required                                                                     | Description                                                                  |
| ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `domains`                                                                    | [Optional[models.DomainRestrictions]](../models/domainrestrictions.md)       | :heavy_minus_sign:                                                           | Restrictions based on the originating domain of a request                    |
| `user_agents`                                                                | [Optional[models.UserAgentRestrictions]](../models/useragentrestrictions.md) | :heavy_minus_sign:                                                           | Restrictions based on the user agent                                         |