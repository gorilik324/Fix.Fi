import { Html, Head, Main, NextScript } from 'next/document'
export default function Document() {
  return (
    <Html>
      <Head>
        <meta name="description" content="The Null Fund"/>
        <meta name="keywords" content="Null, Fund"/>
        <meta name="author" content="stacks"/>
        <title>The Null Fund</title>
        <link rel="icon" type="image/x-icon" href="assets/images/favicon.ico" />
        <link href="https://fonts.googleapis.com/css?family=Poppins:400,500,700,800&display=swap" rel="stylesheet"/>
        <link href="../assets/plugins/bootstrap/css/bootstrap.min.css" rel="stylesheet"/>
        <link href="../assets/plugins/font-awesome/css/all.min.css" rel="stylesheet"/>
        <link href="../assets/plugins/perfectscroll/perfect-scrollbar.css" rel="stylesheet"/>
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  )
}