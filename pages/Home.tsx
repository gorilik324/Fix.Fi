
import { Button, Table } from 'react-bootstrap'
import TradingViewChart from '../components/TradingViewChart/TradingViewChartWrapper'

//Pausing function
export default function Home({ }) {
  return (
    <>
      <div className='row'>
        <div className='col-4'>
          <div className="container" style={{ margin: '0px', maxWidth: '100%', background: 'rgba(0,0,200,0.2)', paddingTop: '12px', borderRadius: '10px', marginBottom: '15px' }}>
            <h3 className="card-title" style={{ marginBottom: '15px' }}>
              Anomaly Detection
              <Button disabled variant='success' style={{marginLeft: '10px'}}>
                Live
              </Button>
            </h3>
            <div className='row'>
              <div className='col'>
                <div className='card'>
                <Table striped hover>
                <thead>
                  <tr>
                    <th>#</th>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Username</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>1</td>
                    <td>Mark</td>
                    <td>Otto</td>
                    <td>@mdo</td>
                  </tr>
                  <tr>
                    <td>2</td>
                    <td>Jacob</td>
                    <td>Thornton</td>
                    <td>@fat</td>
                  </tr>
                  <tr>
                    <td>3</td>
                    <td colSpan={2}>Larry the Bird</td>
                    <td>@twitter</td>
                  </tr>
                  <tr>
                    <td>1</td>
                    <td>Mark</td>
                    <td>Otto</td>
                    <td>@mdo</td>
                  </tr>
                  <tr>
                    <td>2</td>
                    <td>Jacob</td>
                    <td>Thornton</td>
                    <td>@fat</td>
                  </tr>
                  <tr>
                    <td>3</td>
                    <td colSpan={2}>Larry the Bird</td>
                    <td>@twitter</td>
                  </tr>
                  <tr>
                    <td>1</td>
                    <td>Mark</td>
                    <td>Otto</td>
                    <td>@mdo</td>
                  </tr>
                  <tr>
                    <td>2</td>
                    <td>Jacob</td>
                    <td>Thornton</td>
                    <td>@fat</td>
                  </tr>
                  <tr>
                    <td>3</td>
                    <td colSpan={2}>Larry the Bird</td>
                    <td>@twitter</td>
                  </tr>
                  <tr>
                    <td>1</td>
                    <td>Mark</td>
                    <td>Otto</td>
                    <td>@mdo</td>
                  </tr>
                  <tr>
                    <td>2</td>
                    <td>Jacob</td>
                    <td>Thornton</td>
                    <td>@fat</td>
                  </tr>
                  <tr>
                    <td>3</td>
                    <td colSpan={2}>Larry the Bird</td>
                    <td>@twitter</td>
                  </tr>
                  <tr>
                    <td>1</td>
                    <td>Mark</td>
                    <td>Otto</td>
                    <td>@mdo</td>
                  </tr>
                  <tr>
                    <td>2</td>
                    <td>Jacob</td>
                    <td>Thornton</td>
                    <td>@fat</td>
                  </tr>
                  <tr>
                    <td>3</td>
                    <td colSpan={2}>Larry the Bird</td>
                    <td>@twitter</td>
                  </tr>
                  <tr>
                    <td>1</td>
                    <td>Mark</td>
                    <td>Otto</td>
                    <td>@mdo</td>
                  </tr>
                  <tr>
                    <td>2</td>
                    <td>Jacob</td>
                    <td>Thornton</td>
                    <td>@fat</td>
                  </tr>
                  <tr>
                    <td>3</td>
                    <td colSpan={2}>Larry the Bird</td>
                    <td>@twitter</td>
                  </tr>
                </tbody>
              </Table>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className='col-8'>
          <div className="container" style={{ margin: '0px', maxWidth: '100%', background: 'rgba(250,0,0,0.2)', paddingTop: '12px', borderRadius: '10px', marginBottom: '15px' }}>
            <h3 className="card-title" style={{ marginBottom: '15px' }}>
              Pump Predictor
            </h3>
            <div className="row">
              <div className='col-6'>
              <TradingViewChart/>
              </div>
              <div className='col-6'>
              <TradingViewChart/>
              </div>
            </div>
            <div className="row">
              <div className='col-6'>
              <TradingViewChart/>
              </div>
              <div className='col-6'>
              <TradingViewChart/>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}