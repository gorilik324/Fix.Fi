import React, { useEffect, useState } from "react";
import { AdvancedRealTimeChart } from "react-ts-tradingview-widgets";


export default function TradingViewChart({ symbol, confidence }) {

  const styles = {
    parent: {
      fontSize: "0px",
      color: "red",
    },
    link: {
      textDecoration: "line-trough",
    },
    span: {
      color: "darkblue",
    },
  };

  const [chart, setChart] = useState(null);

  useEffect(() => {
    const widgetChart = (
      <div className="card" style={{ height: '272px', borderRadius: '10px' }}>
        <div className="card-title" style={{ margin: '0px', textAlign: 'center' }}>
          {symbol}  -  Confidence: {confidence?.toFixed(3)}%
        </div>
        <div className="card-body">
          <AdvancedRealTimeChart interval={'1'} symbol={symbol} copyrightStyles={styles} style='3' hide_side_toolbar={true} hide_top_toolbar={true} hide_legend={true} autosize theme="light" ></AdvancedRealTimeChart>
        </div>
      </div>);
    setChart(widgetChart);
  }, [symbol, confidence]);

  return chart
}

