# CreatePlaylistRequestMetadata

Required when playlist type is smart - media created between startDate and endDate of createdDate will be add, similarily updatedDate (Optional)


## Fields

| Field                                                | Type                                                 | Required                                             | Description                                          |
| ---------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- |
| `created_date`                                       | [Optional[models.DateRange]](../models/daterange.md) | :heavy_minus_sign:                                   | Date range with start and end dates.                 |
| `updated_date`                                       | [Optional[models.DateRange]](../models/daterange.md) | :heavy_minus_sign:                                   | Date range with start and end dates.                 |