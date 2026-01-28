# WatermarkInput

Contains configuration details for applying a watermark overlay to a video.  
The watermark is placed over the media content during processing.  
For detailed setup steps and customization options, refer to the 
<a href="https://docs.fastpix.io/docs/watermark-your-videos" target="_blank">FastPix Watermark Guide</a>.



## Fields

| Field                                                        | Type                                                         | Required                                                     | Description                                                  | Example                                                      |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `type`                                                       | [models.WatermarkInputType](../models/watermarkinputtype.md) | :heavy_check_mark:                                           | Type of overlay (currently only supports "watermark").       | watermark                                                    |
| `url`                                                        | *str*                                                        | :heavy_check_mark:                                           | URL of the watermark image.                                  | https://static.fastpix.io/watermark-4k.png                   |
| `placement`                                                  | [Optional[models.Placement]](../models/placement.md)         | :heavy_minus_sign:                                           | N/A                                                          |                                                              |
| `width`                                                      | *Optional[str]*                                              | :heavy_minus_sign:                                           | Width of the watermark in percentage or pixels.              | 25%                                                          |
| `height`                                                     | *Optional[str]*                                              | :heavy_minus_sign:                                           | Height of the watermark in percentage or pixels.             | 25%                                                          |
| `opacity`                                                    | *Optional[str]*                                              | :heavy_minus_sign:                                           | Opacity of the watermark in percentage.                      | 80%                                                          |