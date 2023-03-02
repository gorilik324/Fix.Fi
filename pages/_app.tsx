import * as React from 'react';
import { AppProps } from 'next/app';
import '../styles/main.min.scss'
import { Analytics } from '@vercel/analytics/react';
import { WagmiConfig, createClient, configureChains } from 'wagmi'
import { mainnet, goerli, hardhat } from 'wagmi/chains'

import { publicProvider } from 'wagmi/providers/public'

import { CoinbaseWalletConnector } from 'wagmi/connectors/coinbaseWallet'
import { InjectedConnector } from 'wagmi/connectors/injected'
import { MetaMaskConnector } from 'wagmi/connectors/metaMask'
import { WalletConnectConnector } from 'wagmi/connectors/walletConnect'

const { chains, provider } = configureChains(
  [mainnet, goerli, hardhat],
  [publicProvider()],
)

// Set up client
const client = createClient({
  autoConnect: false,
  connectors: [
    new MetaMaskConnector({ chains }),
    new CoinbaseWalletConnector({
      chains,
      options: {
        appName: 'wagmi',
      },
    }),
    new WalletConnectConnector({
      chains,
      options: {
        qrcode: true,
      },
    }),
    new InjectedConnector({
      chains,
      options: {
        name: 'Injected',
        shimDisconnect: true,
      },
    }),
  ],
  provider,
})


function MyApp({ Component, pageProps }: AppProps) {
  return (
    <WagmiConfig client={client}>
        <Component {...pageProps} />
        <Analytics />
    </WagmiConfig>
  )
}

export default MyApp

