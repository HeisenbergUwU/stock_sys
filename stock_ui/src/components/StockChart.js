import React from "react";
import {
  ChartCanvas,
  Chart,
  series,
  coordinates,
  axes,
  utils,
  indicators,
  tooltip,
  CrossHairCursor,
} from "react-financial-charts";
import { discontinuousTimeScaleProviderBuilder } from "@react-financial-charts/scales";

// 解构需要用到的部分
const { CandlestickSeries, LineSeries } = series;
const { XAxis, YAxis } = axes;
const { MouseCoordinateX, MouseCoordinateY } = coordinates;
const { ema, sma } = indicators;
const { format } = utils;

const StockChart = ({
  data,
  width = 800,
  height = 400,
  margin = { left: 50, right: 50, top: 10, bottom: 30 },
}) => {
  // 转换时间到 Date 类型
  const parsedData = data.map((d) => ({
    date: new Date(d.date),
    open: d.open,
    high: d.high,
    low: d.low,
    close: d.close,
    volume: d.volume,
  }));

  // 指定 x 访问器
  const xAccessor = (d) => d.date;
  const xScaleProvider =
    discontinuousTimeScaleProviderBuilder().inputDateAccessor(xAccessor);
  const {
    data: chartData,
    xScale,
    xAccessor: finalXAccessor,
    displayXAccessor,
  } = xScaleProvider(parsedData);

  // y 范围设为价格 high/low
  const yExtents = (d) => [d.high, d.low];

  // 定义一个简单的 SMA，比如 10 天
  const sma10 = sma()
    .id(0)
    .options({ windowSize: 10 })
    .merge((d, c) => {
      d.sma10 = c;
    })
    .accessor((d) => d.sma10);

  return (
    <ChartCanvas
      height={height}
      width={width}
      ratio={window.devicePixelRatio}
      margin={margin}
      data={chartData}
      seriesName="Stock Data"
      xScale={xScale}
      xAccessor={finalXAccessor}
      displayXAccessor={displayXAccessor}
      xExtents={[parsedData.length - 100, parsedData.length - 1]} // 显示最后 100 个点
    >
      <Chart id={1} yExtents={(d) => [d.high, d.low, sma10.accessor()(d)]}>
        <XAxis />
        <YAxis />

        {/* 蜡烛图 */}
        <CandlestickSeries />

        {/* SMA 线 */}
        <LineSeries yAccessor={sma10.accessor()} stroke={sma10.stroke()} />

        {/* 坐标辅助线显示当前鼠标位置 */}
        <MouseCoordinateX displayFormat={format.dateFormat("%Y-%m-%d")} />
        <MouseCoordinateY displayFormat={format.format(".2f")} />
      </Chart>

      <CrossHairCursor />
    </ChartCanvas>
  );
};

export default StockChart;
