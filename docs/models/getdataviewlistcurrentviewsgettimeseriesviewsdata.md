# GetDataViewlistCurrentViewsGetTimeseriesViewsData


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `interval_time`                                                      | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_minus_sign:                                                   | The timestamp for the interval (ISO 8601 format).                    |
| `metric_value`                                                       | *OptionalNullable[int]*                                              | :heavy_minus_sign:                                                   | Reserved for future metric values (currently null).                  |
| `number_of_views`                                                    | *Optional[int]*                                                      | :heavy_minus_sign:                                                   | Number of concurrent viewers at the given interval.                  |