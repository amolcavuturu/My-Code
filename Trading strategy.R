library(readr)
library(dplyr)
library(ggplot2)
library(xts)
library(quantmod)
library(corrplot) #used for correlation plots
library(TTR) #used for ROC calculation
library(psych)#used for decriptive analysis
library(quantstrat)
library(blotter)
library(PerformanceAnalytics)

# .blotter <- new.env()
# .strategy <- new.env()



initdate <- "2015-01-01"
frm <- "2015-01-01"
t <- "2020-01-01"

Sys.setenv(TZ = "UTC")

currency("INR")

HDFC <- getSymbols("HDFC.NS", from = frm, to = t, auto.assign = FALSE)

HDFC <- na.omit(HDFC)

sum(is.na(HDFC))

stock("HDFC", currency = "INR")


#define tradesize and initial equity
tradesize <- 100000
initeq <- 100000

#define names of strategy, portfolio and account
strategy.st <- "firststrat"
portfolio.st <- "firststrat"
account.st <- "firststrat"

#remove the existing strategy if it exists
rm.strat(strategy.st)

#initialize the portfolio
initPortf(portfolio.st, symbols = "HDFC", initDate = initdate, currency = "INR")

#initialize the account
initAcct(account.st, portfolios = portfolio.st, initDate = initdate, currency = "INR", initEq = initeq)

#initialize the orders
initOrders(portfolio.st, initDate = initdate)

#store the strategy
strategy(strategy.st, store = TRUE)


#create indicators
SMA200 <- SMA(Cl(HDFC), n = 200)
RSI3 <- RSI(Cl(HDFC), n = 3)

#custom indicator
# Write the calc_RSI_avg function
calc_RSI_avg <- function(price, n1, n2) {
  
  # RSI 1 takes an input of the price and n1
  RSI_1 <- RSI(price = price, n = n1)
  
  # RSI 2 takes an input of the price and n2
  RSI_2 <- RSI(price = price, n = n2)
  
  # RSI_avg is the average of RSI_1 and RSI_2
  x <- (RSI_1 + RSI_2)/2
  
  # Your output of RSI_avg needs a column name of"RSI_avg"
  colnames(x) <- "RSI_avg"
  return(x)
}


# Delare the DVO function
DVO <- function(HLC, navg = 2, percentlookback = 126) {
  
  # Compute the ratio between closing prices to the average of high and low
  ratio <- Cl(HLC)/((Hi(HLC) + Lo(HLC))/2)
  
  # Smooth out the ratio outputs using a moving average
  avgratio <- SMA(ratio, n = navg)
  
  # Convert ratio into a 0-100 value using runPercentRank()
  out <- runPercentRank(avgratio, n = percentlookback, exact.multiplier = 1) * 100
  colnames(out) <- "DVO"
  return(out)
}


plot(Cl(HDFC))
lines(ZigZag(HDFC[,c("HDFC.High", "HDFC.Low")], change = 2), col = "red")
lines(SMA(Cl(HDFC), n = 5), col = "green")
# plot(rsi_3, col = "blue")


#add indicator to strategy

add.indicator(strategy = strategy.st, name = "SMA", arguments = list(x = quote(Cl(mktdata)), n = 50), label = "SMA200")

add.indicator(strategy = strategy.st, name = "SMA", arguments = list(x = quote(Cl(mktdata)), n = 21), label = "SMA50")

add.indicator(strategy = strategy.st, name = "RSI", arguments = list(price = quote(Cl(mktdata)), n = 3), label = "RSI3")

# Add this function as RSI_3_4 to your strategy with n1 = 3 and n2 = 4
#add.indicator(strategy.st, name = "calc_RSI_avg", arguments = list(price=quote(Cl(mktdata)), n1 = 3, n2 = 4), label = "RSI_3_4")

add.indicator(strategy = strategy.st, name = "DVO", arguments = list(HLC = quote(HLC(mktdata)), navg = 2, percentlookback = 126), label = "DVO_2_126")


#test your indicators

test <- applyIndicators(strategy = strategy.st, mktdata = HDFC)
test

#test subset
test_subset <- test["2015-01-01/2016-01-01"]
test_subset


#add signal sigcomparison

add.signal(strategy = strategy.st, name = "sigComparison", arguments = list(columns = c("SMA50","SMA200"), relationship = "gt"), label = "longfilter")

#add signal sigCrossover

add.signal(strategy = strategy.st, name = "sigCrossover", arguments = list(columns = c("SMA50", "SMA200"), relationship = "lt"), label = "filterexit")


