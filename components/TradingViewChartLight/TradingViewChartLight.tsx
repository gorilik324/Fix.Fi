import { createChart } from 'lightweight-charts';
import React, { useEffect, useRef, useState } from 'react';
import { timeToWrt } from '../../utils/parsing';
import Button from 'react-bootstrap/Button';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Popover from 'react-bootstrap/Popover';
import { symbol } from 'd3';

export default function TradingViewChartLight({ title, data, wrt }) {

  //Setting initial values
  let values = []
  data.forEach(obs => {
    values.push({
      value: obs[wrt],
      time: obs.Close_Time / 1000
    })
  })

  //Setting initial values
  let volume = []
  data.forEach(obs => {
    if(obs.Close > obs.Open){
      volume.push({
        value: obs['Quote_Asset_Volume'],
        time: (obs.Close_Time / 1000),
        color: 'rgba(0, 150, 136, 0.5)'
      })
    }
    else{
      volume.push({
        value: obs['Quote_Asset_Volume'],
        time: (obs.Close_Time / 1000),
        color: 'rgba(255,82,82, 0.5)'
      })
    }
  })

  const chartContainerRef = useRef(null);
  const areaSeriesReplication = useRef(null)
  const volumeReplication = useRef(null)


  //Width and span of the input option for eth invested. 
  const popover = (
    <Popover style={{ boxShadow: '0 0 1.25rem rgb(31 45 61 / 25%)' }} id="popover-basic">
      <Popover.Header as="p">What are {title}?</Popover.Header>
      <Popover.Body as='p' style={{ fontSize: '11.5px' }}>
        Hey
      </Popover.Body>
    </Popover>
  );


  //Setting initial time on crosshairs
  console.log(data)
  const [crossHairTime, setCrossHairTime] = useState(data.slice(-1)[0]?.Close_Time)

  useEffect(() => {
    if (areaSeriesReplication.current !== null) {
      areaSeriesReplication.current.setData(values)
      volumeReplication.current.setData(volume)
    }
  }, [data])

  console.log(volume)


  useEffect(
    () => {
      setCrossHairTime(data.slice(-1)[0]?.Close_Time)
      if (values.length > 2) {

        console.log(values)

        if (!areaSeriesReplication.current) {
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
            topColor: 'rgba(255, 1, 1, 0.4)',
            bottomColor: 'rgba(255, 0, 0, 0.0)',
            lineColor: 'rgba(55, 1, 1, 1.0)',
            lineWidth: 3,
            priceFormat: {
              type: "price",
              minMove: Math.pow(10, -3),
              precision: 4
            },
            lastPriceAnimation: 0
          });
          areaSeries.setData(values)
          areaSeriesReplication.current = areaSeries //Replication set here for use later...


          var volumeSeries = chart.addHistogramSeries({
            color: '#26a69a',
            priceFormat: {
              type: 'volume',
            },
            priceScaleId: '',
            scaleMargins: {
              top: 0.9,
              bottom: 0.02
            },
          });
          volumeSeries.setData(volume)
          volumeReplication.current = volumeSeries //Replication set here for use later...

          //ToolTip
          function myCrosshairMoveHandler(param) {
            if (!param.point) {
              return;
            }
            if (param.time && values) {
              setCrossHairTime(param.time * 1000)
            }
          }
          chart.subscribeCrosshairMove(myCrosshairMoveHandler);
        }
        else{
          areaSeriesReplication.current.setData(values)
          volumeReplication.current.setData(volume)
        }
      }
    }, [data]);


  return (
    <div>
      <div className='row'>
        <div className='col-4'>
          <h1 style={{ fontSize: '35px', position: 'absolute', zIndex: 999, left: '10px', top: '20px' }}>{Number(timeToWrt(crossHairTime, wrt, data))}</h1>
          <h5 style={{ position: 'absolute', zIndex: 999, left: '10px', top: '60px', width: '100%' }}>{(new Date(crossHairTime)).toString().slice(0, -30)}</h5>
        </div>
        <div className='col-4'>
          <h5 style={{ position: 'absolute', zIndex: 999, left: '10px', top: '5px' }}>{title}: {data[0]?.Symbol}
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
