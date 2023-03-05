import dynamic from "next/dynamic";

const TradingViewChart = dynamic(() => import("./TradingViewChartLight"), {
  ssr: false
});

export default TradingViewChart;