# add signal sigThreshold which specifies that rsi_3 must be less than 20, label it longthreshold

add.signal(strategy.st, name = "sigThreshold", arguments = list(column = "DVO_2_126", threshold = 20, relationship = "lt", cross = FALSE), label = "longthreshold")


# add signal sigThreshold which specifies that rsi_3 must cross above 80, label it thresholdexit

add.signal(strategy.st, name = "sigThreshold", arguments = list(column = "DVO_2_126", threshold = 80, relationship = "gt", cross = TRUE), label = "thresholdexit")


# Create your dataset: test
test_init <- applyIndicators(strategy.st, mktdata = OHLC(HDFC))
test_init
test <- applySignals(strategy = strategy.st, mktdata = test_init)
test


# Add signal combined using sigFormula signal to your code specifying that both longfilter and longthreshold must be TRUE, label it longentry

add.signal(strategy.st, name = "sigFormula", arguments = list(formula = "longfilter & longthreshold", cross = TRUE), label = "longentry")



# add rule type = exit,  name = filterexit
add.rule(strategy.st, name = "ruleSignal", 
         arguments = list(sigcol = "filterexit", sigval = TRUE, orderqty = "all", 
                          ordertype = "market", orderside = "long", 
                          replace = FALSE, prefer = "Open"), 
         type = "exit")


# add rule type = exit , name = thresholdexit
add.rule(strategy.st, name = "ruleSignal", 
         arguments = list(sigcol = "thresholdexit", sigval = TRUE, orderqty = "all", 
                          ordertype = "market", orderside = "long", 
                          replace = FALSE, prefer = "Open"), 
         type = "exit")



# add rule type = entry , of 1 share when all conditions line up to enter into a position
add.rule(strategy.st, name = "ruleSignal", 
         arguments = list(sigcol = "longentry", sigval = TRUE, orderqty = 1,
                          ordertype = "market", orderside = "long",
                          replace = FALSE, prefer = "Open"), 
         
         type = "enter")




# # Add a rule that uses an osFUN to size an entry position
# add.rule(strategy = strategy.st, name = "ruleSignal",
#          arguments = list(sigcol = "longentry", sigval = TRUE, ordertype = "market",
#                           orderside = "long", replace = FALSE, prefer = "Open",
#                           
#                           # Use the osFUN called osMaxDollar
#                           osFUN = osMaxDollar,
#                           
#                           # The tradeSize argument should be equal to tradesize (defined earlier)
#                           tradeSize = tradesize,
#                           
#                           # The maxSize argument should be equal to tradesize as well
#                           maxSize = tradesize),
#          type = "enter")



# Use applyStrategy() to apply your strategy. Save this to out
out <- applyStrategy(strategy = strategy.st, portfolios = portfolio.st)

# Update your portfolio (portfolio.st)
updatePortf(portfolio.st)
daterange <- time(getPortfolio(portfolio.st)$summary)[-1]

# Update your account (account.st)
updateAcct(account.st, daterange)
updateEndEq(account.st)


# Get the tradeStats for your portfolio
tstats <- tradeStats(Portfolios = portfolio.st)

# Print the profit factor
tstats$Profit.Factor



#visualisation of results

# Use chart.Posn to view your system's performance on HDFC
chart.Posn(Portfolio = portfolio.st, Symbol = "HDFC")





# Compute the SMA50
sma50 <- SMA(x = Cl(HDFC), n = 50)

# Compute the SMA200
sma200 <- SMA(x = Cl(HDFC), n = 200)

# Compute the DVO_2_126 with an navg of 2 and a percentlookback of 126
dvo <- DVO(HLC = HLC(HDFC), navg = 2, percentlookback = 126)

# Recreate the chart.Posn of the strategy from the previous exercise
chart.Posn(Portfolio = portfolio.st, Symbol = "HDFC")

# Overlay the SMA50 on your plot as a blue line
add_TA(sma50, on = 1, col = "blue")

# Overlay the SMA200 on your plot as a red line
add_TA(sma200, on = 1, col = "red")

# Add the DVO_2_126 to the plot in a new window
add_TA(dvo)




#Cash Sharpe ratio
portpl <- .blotter$portfolio.firststrat$summary$Net.Trading.PL
SharpeRatio.annualized(portpl, geometric=FALSE)




# Get instrument returns
instrets <- PortfReturns(portfolio.st)

# Compute Sharpe ratio from returns
SharpeRatio.annualized(instrets, geometric = FALSE)

