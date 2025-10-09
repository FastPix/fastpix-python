# ListErrorsData

Displays the result of the request.


## Fields

| Field                                                                                                              | Type                                                                                                               | Required                                                                                                           | Description                                                                                                        |
| ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| `errors`                                                                                                           | List[[models.ErrorDetails](../models/errordetails.md)]                                                             | :heavy_minus_sign:                                                                                                 | Retrieves a list of errors that have occurred in the system.                                                       |
| `top_errors`                                                                                                       | List[[models.TopErrorDetails](../models/toperrordetails.md)]                                                       | :heavy_minus_sign:                                                                                                 | Retrieves a list of errors that have occurred most frequently in the system, ranked by their count of occurrences. |