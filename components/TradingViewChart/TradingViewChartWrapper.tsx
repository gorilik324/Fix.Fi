import dynamic from "next/dynamic";

const TradingViewChart = dynamic(() => import("./TradingViewChart"), {
  ssr: false
});

export default TradingViewChart;
