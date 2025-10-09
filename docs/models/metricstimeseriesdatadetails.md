# MetricsTimeseriesDataDetails

The metric's value at specific time intervals.


## Fields

| Field                                                                           | Type                                                                            | Required                                                                        | Description                                                                     | Example                                                                         |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `interval_time`                                                                 | [date](https://docs.python.org/3/library/datetime.html#date-objects)            | :heavy_minus_sign:                                                              | The timestamp for the data point indicating when the metric value was recorded. | 2023-12-04T14:00:00.000Z                                                        |
| `metric_value`                                                                  | [OptionalNullable[models.MetricValue]](../models/metricvalue.md)                | :heavy_minus_sign:                                                              | The value of the specified metric at the given interval.                        | 0.793110142151515                                                               |
| `number_of_views`                                                               | *OptionalNullable[int]*                                                         | :heavy_minus_sign:                                                              | The total number of views recorded during that interval.                        | 143244                                                                          |