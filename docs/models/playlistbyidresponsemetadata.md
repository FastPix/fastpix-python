# PlaylistByIDResponseMetadata

Required when the playlist type is `smart`. Media created between `startDate` and `endDate` of `createdDate` is added. Optionally, you can include media based on `updatedDate`.


## Fields

| Field                                                | Type                                                 | Required                                             | Description                                          |
| ---------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- |
| `created_date`                                       | [Optional[models.DateRange]](../models/daterange.md) | :heavy_minus_sign:                                   | Date range with start and end dates.                 |
| `updated_date`                                       | [Optional[models.DateRange]](../models/daterange.md) | :heavy_minus_sign:                                   | Date range with start and end dates.                 |