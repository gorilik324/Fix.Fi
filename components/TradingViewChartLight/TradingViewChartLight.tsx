import { createChart } from 'lightweight-charts';
import React, { useEffect, useRef, useState } from 'react';
import { timeToWrt } from '../../utils/parsing';
import Button from 'react-bootstrap/Button';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Popover from 'react-bootstrap/Popover';

export default function TradingViewChartLight({ title, info, data, latestData, wrt }) {

  const chartContainerRef = useRef(null);
  const [fullData, setFullData] = useState(data)

  //Width and span of the input option for eth invested. 
  const popover = (
    <Popover style={{ boxShadow: '0 0 1.25rem rgb(31 45 61 / 25%)' }} id="popover-basic">
      <Popover.Header as="p">What are {title}?</Popover.Header>
      <Popover.Body as='p'style={{fontSize:'11.5px'}}>
        {info}
      </Popover.Body>
    </Popover>
  );

  //Updaing of chart on new data (using a reference replicaiton created within the below use effect. )
  const areaSeriesReplication = useRef(null)
  useEffect(() => {
    if (areaSeriesReplication.current !== null) {
      if (latestData.TIMESTAMP > fullData.slice(-1)[0].TIMESTAMP) {
        console.log(latestData)
        areaSeriesReplication.current.update({
          value: latestData[wrt],
          time: latestData.TIMESTAMP > fullData.slice(-1)[0].TIMESTAMP ? latestData.TIMESTAMP : fullData.slice(-1)[0].TIMESTAMP
        })
      }
    }
    setFullData(fullData => [...fullData, latestData])
  }, [latestData, wrt])


  //Setting initial values
  let values = []
  data.forEach(obs => {
    values.push({
      value: obs[wrt],
      time: obs.Close_Time
    })
  })

  //Setting initial time on crosshairs
  console.log(data)
  const [crossHairTime, setCrossHairTime] = useState(data.slice(-1)[0]?.Close_Time)

  useEffect(
    () => {
      setCrossHairTime(data.slice(-1)[0]?.Close_Time)
      if (values.length > 2) {

        console.log(values)
        const chart = createChart(chartContainerRef.current, {
          width: chartContainerRef.current.clientWidth - 20,
          height: 320,
          layout: {
            fontFamily: 'sans-serif',
          },
          rightPriceScale: {
            scaleMargins: {
              top: 0.35,
              bottom: 0.2,
            },
            borderVisible: false,
          },
          timeScale: {
            borderVisible: false,
          },
          grid: {
            horzLines: {
              color: '#eee',
              visible: false,
            },
            vertLines: {
              color: '#ffffff',
            },
          },
          crosshair: {
            horzLine: {
              visible: false,
              labelVisible: false
            },
            vertLine: {
              visible: true,
              style: 0,
              width: 2,
              color: 'rgba(32, 38, 46, 0.1)',
              labelVisible: false,
            }
          },
        });
        chart.timeScale().fitContent()
        const areaSeries = chart.addAreaSeries({
          topColor: 'rgba(1, 1, 1, 0.4)',
          bottomColor: 'rgba(0, 0, 0, 0.0)',
          lineColor: 'rgba(1, 1, 1, 1.0)',
          lineWidth: 3,
          priceFormat: {
            type: "price",
            minMove: Math.pow(10, -3),
            precision: 4
          },
          lastPriceAnimation: 2
        });
        areaSeries.setData(values)
        areaSeriesReplication.current = areaSeries //Replication set here for use later...

        //ToolTip
        function myCrosshairMoveHandler(param) {
          if (!param.point) {
            return;
          }
          if (param.time && values) {
            setCrossHairTime(param.time)
          }
        }
        chart.subscribeCrosshairMove(myCrosshairMoveHandler);
      }
    }, [data]);


  console.log((timeToWrt(crossHairTime, wrt, fullData)))

  return (
    <div>
      <div className='row'>
        <div className='col-4'>
          <h1 style={{ fontSize: '35px', position: 'absolute', zIndex: 999, left: '10px', top: '20px' }}>{Number(timeToWrt(crossHairTime, wrt, data)).toFixed(3)}</h1>
          <h5 style={{ position: 'absolute', zIndex: 999, left: '10px', top: '60px', width: '100%' }}>{(new Date(crossHairTime)).toString().slice(0, -30)}</h5>
        </div>
        <div className='col-4'>
          <h5 style={{ position: 'absolute', zIndex: 999, left: '10px', top: '5px' }}>{title}
          <OverlayTrigger trigger="click" placement="bottom" overlay={popover}>
              <Button style={{ padding: '0px 10px', border: '0px', marginLeft: '5px' }} variant="info">i</Button>
          </OverlayTrigger>
          </h5>
        </div>
      </div>
      <div style={{ borderRadius: '10px', overflow: 'hidden' }} ref={chartContainerRef} />
    </div>
  );
};
