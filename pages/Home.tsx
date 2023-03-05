
import { Button, Table } from 'react-bootstrap'
import TradingViewChart from '../components/TradingViewChart/TradingViewChartWrapper'
import TradingViewChartLight from '../components/TradingViewChartLight/TradingViewChartLightWrapper'
import { useEffect, useState } from 'react'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Popover from 'react-bootstrap/Popover';


//Pausing function
export default function Home({ pumpData }) {

  const [identifierChartData, setIdentifierChartData] = useState([])

  useEffect(() => {
    async function getData() {
      //pumpData[-1].window etc is used here...
      const fabricated = { symbol: 'ETHUSDT', pumpTime: 1676835000000 }
      //window here is 30
      const res = await fetch(`https://api.binance.com/api/v3/klines?symbol=${fabricated.symbol}&interval=1m&startTime=${fabricated.pumpTime - (60000 * 20)}&endTime=${fabricated.pumpTime + (60000 * 20)}`)
      const orders = await res.json()
      let propperArray: Array<Object> = []
      orders.forEach(row => {
        propperArray.push({
          Open_Time: row[0],
          Open: row[1],
          High: row[2],
          Low: row[3],
          Close: row[4],
          Volume: row[5],
          Close_Time: row[6],
          Quote_Asset_Volume: row[7],
          Number_Of_Trades: row[8],
          Taker_Buy_Base_Asset_Volume: row[9],
          Taker_Buy_Quote_Asset_Volume: row[10],
          Ignore: row[11]
        })
      });
      setIdentifierChartData(propperArray)
    }
    getData()
  }, [])

  console.log(identifierChartData)

  //Width and span of the input option for eth invested. 
  const popover = (
    <Popover style={{ boxShadow: '0 0 1.25rem rgb(31 45 61 / 25%)' }} id="popover-basic">
      <Popover.Header as="p">How are pumps predicted?</Popover.Header>
      <Popover.Body as='p'style={{fontSize:'11.5px'}}>
        {'This is how'}
      </Popover.Body>
    </Popover>
  );

  return (
    <>
      <div className='row'>
        <div className='col-4'>
          <div className="container" style={{ margin: '0px', maxWidth: '100%', background: 'rgba(0,0,200,0.2)', paddingTop: '12px', borderRadius: '10px', marginBottom: '15px' }}>
            <h3 className="card-title" style={{ marginBottom: '15px' }}>
              Anomaly Detection
              <Button disabled variant='success' style={{ marginLeft: '10px' }}>
                Live
              </Button>
            </h3>
            <div className='row'>
              <div className='col'>
                <div className='card'>
                  <TradingViewChartLight
                    info={'Null Funds are the funds not available for withdrawal to investors. Upon expiry of The Null Fund, these funds are distributed to the current investors. These funds are locked, and are the reason for the higher returns of the system.'}
                    title={'Recently Identified Pump'} data={identifierChartData} latestData={[]} wrt={'Close'} />
                  <div style={{ height: '245px', overflowX: 'scroll', padding: '5px' }}>
                    <Table>
                      <thead style={{ position: 'sticky', top: 0 }}>
                        <tr style={{ background: 'white' }}>
                          <th>Pair</th>
                          <th>Time</th>
                          <th>Size</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                        </tr>
                        <tr>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                        </tr>
                        <tr>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                        </tr>
                        <tr>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                        </tr>
                        <tr>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                        </tr>
                        <tr>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                        </tr>
                        <tr>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                        </tr>
                        <tr>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                        </tr>
                        <tr>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                        </tr>
                        <tr>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                        </tr>
                        <tr>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                        </tr>
                        <tr>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                          <td>{'2'}</td>
                        </tr>
                      </tbody>
                    </Table>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className='col-8'>
          <div className="container" style={{ margin: '0px', maxWidth: '100%', background: 'rgba(250,0,0,0.2)', paddingTop: '12px', borderRadius: '10px', marginBottom: '15px' }}>
            <h3 className="card-title" style={{ marginBottom: '15px' }}>
              Pump Predictor
              <OverlayTrigger trigger="click" placement="bottom" overlay={popover}>
              <Button style={{ padding: '0px 10px', border: '0px', marginLeft: '5px' }} variant="info">i</Button>
              </OverlayTrigger>
              <Button disabled variant='success' style={{ marginLeft: '10px' }}>
                Live
              </Button>
            </h3>
            <div className="row">
              <div className='col-6'>
                <TradingViewChart symbol={'BTCUSDT'}/>
              </div>
              <div className='col-6'>
                <TradingViewChart symbol={'BTCUSDT'} />
              </div>
            </div>
            <div className="row">
              <div className='col-6'>
                <TradingViewChart symbol={'BTCUSDT'} />
              </div>
              <div className='col-6'>
                <TradingViewChart symbol={'BTCUSDT'} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

export const getServerSideProps = async () => {
  //Make an Supabase call for the most reccent 100 pump rows and 4 predictions.
  // pumpData = ...
  return {
    props: { pumpData }
  }
}


