# $tock$ - Stock trading web app :moneybag:

<code>**$tock$**</code> is a stock trading web platform which uses <code>IEX API</code> for current stocks prices.

$tocks$ users are able to register for a demo account, that automatically gives them $10,000.00 to buy shares of stocks.
Platform uses <code>Flask</code> framework, <code>session</code> and <code>sqlite</code> database to remember and store users and their data and transactions.
All is done with a pretty and clean user interface using <code>CSS</code> and <code>Bootsrap library</code>.

Functionality of $tocks$ includes:
 - User registration
 - User login / logout
 - User account management (changing password, depositing and withdrawing money from demo account)
 - Getting a quote of current prices of U.S. stocks
 - Buying and selling shares with a demo account
 - Dashboard of past transactions
 - Dashboard of open positions
 - Account statistics (available credit, total portfolio, gain/loss)
 
 Click on image to make it bigger
 
 <p><img width="400" alt="$tocks$" src="https://user-images.githubusercontent.com/94573733/153724313-39a1c91d-d128-47a4-9cc0-c8f86c366111.png">
 <img width="400" alt="$tocks$_Buy" src="https://user-images.githubusercontent.com/94573733/153724462-46222525-aea3-4e77-a3f6-3319d6d3c177.png">
 <p><img width="400" alt="$tock$_transactions" src="https://user-images.githubusercontent.com/94573733/153724706-5772aacd-b9e6-474d-946d-f5c59ea4b692.png"></p>

 

This project is still being developed so has not been deployed yet. Although I'm planning to do so once I'm happy with its functionality.
For now to test the plaftorm it is neccesary to:
- Register with IEX Cloud API at https://iexcloud.io/cloud-login#/register/.
  - Once registered, scroll down to “Get started for free” and click “Select Start plan” to choose the free plan.
  - Once you’ve confirmed your account via a confirmation email, visit https://iexcloud.io/console/tokens.
  - Copy the key that appears under the Token column (it should begin with pk_).
  - In your terminal window, execute:
    <code>$ export API_KEY=value</code>
