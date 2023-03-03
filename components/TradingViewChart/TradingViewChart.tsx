import React, { useEffect } from "react";
import { AdvancedRealTimeChart } from "react-ts-tradingview-widgets";


export default function TradingViewChart(){

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


    return(
        <div className="card" style={{height: '275px', borderRadius: '5px'}}>
            <div className="card-title" style={{margin: '0px', textAlign: 'center'}}>
                VIA/BTC
            </div>
            <div className="card-body">
            <AdvancedRealTimeChart symbol="BTCUSDT" copyrightStyles={styles} style='3' hide_side_toolbar={true} hide_top_toolbar={true} hide_legend={true} autosize theme="light" ></AdvancedRealTimeChart>
            </div>
        </div>
    )
}

