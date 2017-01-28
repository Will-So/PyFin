# Setting up Mint
1. Specify your password as `MINT_PASSWORD` in your environmental variables
2. Run the setup script, you will be asked to enter your username 
2. The first time you run the script, a browser window will be opened and the username and password will automatically be entered
 if 2-factor authentication is enabled, you will have to do that part manually. Afterwards, the program will save your cookies 
 so this won't have to be done again. 
# Setting up Interactive Brokers
1. Set up Interactive brokers in Mint.
2. Make a Flex Query token that is good for one year
3. Enter in that token to the configuration page.
# Setting up lending Club
- Make an environmental variable `LENDING_CLUB_API` with your password
- Change the config file so 


## Notes
We ignore the distinction between portfolio and investor ID in this case. 

- It might be worth investigating [alternatives](https://www.quora.com/Does-Mint-com-have-an-open-API) to the MINT API