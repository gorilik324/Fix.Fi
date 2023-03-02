import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Link from 'next/link'

export default function NavBar() {

  return (
    <div className='row'>
      <div className='col'>
        <div className='card'>
          <Navbar variant="light">
            <Container style={{ marginLeft: '10px', marginRight: '10px', width: '100%' }}>
              <Navbar.Brand style={{fontSize: '20px'}}>
                Fix.Fi
                <p style={{fontSize: '12px', margin: '0px'}}>
                Automating the detection and prediction of crypto-currency pump and dumps. 
                </p>
                </Navbar.Brand>
            </Container>
            <Nav >
              <Navbar.Text>
                <p style={{margin: '0px', width: '300px'}}></p>
                <p style={{margin: '0px', width: '300px'}}>
                </p>
              </Navbar.Text>
            </Nav>
          </Navbar>
        </div>
      </div>
    </div>
  )
}